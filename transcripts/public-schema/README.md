# Public schema snapshot

`models.dev-model-schema.json` is an unchanged public JSON Schema downloaded from <https://models.dev/model-schema.json> on August 31, 2026. Its declared identifier is `https://models.dev/model-schema.json`.

The official OpenCode configuration schema references this dependency for its model field. The first offline CI execution exposed the unresolved external reference. `scripts/check_permissions.py` registers this local snapshot under the original identifier so validation uses the same official definitions without network access. This snapshot is source data, not an AI-generated replacement schema.
