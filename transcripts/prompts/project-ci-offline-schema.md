# Repair the actual offline schema dependency failure

The final local run passed lint, mypy, pip consistency, requirements, semantics, full upstream/application tests and all six expected rejections. Gate 2 failed because `scripts/check_permissions.py` validates the official OpenCode schema, whose `Model` definition references `https://models.dev/model-schema.json#/$defs/Model`. JSON Schema then fetched that URL and failed without networking. The candidate check had passed while that URL was reachable.

Edit ONLY `scripts/check_permissions.py`. The coordinator has now fetched the exact public dependency and archived it, unchanged, at `transcripts/public-schema/models.dev-model-schema.json` inside the repository. Use this actual vendored file; do not replace its enum, change the official configuration schema, remove schema validation or change any permission rule.

Register the local dependency under its real `$id` URI `https://models.dev/model-schema.json` using the installed `referencing.Registry` and `Resource.from_contents`, then pass that explicit registry to `jsonschema.Draft202012Validator`. Resolve the file relative to this script's repository, so both local and GitHub CI use the same snapshot. A missing or invalid required dependency must report a clear permission-check failure. The explicit registry must not fall back to network retrieval. Keep the existing config and manifest checks intact.

The actual failure log is `evaluation/ci-initial/check_static.stdout.txt` if needed. Do not change source, tests, thresholds, root config, permission manifest, approvals, schema data or other scripts. Do not run commands; the coordinator will immediately run the two previously failed real gates, then commit the fix and run all six gates once against the new HEAD.
