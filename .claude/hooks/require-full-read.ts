#!/usr/bin/env node
/**
 * PreToolUse gate over the authored trees: keep a change to a file from resting on a
 * fragment of it.
 *
 * Reads the hook payload on stdin. Searching stays open — a grep, a git patch, a symbol
 * lookup and a windowed Read all return their lines, each answered with the reminder that
 * they locate the file and settle nothing about it. Writing is where it closes: on a write
 * it walks the session transcript for Read calls on the same file and denies the write when
 * those reads do not cover every line, or when the file changed on disk after they were
 * taken. A shell write is denied outright, through Bash and through the MCP tools that run
 * a shell of their own: no transcript records it, and the gate at the end of the turn
 * cannot see it at all.
 *
 * Writing means every tool that rewrites a file, native or MCP. Reading means Read alone:
 * it is the one call that returns the file whole and reports the bounds it returned.
 *
 * Fails open on every error it cannot attribute to a partial read: a gate that breaks
 * editing is worse than the habit it corrects.
 */

import { readdirSync, readFileSync, realpathSync, statSync } from 'node:fs'
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

// Binaries that write lines of a file to stdout. Gating these is what leaves Read as
// the only way authored content reaches the session, whole and with its line numbers.
const EXTRACTING_BINARIES = new Set([
  'ack',
  'ag',
  'awk',
  'bat',
  'cat',
  'egrep',
  'fgrep',
  'grep',
  'head',
  'less',
  'more',
  'rg',
  'sed',
  'tail',
])

// Binaries that land content on the path given last. The destination is what the gate
// answers for: a source under the authored trees is a move out, which writes nothing there.
const DESTINATION_BINARIES = new Set(['cp', 'install', 'mv'])

// Binaries that write every path they are handed.
const WRITING_BINARIES = new Set(['tee', 'touch', 'truncate'])

// Editors that rewrite their operand instead of printing it, under an in-place flag.
const IN_PLACE_BINARIES = new Set(['perl', 'sed'])

// Git subcommands that write file content to stdout. `log` joins them under a patch flag.
const GIT_PRINTING_SUBCOMMANDS = new Set(['blame', 'cat-file', 'diff', 'show'])
const GIT_PATCH_FLAGS = new Set(['-p', '-u', '--patch'])

// Git flags that reduce the output to names and counts, with no line of content.
const GIT_SUMMARY_FLAGS = new Set([
  '--name-only',
  '--name-status',
  '--numstat',
  '--shortstat',
  '--stat',
])

// Long flags that reduce a search to the names of the files it matched.
const NAME_ONLY_FLAGS = new Set(['--files-with-matches', '--files-without-match'])

// Short flags carrying the same reduction, which cluster: -rl reads as -r -l.
const NAME_ONLY_LETTERS = ['l', 'L']

// The shell operators that end one command and start the next, outside a quote.
const SEGMENT_OPERATORS = new Set(['|', ';', '&', '\n'])

// Native tools that rewrite a file on disk.
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

// MCP tools that run a shell, which reaches the same files Bash does.
const MCP_SHELL_TOOLS = new Set(['ctx_execute', 'ctx_execute_file', 'execute_shell_command'])

// MCP tools that put authored content in context. None of them credits a read: a symbol
// lookup returns a fragment, and `read_file` carries line bounds this gate does not model,
// so both stand where grep stands.
const MCP_LOCATING_TOOLS = new Set([
  'find_referencing_symbols',
  'find_symbol',
  'get_symbols_overview',
  'read_file',
  'search_for_pattern',
])

// MCP tools that name a path without returning a line of it: nothing to credit, nothing to
// gate. Every other MCP tool naming an authored path is judged as a write, which is the
// side to err on for a tool this gate has never heard of.
const MCP_INSPECTING_TOOLS = new Set(['find_file', 'get_diagnostics_for_file', 'list_dir'])

