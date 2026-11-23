#!/usr/bin/env python3
"""Resolve the Obsidian vault a new note goes to.

Usage:
  python3 vault.py [--vault <dir>]

Prints the vault directory: --vault when given, the only vault in Obsidian's
obsidian.json, or the open one. Exit 0 with the path, 2 when no single vault
can be picked.
"""

import argparse
import json
import os
import sys

OBSIDIAN_CONFIGS = [
    "~/Library/Application Support/obsidian/obsidian.json",
    "~/.config/obsidian/obsidian.json",
    "~/.var/app/md.obsidian.Obsidian/config/obsidian/obsidian.json",
    os.path.join(os.environ.get("APPDATA", ""), "obsidian", "obsidian.json"),
]


def known_vaults():
    for config in OBSIDIAN_CONFIGS:
        try:
            with open(os.path.expanduser(config), encoding="utf-8") as handle:
                vaults = list(json.load(handle).get("vaults", {}).values())
        except (OSError, ValueError, AttributeError):
            continue
        if vaults:
            return vaults
    return []


def default_vault(vault):
    """The vault a new note goes to: --vault, the only vault, or the open one."""
    if vault:
        return vault if os.path.isdir(vault) else None
    vaults = known_vaults()
    if len(vaults) == 1:
        return vaults[0].get("path")
    open_vaults = [v.get("path") for v in vaults if v.get("open")]
    return open_vaults[0] if len(open_vaults) == 1 else None


def main():
    parser = argparse.ArgumentParser(description="Resolve the Obsidian vault a new note goes to.")
    parser.add_argument("--vault")
    args = parser.parse_args()
    vault = default_vault(args.vault)
    if vault is None and args.vault:
        print(f"{args.vault} is not a directory. Pass an existing vault directory with --vault.")
        return 2
    if vault is None:
        print("cannot pick the vault from obsidian.json. Pass the vault directory with --vault.")
        return 2
    print(vault)
    return 0


if __name__ == "__main__":
    sys.exit(main())
