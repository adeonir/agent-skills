#!/usr/bin/env node
/**
 * Stop gate: refuse to end the turn while an authored file was written and not read again.
 *
 * Reads the hook payload on stdin, walks the transcript of the turn under way, and blocks
 * the stop when a file's last write is not followed by Reads covering every line of it.
 * A write is any tool that rewrites a file, native or MCP; a read is Read alone.
 * A patch is written against the passage it touches; what it contradicts two sections up
 * shows only on a reading of the whole file after the fact.
 *
 * Fails open on every error it cannot attribute to a missing re-read: a gate that traps
 * the turn is worse than the habit it corrects.
 */

import { readdirSync, readFileSync, realpathSync } from 'node:fs'
import { basename, dirname, isAbsolute, join, relative, resolve, sep } from 'node:path'

// Read tool defaults: reads start at line 1 and return at most 2000 lines when the
// call carries no offset/limit, so an omitted argument stands in for these.
const DEFAULT_OFFSET = 1
const DEFAULT_LIMIT = 2000

// 8192: enough of the head to spot a NUL byte in a binary or image file, which Read
// does not return as lines and this gate therefore cannot reason about.
const BINARY_SNIFF_BYTES = 8192

// Authoring only: the two product trees the CLI ships, the two workshop trees that
// produce them, and the bridge a call reaches a workshop skill through.
const AUTHORED_DIRS = ['README.md', 'AGENTS.md', '.agents', 'src']

const WRITE_TOOLS = new Set(['Edit', 'NotebookEdit', 'Write'])

// MCP tools that rewrite a file on disk. Named bare: the server prefix varies with how
// the plugin is installed, and only the part past the last separator is stable.
const MCP_WRITE_TOOLS = new Set([
  'create_text_file',
  'insert_after_symbol',
  'insert_before_symbol',
  'rename_symbol',
  'replace_content',
  'replace_in_files',
  'replace_symbol_body',
  'safe_delete_symbol',
])

// The keys a tool names its target with. Native tools use `file_path`, Serena uses a path
// relative to the project root, and the plural forms carry a list.
const PATH_KEYS = ['file_path', 'notebook_path', 'relative_path']
const PATH_LIST_KEYS = ['relative_paths', 'file_paths', 'paths']

type LineRange = [number, number]

interface ToolInput {
  file_path?: unknown
  offset?: unknown
  limit?: unknown
  // The path keys are reached by name, which is why the shape stays open.
  [key: string]: unknown
}

interface ContentBlock {
  type?: unknown
  name?: unknown
  input?: unknown
}

/** Per file: whether this turn wrote it, and every read that came after the last write. */
interface FileHistory {
  written: boolean
  readsAfter: LineRange[]
}

function allow(): never {
  process.exit(0)
}

function block(reason: string): never {
  process.stdout.write(JSON.stringify({ decision: 'block', reason }))
  process.exit(0)
}

function isAuthored(target: string): boolean {
  const projectDir = process.env.CLAUDE_PROJECT_DIR
  if (!projectDir) return false

  // Resolved against the project, not the shell: an MCP tool names its target relative
  // to the repository root.
  const relativePath = relative(projectDir, resolve(projectDir, target))
  if (!relativePath || relativePath.startsWith('..') || isAbsolute(relativePath)) return false

  const normalized = relativePath.split(sep).join('/')
  return AUTHORED_DIRS.some((directory) => normalized.startsWith(`${directory}/`))
}

/** The tool name past its server prefix: `mcp__plugin_serena_serena__read_file` is `read_file`. */
function bareToolName(name: string): string {
  return name.startsWith('mcp__') ? (name.split('__').at(-1) ?? name) : name
}

/** Every authored path a tool input names, absolute. */
function authoredPaths(input: ToolInput | undefined): string[] {
  if (!input) return []

  const candidates: unknown[] = PATH_KEYS.map((key) => input[key])
  for (const key of PATH_LIST_KEYS) {
    const value = input[key]
    if (Array.isArray(value)) candidates.push(...value)
  }

  const projectDir = process.env.CLAUDE_PROJECT_DIR ?? ''
  return candidates
    .filter((value): value is string => typeof value === 'string' && !!value && isAuthored(value))
    .map((value) => resolve(projectDir, value))
}

function coerceInt(value: unknown, fallback: number): number {
  const parsed = typeof value === 'number' ? value : Number.parseInt(String(value ?? ''), 10)
  return Number.isFinite(parsed) ? Math.trunc(parsed) : fallback
}

function resolveKey(target: string): string {
  try {
    return realpathSync(target)
  } catch {
    return resolve(target)
  }
}

/**
 * A message the user typed, told apart from the one the harness writes to carry a tool result:
 * the first is text, the second is a content array of `tool_result` blocks.
 */
function isTyped(content: unknown): boolean {
  if (typeof content === 'string') return true
  if (!Array.isArray(content)) return false
  return (content as ContentBlock[]).some((entry) => entry?.type === 'text')
}