// The keys a tool names its target with. Native tools use `file_path`, Serena uses a path
// relative to the project root, and the plural forms carry a list.
const PATH_KEYS = ['file_path', 'notebook_path', 'relative_path']
const PATH_LIST_KEYS = ['relative_paths', 'file_paths', 'paths']

// A write bumps mtime a moment after the call that caused it is written to the transcript.
// One minute absorbs that gap: past it the file moved for a reason the session cannot see,
// and reads taken before the move no longer describe it.
const EXTERNAL_CHANGE_TOLERANCE_MS = 60_000

type LineRange = [number, number]

interface ReadInput {
  file_path?: unknown
  offset?: unknown
  limit?: unknown
}

interface ToolInput extends ReadInput {
  command?: unknown
  output_mode?: unknown
  path?: unknown
  glob?: unknown
  code?: unknown
  // The path keys are reached by name, which is why the shape stays open.
  [key: string]: unknown
}

interface ContentBlock {
  type?: unknown
  name?: unknown
  input?: unknown
}

function allow(): never {
  process.exit(0)
}

function deny(reason: string): never {
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'deny',
        permissionDecisionReason: reason,
      },
    }),
  )
  process.exit(0)
}

/** Lets the call through with a reminder, which lands next to the lines it returns. */
function remind(target: string): never {
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        additionalContext:
          `These are lines of ${target}, under an authored tree. They say where to look and ` +
          'settle nothing: an authored file is one argument, and a constraint here is answered ' +
          'by another three sections away. Read the file whole before proposing a change to it, ' +
          'and before making a claim about what it says.',
      },
    }),
  )
  process.exit(0)
}

/** Sends a shell write back to Edit/Write, the two calls both gates can reason about. */
function denyShellWrite(target: string): never {
  deny(
    `Change ${target} through Edit or Write, never through the shell. A shell write is ` +
      'content this session never read: the gate before it cannot prove the file was read ' +
      'whole, and the gate at the end of the turn cannot see the file changed at all. ' +
      `Read ${target} in full, then edit it.`,
  )
}

