# Frozen protocol manifests

`tools/lab.py freeze` creates new-ID-only JSON manifests containing root paths,
SHA-256 hashes, and the Git commit at the time of freezing. Inputs must already be
committed. `verify` detects edits, removals, and additions under frozen directories.

A hash is a provenance check, not protection against an agent that can edit the
files or helper. This is not an adversarially isolated test or a scientific proof.
Never overwrite an existing freeze. New protocol versions need a documented reason,
new confirmation seeds, and an explicit disclosure of any previously observed tests.