function lineCount(data: Buffer): number {
  if (data.length === 0) return 0

  let newlines = 0
  for (const byte of data) {
    if (byte === 0x0a) newlines += 1
  }

  return data.at(-1) === 0x0a ? newlines : newlines + 1
}

/**
 * The session transcript plus the one each subagent writes. A subagent reads and edits
 * through its own transcript, so leaving those out reads as "never read" for every file
 * it just opened.
 */
function transcriptFiles(transcriptPath: string): string[] {
  const files = [transcriptPath]
  const subagentDir = join(dirname(transcriptPath), basename(transcriptPath, '.jsonl'), 'subagents')

  try {
    for (const entry of readdirSync(subagentDir)) {
      if (entry.endsWith('.jsonl')) files.push(join(subagentDir, entry))
    }
  } catch {
    // No subagent directory: the session never spawned one.
  }

  return files
}

/**
 * The order is the order of the lines: a write clears the reads recorded before it, so what
 * survives is what was read after the last one. Two transcripts carry no order between them,
 * which is why the reads of a subagent count for the writes of the session that spawned it.
 *
 * A message the user typed clears the history whole. The gate answers for the turn under way,
 * and a file written and reviewed three turns ago is closed: carrying it forward would ask for
 * the whole session to be read again at every stop.
 */
function collectHistory(transcriptPath: string): Map<string, FileHistory> | null {
  const history = new Map<string, FileHistory>()
  let openedOne = false

  for (const file of transcriptFiles(transcriptPath)) {
    let transcript: string
    try {
      transcript = readFileSync(file, 'utf8')
    } catch {
      continue
    }
    openedOne = true

    for (const line of transcript.split('\n')) {
      if (!line.includes('"tool_use"') && !line.includes('"user"')) continue

      let entry: { message?: { role?: unknown; content?: unknown } }
      try {
        entry = JSON.parse(line)
      } catch {
        continue
      }

      const content = entry.message?.content
      if (entry.message?.role === 'user' && isTyped(content)) {
        history.clear()
        continue
      }

      if (!Array.isArray(content)) continue

      for (const rawBlock of content as ContentBlock[]) {
        if (rawBlock?.type !== 'tool_use') continue

        const name = rawBlock.name
        if (typeof name !== 'string') continue

        const writes = WRITE_TOOLS.has(name) || MCP_WRITE_TOOLS.has(bareToolName(name))
        // Read alone credits a read: it is the one call that returns the file whole and
        // reports the bounds it returned.
        if (!writes && name !== 'Read') continue

        const input = rawBlock.input as ToolInput | undefined

        // One call rewrites many files: `replace_in_files` takes a list.
        for (const path of authoredPaths(input)) {
          const key = resolveKey(path)
          const known = history.get(key) ?? { written: false, readsAfter: [] }

          if (writes) {
            known.written = true
            known.readsAfter = []
            history.set(key, known)
            continue
          }

          if (!known.written) continue

          const offset = Math.max(coerceInt(input?.offset, DEFAULT_OFFSET), 1)
          const limit = coerceInt(input?.limit, DEFAULT_LIMIT)
          if (limit < 1) continue

          known.readsAfter.push([offset, offset + limit - 1])
          history.set(key, known)
        }
      }
    }
  }

  return openedOne ? history : null
}

/** Lowest line not covered by any range, or null when the file is fully covered. */
function firstGap(ranges: LineRange[], total: number): number | null {
  let cursor = 1

  for (const [start, end] of ranges.toSorted((left, right) => left[0] - right[0])) {
    if (start > cursor) return cursor
    if (end >= cursor) cursor = end + 1
    if (cursor > total) return null
  }

  return cursor > total ? null : cursor
}

function needsReread(target: string, ranges: LineRange[]): boolean {
  let data: Buffer
  try {
    data = readFileSync(target)
  } catch {
    // Gone from disk: a file the run deleted or moved has nothing left to read.
    return false
  }

  if (data.subarray(0, BINARY_SNIFF_BYTES).includes(0)) return false

  const total = lineCount(data)
  if (total === 0) return false

  return firstGap(ranges, total) !== null
}

function main(): void {
  let payload: { transcript_path?: unknown; stop_hook_active?: unknown }
  try {
    payload = JSON.parse(readFileSync(0, 'utf8'))
  } catch {
    allow()
  }

  // Already blocked once and the turn came back here: let it end rather than trap it.
  if (payload.stop_hook_active === true) allow()

  const transcript = payload.transcript_path
  if (typeof transcript !== 'string' || !transcript) allow()

  const history = collectHistory(transcript)
  // Transcript unreadable: cannot prove a missing re-read, so do not block on it.
  if (history === null) allow()

  const pending = [...history.entries()]
    .filter(([target, entry]) => entry.written && needsReread(target, entry.readsAfter))
    .map(([target]) => target)

  if (pending.length === 0) allow()

  block(
    `Read what you just wrote before ending the turn: ${pending.join(', ')}. ` +
      'A patch is written against the passage it touches, and what it contradicts elsewhere ' +
      'in the file shows only on a reading of the whole file after the edit. ' +
      'Call Read on each path with no offset/limit, fix what the reading turns up, then stop.',
  )
}

main()
