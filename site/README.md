# Documentation site source

Hand-authored assets for the Agent Work Model docs site. Generated HTML
is written to `_site/` by `python3 -m awm site` and is not checked in.

| Path | Role |
| --- | --- |
| `DESIGN.md` | Editorial Instrument plus the AWM long-form documentation extension |
| `product-design-exceptions.md` | Audited local exceptions for sustained prose |
| `conformance-report.md` | Route inventory, findings, decisions, and evidence |
| `assets/house-tokens.css` | House tokens plus scoped long-form roles |
| `assets/house-tokens.json` | Framework-neutral token source |
| `assets/house-icons.svg` | Flat outline icon sprite |
| `assets/site.css` | Site layout only |
| `assets/site.js` | Theme, nav, and copy affordances |

Do not invent page-local tokens in `site.css`. Accent is cyan `#3DE0F0`.
The primary surface class is Decide / Learn. Long-form typography and
layout follow the documented extension in `DESIGN.md`. Production hosting
is Cloudflare Pages at https://agent-work-model.org/.