function isAuthored(candidate: string): boolean {
  const projectDir = process.env.CLAUDE_PROJECT_DIR
  if (!projectDir) return false

  const relativePath = relative(projectDir, resolve(projectDir, candidate))
  if (!relativePath || relativePath.startsWith('..') || isAbsolute(relativePath)) return false

  const normalized = relativePath.split(sep).join('/')
  return AUTHORED_DIRS.some(
    (directory) => normalized === directory || normalized.startsWith(`${directory}/`),
  )
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

function sameFile(candidate: string, target: string): boolean {
  try {
    return realpathSync(candidate) === realpathSync(target)
  } catch {
    return resolve(candidate) === resolve(target)
  }
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
 * What the transcript records about one file: every read with the moment it happened, and
 * the moment the session last wrote it.
 */
interface FileEvents {
  reads: Array<{ atMs: number; range: LineRange }>
  lastWriteMs: number
}

/** The reads that describe the file as it now stands, and how many stopped describing it. */
function readRanges(
  transcriptPath: string,
  target: string,
  mtimeMs: number,
): { ranges: LineRange[]; discarded: number } | null {
  const events: FileEvents = { reads: [], lastWriteMs: 0 }
  let openedOne = false

  for (const file of transcriptFiles(transcriptPath)) {
    let transcript: string
    try {
      transcript = readFileSync(file, 'utf8')
    } catch {
      continue
    }
    openedOne = true

    collectEvents(transcript, target, events)
  }

  if (!openedOne) return null

  // A file the session itself last wrote is still described by the reads that precede the
  // write: the one passage that moved is the one the session authored, and it knows it. A
  // file that moved on its own is described by nothing read before the move.
  const movedOutside = mtimeMs > events.lastWriteMs + EXTERNAL_CHANGE_TOLERANCE_MS
  const fresh = events.reads.filter((read) => !movedOutside || read.atMs >= mtimeMs)

  return { ranges: fresh.map((read) => read.range), discarded: events.reads.length - fresh.length }
}

function collectEvents(transcript: string, target: string, events: FileEvents): void {
  for (const line of transcript.split('\n')) {
    if (!line.includes('"tool_use"')) continue

    let entry: { timestamp?: unknown; message?: { content?: unknown } }
    try {
      entry = JSON.parse(line)
    } catch {
      continue
    }

    const atMs = Date.parse(String(entry.timestamp ?? ''))
    if (!Number.isFinite(atMs)) continue

    const content = entry.message?.content
    if (!Array.isArray(content)) continue

    for (const block of content as ContentBlock[]) {
      if (block?.type !== 'tool_use' || typeof block.name !== 'string') continue

      const input = block.input as ToolInput | undefined
      if (!authoredPaths(input).some((path) => sameFile(path, target))) continue

      if (WRITE_TOOLS.has(block.name) || MCP_WRITE_TOOLS.has(bareToolName(block.name))) {
        events.lastWriteMs = Math.max(events.lastWriteMs, atMs)
        continue
      }

      // Read alone credits a read: it is the one call that returns the file whole and
      // reports the bounds it returned.
      if (block.name !== 'Read') continue

      const offset = Math.max(coerceInt(input?.offset, DEFAULT_OFFSET), 1)
      const limit = coerceInt(input?.limit, DEFAULT_LIMIT)
      if (limit < 1) continue

      events.reads.push({ atMs, range: [offset, offset + limit - 1] })
    }
  }
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

/**
 * The segment cut into the words the shell would pass, with the quotes taken off: what a
 * quote holds stays one word, whatever separator or operator is written inside it.
 */
function shellWords(segment: string): string[] {
  const words: string[] = []
  let current = ''
  let started = false
  let quote: "'" | '"' | null = null

  for (let index = 0; index < segment.length; index += 1) {
    const char = segment.charAt(index)

    if (quote !== "'" && char === '\\') {
      current += segment.charAt(index + 1)
      started = true
      index += 1
      continue
    }

    if (quote === null && (char === '"' || char === "'")) {
      quote = char
      // An empty quote is still a word: `sed -i ''` passes one.
      started = true
      continue
    }

    if (quote === char) {
      quote = null
      continue
    }

    if (quote === null && /\s/.test(char)) {
      if (started) words.push(current)
      current = ''
      started = false
      continue
    }

    current += char
    started = true
  }

  if (started) words.push(current)
  return words
}

/**
 * The command cut at the operators that end one segment and start the next, counting quotes
 * on the way: a separator inside a quote is text, and cutting there invents a command the
 * shell would never run.
 */
function shellSegments(command: string): string[] {
  const segments: string[] = []
  let current = ''
  let quote: "'" | '"' | null = null

  for (let index = 0; index < command.length; index += 1) {
    const char = command.charAt(index)

    // A backslash carries the next character through, except inside single quotes where
    // the shell reads it literally.
    if (quote !== "'" && char === '\\') {
      current += char + command.charAt(index + 1)
      index += 1
      continue
    }

    if (quote === null && (char === '"' || char === "'")) {
      quote = char
    } else if (quote === char) {
      quote = null
    } else if (quote === null && SEGMENT_OPERATORS.has(char)) {
      segments.push(current)
      current = ''
      continue
    }

    current += char
  }

  segments.push(current)
  return segments
}

function isNameOnlyFlag(token: string): boolean {
  if (NAME_ONLY_FLAGS.has(token)) return true
  if (token.startsWith('--') || !token.startsWith('-')) return false

  return NAME_ONLY_LETTERS.some((letter) => token.slice(1).includes(letter))
}

function isInPlaceFlag(token: string): boolean {
  if (token.startsWith('--')) return token.startsWith('--in-place')
  if (!token.startsWith('-')) return false

  // `-i` carries its backup suffix and clusters: `perl -pi -e` reads as -p -i -e.
  return token.slice(1).includes('i')
}

/** The binary a segment runs, past the environment assignments that may precede it. */
function binaryOf(tokens: string[]): string | null {
  for (const token of tokens) {
    if (/^[A-Za-z_][A-Za-z0-9_]*=/.test(token)) continue
    return token.split('/').at(-1) || null
  }

  return null
}

/** The path inside a `HEAD:src/rules/naming.md` operand, or the operand as it stands. */
function pathOf(operand: string): string {
  const separator = operand.lastIndexOf(':')
  return separator === -1 ? operand : operand.slice(separator + 1)
}

/** The authored path a git segment would print, or null where it prints none. */
function gitPrintedPath(operands: string[]): string | null {
  const subcommand = operands.find((token) => !token.startsWith('-'))
  if (!subcommand) return null
  if (operands.some((token) => GIT_SUMMARY_FLAGS.has(token))) return null

  const prints =
    GIT_PRINTING_SUBCOMMANDS.has(subcommand) ||
    (subcommand === 'log' && operands.some((token) => GIT_PATCH_FLAGS.has(token)))
  if (!prints) return null

  return (
    operands
      .slice(operands.indexOf(subcommand) + 1)
      .find((token) => !token.startsWith('-') && isAuthored(pathOf(token))) ?? null
  )
}

/** The authored path a shell segment would print, or null where it prints none. */
function extractedPath(segment: string): string | null {
  const tokens = shellWords(segment)
  const binary = binaryOf(tokens)
  if (!binary) return null

  const operands = tokens.slice(tokens.indexOf(binary) + 1)
  if (binary === 'git') return gitPrintedPath(operands)
  if (!EXTRACTING_BINARIES.has(binary)) return null
  if (operands.some(isNameOnlyFlag)) return null

  return operands.find((token) => !token.startsWith('-') && isAuthored(token)) ?? null
}

/** The authored path a redirection in a segment would write, or null where it writes none. */
function redirectedPath(tokens: string[]): string | null {
  for (const [index, token] of tokens.entries()) {
    // `>`, `>>`, `2>` and `&>`, with the path attached to the operator or standing after it.
    const redirection = /^(?:\d*|&)>>?(.*)$/.exec(token)
    if (!redirection) continue

    const target = redirection[1] || tokens[index + 1]
    if (target && isAuthored(target)) return target
  }

  return null
}

/** The authored path a segment would write through its binary, or null where it writes none. */
function writtenOperand(binary: string, operands: string[]): string | null {
  const paths = operands.filter((token) => !token.startsWith('-'))

  if (DESTINATION_BINARIES.has(binary)) {
    const destination = paths.at(-1)
    return destination && isAuthored(destination) ? destination : null
  }

  if (WRITING_BINARIES.has(binary)) return paths.find(isAuthored) ?? null

  if (IN_PLACE_BINARIES.has(binary) && operands.some(isInPlaceFlag)) {
    return paths.find(isAuthored) ?? null
  }

  return null
}

function guardShellWrite(command: unknown): void {
  if (typeof command !== 'string' || !command) return

  for (const segment of shellSegments(command)) {
    const tokens = shellWords(segment)

    const redirected = redirectedPath(tokens)
    if (redirected) denyShellWrite(redirected)

    const binary = binaryOf(tokens)
    if (!binary) continue

    const written = writtenOperand(binary, tokens.slice(tokens.indexOf(binary) + 1))
    if (written) denyShellWrite(written)
  }
}

function noticeExtraction(command: unknown): void {
  if (typeof command !== 'string' || !command) return

  for (const segment of shellSegments(command)) {
    const path = extractedPath(segment)
    if (path) remind(path)
  }
}

/** A content search over the authored trees, which returns their lines without their file. */
function noticeGrep(input: ToolInput | undefined): void {
  if (input?.output_mode !== 'content') return

  const target = [input.path, input.glob].find(
    (value) => typeof value === 'string' && value && isAuthored(value),
  )
  if (typeof target === 'string') remind(target)
}

/** A window over a file one call could return whole. */
function noticeWindowedRead(input: ReadInput | undefined, target: string, total: number): void {
  if (input?.offset === undefined && input?.limit === undefined) return
  // Past the ceiling of one call the window is the only way through the file.
  if (total > DEFAULT_LIMIT) return

  remind(basename(target))
}

function guardPartialEdit(
  transcript: unknown,
  target: string,
  total: number,
  mtimeMs: number,
): void {
  if (typeof transcript !== 'string' || !transcript) return

  const history = readRanges(transcript, target, mtimeMs)
  // Transcript unreadable: cannot prove a partial read, so do not block on it.
  if (history === null) return

  const { ranges, discarded } = history
  const gap = firstGap(ranges, total)
  if (gap === null) return

  const detail =
    discarded > 0
      ? 'it changed outside this session after it was read, so what was read no longer describes it'
      : ranges.length === 0
        ? 'it has not been read in this session'
        : `the session has only read lines ${ranges
            .toSorted((left, right) => left[0] - right[0])
            .map(([start, end]) => `${start}-${Math.min(end, total)}`)
            .join(', ')} of ${total}; line ${gap} onward is unread`

  deny(
    `Read ${basename(target)} in full before editing it — ${detail}. ` +
      'Editing from a window produces a patch that fits the window and contradicts ' +
      `the rest of the file. Call Read on ${target} with no offset/limit ` +
      `(repeat with offset for files over ${DEFAULT_LIMIT} lines), then edit.`,
  )
}

/** Answers for one authored path a call names. Returns where the path raises no question. */
function guardTarget(
  transcript: unknown,
  toolName: string,
  input: ToolInput | undefined,
  target: string,
): void {
  let data: Buffer
  try {
    data = readFileSync(target)
  } catch {
    // Missing file: this is a create, and there is nothing to have read.
    return
  }

  if (data.subarray(0, BINARY_SNIFF_BYTES).includes(0)) return

  const total = lineCount(data)
  if (total === 0) return

  if (toolName === 'Read') {
    noticeWindowedRead(input, target, total)
    return
  }

  let mtimeMs = 0
  try {
    mtimeMs = statSync(target).mtimeMs
  } catch {
    // Unstattable: no moment to compare a read against, so judge on coverage alone.
  }

  guardPartialEdit(transcript, target, total, mtimeMs)
}

function main(): void {
  let payload: { tool_name?: unknown; tool_input?: ToolInput; transcript_path?: unknown }
  try {
    payload = JSON.parse(readFileSync(0, 'utf8'))
  } catch {
    allow()
  }

  const toolName = typeof payload.tool_name === 'string' ? payload.tool_name : ''
  const bareName = bareToolName(toolName)
  const input = payload.tool_input

  if (toolName === 'Bash') {
    // Writing first: `sed -i` on an authored file also reads as an extraction, and a
    // reminder in place of the denial would let the write through.
    guardShellWrite(input?.command)
    noticeExtraction(input?.command)
    allow()
  }

  // An MCP shell reaches the same files Bash does, through a field of its own.
  if (MCP_SHELL_TOOLS.has(bareName)) {
    guardShellWrite(input?.command ?? input?.code)
    allow()
  }

  if (toolName === 'Grep') {
    noticeGrep(input)
    allow()
  }

  const targets = authoredPaths(input)
  const [first] = targets
  if (!first) allow()

  if (MCP_INSPECTING_TOOLS.has(bareName)) allow()

  // Answered before the file is opened: a symbol search names a directory as often as a file.
  if (MCP_LOCATING_TOOLS.has(bareName)) remind(basename(first))

  // Every path, not the first: one `replace_in_files` rewrites a list of them.
  for (const target of targets) {
    guardTarget(payload.transcript_path, toolName, input, target)
  }

  allow()
}

main()
