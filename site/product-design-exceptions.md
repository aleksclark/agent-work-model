# Product design exceptions

## Product and surface

- Product: Agent Work Model documentation
- Frontend path: `site/` and generated `_site/`
- Primary surface class: Decide / Learn
- Secondary surface classes: Explore (glossary), Command / Inspect (reference and term pages)
- Local design authority: `site/DESIGN.md`

## Accent

Selected: `#3DE0F0` cyan

Reason: Retains the established Agent Work Model identity and provides strong focus and selection contrast in both themes.

## Deliberate exceptions

| House invariant | Local value/behavior | Product reason | Approval/evidence |
| --- | --- | --- | --- |
| Long-form body uses the fixed 14px body role | Explanatory prose uses Archivo 16px / 1.7; reference UI remains 14px or compact | Overview and Guides contain sustained prose rather than operational UI. A dedicated reading role improves comfort without enlarging dense reference material. | User requested a long-form redesign. Practical Typography recommends 45–90 characters per line; W3C requires layouts to tolerate at least 1.5 line height and user spacing overrides. Browser evidence is recorded on PR #2. |
| Section heading uses the fixed 15px section role | Long-form section headings use Archivo 20px / 1.3 desktop and 18px / 1.3 mobile | Long articles need stronger scan landmarks than reference tables and inspectors. | User-approved design-system update; desktop/mobile dark and light screenshots on PR #2. |
| Reading width is a 960px page region | Long-form text is capped at 65ch inside the 960px region, with a 200px in-page navigation rail on wide screens | A bounded measure reduces return-sweep distance while using otherwise empty space for orientation. | 65ch sits within the 45–90-character guidance and matches common public design-system prose patterns. |

No color, font-family, spacing-scale, radius, elevation, focus, status, or icon exceptions are introduced.

## Long-form contract

- Overview and Guide pages use the long-form reading role.
- Wide screens show a sticky “On this page” rail generated from section headings.
- Tablet and mobile replace the rail with a native disclosure immediately after the page header.
- One idea lands per section; section headings remain descriptive out of context.
- Paragraphs and lists have no fixed height and must tolerate WCAG 1.4.12 text-spacing overrides.
- Glossary, reference, and term pages retain compact technical typography and responsive record tables.

## Collection contract

The site contains no remotely fetched resource collection. Glossary and reference tables are deterministically generated from the bounded canonical model under `model/`.

- Human-readable primary field: term key/name
- Secondary ID field: qualified identity field
- Server query operation: not applicable (static build)
- Server sort/filter fields: not applicable
- Pagination model and bound: canonical accepted term list
- URL state: one generated page per term

## Verification

- Dark desktop screenshot: managed-headless browser, overview and Guides at 1280px
- Dark mobile screenshot: managed-headless browser, overview and Guides at 390px
- Light parity screenshot: managed-headless browser, overview and Guides at 1280px and 390px
- Accessibility evidence: semantic article/nav/details structure, keyboard focus checks, WCAG text-spacing override test
- Real browser/integration gate: public Cloudflare Pages deployment at `https://agent-work-model.org/`
