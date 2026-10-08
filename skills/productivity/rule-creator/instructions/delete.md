# Delete

Remove a rule file.

## Workflow

1. **Resolve the target** the same way [edit.md](edit.md) does: by filename, topic, or rule title, asking when ambiguous.
2. **Read the file and show the user what is about to be deleted.** The full content, not just the filename.
3. **Ask for explicit confirmation, naming the level:** "Delete this <level> rule?". At user level, state that it stops applying to every project on the machine. Default no. When the target is a symlink, ask instead which of two acts the user means:
   - **Unlink here** — remove the link, leaving the shared target intact. The rule stops applying to this project only.
   - **Delete the target** — remove the shared file. The rule dies everywhere, and every other project keeps a dangling link the skill cannot reach to clean up.

   Default to unlinking; it is the narrower act, and the wider one is not reversible from here.
4. **On confirmation, `rm` the file or the link the user chose.**
5. **Output a summary:** filename deleted, level, scope, rule titles removed.

## When a rule contains multiple H2 sections

If the user wants to delete only one rule from a multi-rule file, route to [edit.md](edit.md) instead. Delete operates at file granularity.
