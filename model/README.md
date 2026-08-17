# Canonical source

This directory is the **canonical source** for the Agent Work Model.

Generated Markdown and normalized JSON under `generated/` are derived from
these files. Do not hand-edit generated artifacts or maintain a parallel
glossary.

## Layout

| Path | Role |
| --- | --- |
| `catalog.yaml` | Model identity, load order, accepted term keys, native systems, lint conventions |
| `terms/*.yaml` | One accepted term per file |
| `rules/*.yaml` | Architecture rules consumed by lint and future prose |
| `mappings/*.yaml` | Native-system mapping hooks (exact / partial / ambiguous / tbd / none) |

Load order is deterministic: catalog first, then YAML files in each
directory in lexicographic filename order. Term documents are then
arranged in `catalog.term_keys` order for generation.

## Editing a term

1. Change the YAML under `terms/`, `rules/`, or `mappings/`.
2. If you add a term or system, update `catalog.yaml`.
3. Run `make check` (validate + lint + tests + generated-drift check).
4. Commit the source **and** the regenerated files together.

See the repository README for field meanings and the contribution workflow.
