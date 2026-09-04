# Long-form documentation conformance report

## Scope

- Repository: `aleksclark/agent-work-model`
- Worktree / branch: `.worktrees/cloudflare-docs-site` / `cloudflare-docs-site`
- Base SHA: `ff7e81a6904bf4a2a10d1705d2f25a5f094a5a2b`
- Frontend roots: `awm/site.py`, `site/`
- Local design authority: `site/DESIGN.md`
- Test/gate commands: `python3 -m pytest`, `python3 -m awm check`, `python3 -m awm site`
- Selected accent: cyan `#3DE0F0`

## Route and surface inventory

| Route | Primary surface | Secondary | Long-form treatment |
| --- | --- | --- | --- |
| `/` | Decide / Learn | Explore | 16px prose, 65ch measure, page contents |
| `/boundaries` | Decide / Learn | Inspect | 16px prose, 65ch measure, page contents |
| `/interoperability` | Decide / Learn | Inspect | 16px prose, 65ch measure, page contents |
| `/specifications` | Decide / Learn | Inspect | 16px prose, 65ch measure, page contents |
| `/glossary` | Explore | Inspect | Compact reference table; labeled records on mobile |
| `/reference` | Inspect | Explore | Compact reference tables; labeled records on mobile |
| `/terms/*` | Inspect | Learn | Compact metadata and tables; labeled records on mobile |

## Findings and decisions

| ID | Priority | Status | Finding | Resolution / evidence |
| --- | --- | --- | --- | --- |
| LF-001 | P1 foundation | INTENTIONAL EXCEPTION | Fixed 14px body role is optimized for product UI, not sustained prose. | Scoped 16px / 1.7 long-form role documented in `product-design-exceptions.md`; reference UI remains unchanged. |
| LF-002 | P1 composition | PASS | Long pages lacked local orientation. | Generated sticky desktop “On this page” rail and mobile native disclosure. |
| LF-003 | P1 composition | PASS | Prose occupied only part of the 960px canvas without using the remaining space. | Text capped at 65ch; remaining width carries local contents rather than more prose. |
| LF-004 | P2 responsive | PASS | Dense reference tables previously required hidden horizontal panning. | Existing labeled-record mobile recomposition retained; browser probes report zero wrapper overflow. |
| LF-005 | P2 accessibility | PASS | Long-form layout must tolerate user text spacing. | WCAG 1.4.12 override probe at 390px produced zero clipped elements and zero document overflow. |
| LF-006 | P2 hierarchy | PASS | Long-form sections needed stronger scan landmarks. | Scoped 20px desktop / 18px mobile prose-section role; reference headings retain house scale. |
| DM-001 | P1 hosting | PASS | Canonical production host changed. | Pages custom domains active; canonical tags, sitemap, robots, workflow URL, and redirect plan use `agent-work-model.org`. |

## Best-practice inputs

- U.S. Web Design System: dedicated Prose and In-page Navigation patterns.
- W3C WCAG 2.2 Understanding 1.4.12: layout tolerance for line, paragraph, letter, and word spacing overrides.
- Butterick’s Practical Typography: target average line length of roughly 45–90 characters.
- Nielsen Norman Group: web readers scan; descriptive headings, front-loaded meaning, and visible structure improve comprehension.

## Final evidence

- Computed prose: Archivo 16px / 27.2px.
- Computed section heading: Archivo 20px / 26px desktop; 18px / 23.4px mobile.
- Computed measure: 65ch (approximately 521px with the loaded Archivo face).
- Desktop contents: 200px sticky rail; mobile contents: native disclosure in document flow.
- Dark desktop: `longform-overview-desktop-dark.png`.
- Dark mobile: `longform-boundaries-mobile-dark-toc-open.png`.
- Light parity: `longform-boundaries-mobile-light-toc-open.png`.
- Text-spacing stress: `longform-spacing-override-mobile.png`, zero clipping/overflow.
- Fonts remain Archivo / Newsreader / IBM Plex Mono; no extra accent, elevation, radius, or spacing values.

## Open blockers

None. Production DNS/TLS is active for the apex and `www` host. Cloudflare dynamic redirect rules return path- and query-preserving HTTP 301 responses from `www.agent-work-model.org`, `agentregistryprotocol.org`, and `www.agentregistryprotocol.org` to the canonical apex.
