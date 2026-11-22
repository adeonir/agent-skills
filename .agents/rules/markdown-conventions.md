## Fenced Code Blocks Declare a Language

**Impact: MEDIUM**

Every fenced code block carries a language tag. An untagged fence trips the repo's bare-fence self-check and loses syntax highlighting, and a security audit reads an unlabeled block as possible obfuscation.

**Incorrect:**

````text
```
npm install
```
````

**Correct:**

````text
```bash
npm install
```
````

## Forward Slashes in Paths

**Impact: MEDIUM**

Write every path with forward slashes. Backslash paths break on Unix, and a skill runs on every platform the consumer uses.

**Incorrect:**

```text
scripts\helper.py
```

**Correct:**

```text
scripts/helper.py
```
