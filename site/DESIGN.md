---
version: alpha
name: Editorial Instrument
description: Dark-primary technical editorial house system for product and operational browser interfaces.
colors:
  primary: "#3DE0F0"
  accent-violet: "#B98BFF"
  accent-cyan: "#3DE0F0"
  accent-mint: "#7CFFB2"
  accent-ink: "#15170E"
  dark-canvas: "oklch(0.178 0.008 250)"
  dark-sunken: "oklch(0.152 0.008 250)"
  dark-surface: "oklch(0.212 0.009 250)"
  dark-raised: "oklch(0.252 0.010 250)"
  dark-rule: "oklch(0.298 0.010 250)"
  dark-rule-strong: "oklch(0.392 0.012 250)"
  dark-text: "oklch(0.955 0.005 250)"
  dark-text-secondary: "oklch(0.822 0.007 250)"
  dark-text-tertiary: "oklch(0.668 0.009 250)"
  light-canvas: "oklch(0.985 0.003 250)"
  light-sunken: "oklch(0.952 0.004 250)"
  light-surface: "oklch(1 0 0)"
  light-raised: "oklch(0.938 0.005 250)"
  light-rule: "oklch(0.882 0.006 250)"
  light-rule-strong: "oklch(0.782 0.010 250)"
  light-text: "oklch(0.215 0.012 250)"
  light-text-secondary: "oklch(0.405 0.012 250)"
  light-text-tertiary: "oklch(0.538 0.012 250)"
  status-ok-dark: "oklch(0.80 0.14 152)"
  status-warning-dark: "oklch(0.83 0.15 78)"
  status-danger-dark: "oklch(0.72 0.16 26)"
  status-info-dark: "oklch(0.80 0.08 235)"
  status-ok-light: "oklch(0.48 0.13 152)"
  status-warning-light: "oklch(0.52 0.13 68)"
  status-danger-light: "oklch(0.50 0.18 26)"
  status-info-light: "oklch(0.45 0.09 235)"
  status-ok-bg-dark: "oklch(0.2526 0.0173 175.8)"
  status-warning-bg-dark: "oklch(0.2562 0.0111 83.1)"
  status-danger-bg-dark: "oklch(0.2430 0.0150 6.9)"
  status-info-bg-dark: "oklch(0.2402 0.0151 242.1)"
  status-ok-bg-light: "oklch(0.9395 0.0116 165.4)"
  status-warning-bg-light: "oklch(0.9431 0.0090 67.4)"
  status-danger-bg-light: "oklch(0.9462 0.0126 17.2)"
  status-info-bg-light: "oklch(0.9422 0.0099 239.1)"
typography:
  display:
    fontFamily: Newsreader
    fontSize: 48px
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: "-0.015em"
  display-mobile:
    fontFamily: Newsreader
    fontSize: 32px
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: "-0.015em"
  page-title:
    fontFamily: Archivo
    fontSize: 30px
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.022em"
  page-title-mobile:
    fontFamily: Archivo
    fontSize: 22px
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.022em"
  section:
    fontFamily: Archivo
    fontSize: 15px
    fontWeight: 600
    lineHeight: 1.2
  lede:
    fontFamily: Archivo
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: Archivo
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
  body-compact:
    fontFamily: Archivo
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
  control:
    fontFamily: Archivo
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1
  label:
    fontFamily: Archivo
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.3
  metadata:
    fontFamily: IBM Plex Mono
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.5
  eyebrow:
    fontFamily: IBM Plex Mono
    fontSize: 10px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "0.16em"
  data:
    fontFamily: IBM Plex Mono
    fontSize: 30px
    fontWeight: 500
    lineHeight: 1
  data-mobile:
    fontFamily: IBM Plex Mono
    fontSize: 22px
    fontWeight: 500
    lineHeight: 1
  code:
    fontFamily: IBM Plex Mono
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.7
rounded:
  sm: 2px
  md: 2px
  pill: 999px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.accent-ink}"
    typography: "{typography.control}"
    rounded: "{rounded.md}"
    height: 34px
    padding: 16px
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.dark-text-secondary}"
    typography: "{typography.control}"
    rounded: "{rounded.md}"
    height: 34px
    padding: 16px
  input:
    backgroundColor: "{colors.dark-sunken}"
    textColor: "{colors.dark-text}"
    typography: "{typography.control}"
    rounded: "{rounded.md}"
    height: 34px
    padding: 12px
  surface:
    backgroundColor: "{colors.dark-surface}"
    textColor: "{colors.dark-text}"
    rounded: "{rounded.md}"
    padding: 16px
  metadata:
    backgroundColor: "{colors.dark-canvas}"
    textColor: "{colors.dark-text-tertiary}"
    typography: "{typography.metadata}"
    rounded: "{rounded.sm}"
    padding: 8px
  accent-option-violet:
    backgroundColor: "{colors.accent-violet}"
    textColor: "{colors.accent-ink}"
    rounded: "{rounded.sm}"
    padding: 8px
  accent-option-cyan:
    backgroundColor: "{colors.accent-cyan}"
    textColor: "{colors.accent-ink}"
    rounded: "{rounded.sm}"
    padding: 8px
  accent-option-mint:
    backgroundColor: "{colors.accent-mint}"
    textColor: "{colors.accent-ink}"
    rounded: "{rounded.sm}"
    padding: 8px
  raised-state:
    backgroundColor: "{colors.dark-raised}"
    textColor: "{colors.dark-text}"
    rounded: "{rounded.sm}"
    padding: 8px
  rule-subtle:
    backgroundColor: "{colors.dark-rule}"
    textColor: "{colors.dark-text}"
    height: 1px
  rule-strong:
    backgroundColor: "{colors.dark-rule-strong}"
    textColor: "{colors.dark-text}"
    height: 2px
  light-page:
    backgroundColor: "{colors.light-canvas}"
    textColor: "{colors.light-text}"
    padding: 16px
  light-sunken:
    backgroundColor: "{colors.light-sunken}"
    textColor: "{colors.light-text-secondary}"
    rounded: "{rounded.md}"
    padding: 12px
  light-surface:
    backgroundColor: "{colors.light-surface}"
    textColor: "{colors.light-text}"
    rounded: "{rounded.md}"
    padding: 16px
  light-raised:
    backgroundColor: "{colors.light-raised}"
    textColor: "{colors.light-text-secondary}"
    rounded: "{rounded.sm}"
    padding: 8px
  light-rule-subtle:
    backgroundColor: "{colors.light-rule}"
    textColor: "{colors.light-text}"
    height: 1px
  light-rule-strong:
    backgroundColor: "{colors.light-rule-strong}"
    textColor: "{colors.light-text}"
    height: 2px
  light-tertiary-metadata:
    backgroundColor: "{colors.light-canvas}"
    textColor: "{colors.light-text-tertiary}"
    typography: "{typography.metadata}"
    padding: 8px
  status-ok:
    backgroundColor: "{colors.status-ok-bg-dark}"
    textColor: "{colors.status-ok-dark}"
    rounded: "{rounded.sm}"
    padding: 8px
  status-warning:
    backgroundColor: "{colors.status-warning-bg-dark}"
    textColor: "{colors.status-warning-dark}"
    rounded: "{rounded.sm}"
    padding: 8px
  status-danger:
    backgroundColor: "{colors.status-danger-bg-dark}"
    textColor: "{colors.status-danger-dark}"
    rounded: "{rounded.sm}"
    padding: 8px
  status-info:
    backgroundColor: "{colors.status-info-bg-dark}"
    textColor: "{colors.status-info-dark}"
    rounded: "{rounded.sm}"
    padding: 8px
  status-ok-light:
    backgroundColor: "{colors.status-ok-bg-light}"
    textColor: "{colors.status-ok-light}"
    rounded: "{rounded.sm}"
    padding: 8px
  status-warning-light:
    backgroundColor: "{colors.status-warning-bg-light}"
    textColor: "{colors.status-warning-light}"
    rounded: "{rounded.sm}"
    padding: 8px
  status-danger-light:
    backgroundColor: "{colors.status-danger-bg-light}"
    textColor: "{colors.status-danger-light}"
    rounded: "{rounded.sm}"
    padding: 8px
  status-info-light:
    backgroundColor: "{colors.status-info-bg-light}"
    textColor: "{colors.status-info-light}"
    rounded: "{rounded.sm}"
    padding: 8px
---

## Overview

Editorial Instrument is the mandatory house fallback when a product has no stronger local design system. Dark mode is canonical. Light mode preserves identical geometry and semantics.

Projects choose exactly one accent: violet `#B98BFF`, cyan `#3DE0F0`, or mint `#7CFFB2`. Change `colors.primary` to the chosen allowed value. Typography, sizes, spacing, shape, status colors, focus, elevation, and icon geometry remain fixed. Comfortable density is the default; compact density requires an explicit task or local product requirement.

## Colors

Use semantic roles rather than raw palette values. The four dark grounds are canvas, sunken, surface, and raised. Text uses primary, secondary, and tertiary roles. Status colors mean health/status only and never act as extra product accents.

## Typography

Archivo is the product face. Newsreader appears selectively on Decide/Learn display copy. IBM Plex Mono is reserved for IDs, timestamps, units, code, technical metadata, and compact uppercase eyebrows. Do not invent sizes between the listed tokens.

## Layout

Classify every screen as Monitor, Operate, Configure, Explore, Command/Inspect, or Decide/Learn before composing it. Use the fixed spacing scale and the comfortable/compact profiles from `house-tokens.json`. Human-readable names lead list and detail identity; machine IDs are secondary.

Resource collections are searched, sorted, filtered, and paginated by the server. Browser controls may persist query state but render only bounded server responses.

## Elevation & Depth

Use flat hierarchy: typography, spacing, alignment, rules, and ground levels. Only modal and toast may cast a shadow. Do not use gradients, glass, blur, glow, or ornamental texture.

## Shapes

General controls and surfaces use 2px radius. Pill radius is reserved for compact status labels and switch tracks. Selection uses a 2px accent rule plus a restrained ground shift.

## Components

Navigation combines a clean flat outline icon with a human label. Icons use a 24px grid, 1.75px currentColor stroke, and round caps/joins; render at 16px by default. Status always combines icon, text, and color.

Operational headers use eyebrow, title, lede, actions, and optional ruled metadata. Forms use label/help and control columns on wide screens. Lists prioritize names/titles over IDs. Empty and error states explain cause and next action.

## Do's and Don'ts

Do design dark mode first, use one allowed accent, keep typography/spacing rigid, default to comfortable density, prefer human-readable names, and send collection controls to the server.

Do not treat a framework theme as design, use centered heroes on operational surfaces, make every section a card, add arbitrary shadows/pills, decorate headings with icon tiles, use emoji as product icons, lead with opaque IDs when names exist, or transform live resource collections in the browser.

## Agent Work Model long-form extension

Agent Work Model is primarily a Decide / Learn documentation surface with unusually prose-heavy Overview and Guide pages. The local exception record is `site/product-design-exceptions.md`; it changes no color, font-family, spacing, shape, focus, status, elevation, or icon invariant.

### Evidence base

- Butterick’s Practical Typography recommends roughly 45–90 characters per line and warns that long return sweeps reduce reading comfort.
- U.S. Web Design System provides dedicated Prose and In-page Navigation patterns rather than treating running text like compact application UI.
- W3C WCAG 2.2 Success Criterion 1.4.12 requires content to survive user overrides including 1.5 line height and larger paragraph, letter, and word spacing.
- Nielsen Norman Group’s scanning guidance supports descriptive headings, front-loaded meaning, short sections, and visible structure for web reading.

### Long-form typography

- Running explanatory prose: Archivo 16px / 1.7.
- Long-form section heading: Archivo 20px / 1.3 desktop, 18px / 1.3 mobile.
- Lede on long-form pages: Archivo 16px / 1.6.
- Reflective or persuasive emphasis may use Newsreader at the same 16px / 1.7 reading role.
- Measure: maximum 65ch. Never widen prose to fill the 960px reference canvas.
- Reference tables, controls, metadata, code, glossary, and term inspectors retain the original compact house scale.

### Long-form composition

1. Kicker, title, and concise lede establish the promise.
2. A generated “On this page” list exposes the article structure.
3. One idea lands per section under a heading that makes sense out of context.
4. Wide screens place the contents list in a quiet sticky right rail; tablet/mobile use a native disclosure after the header.
5. Section spacing uses the existing 24/32/48px scale. Rules mark major transitions but do not underline every heading.
6. Links remain visibly underlined in prose. Machine identifiers remain secondary mono text.
7. No text container uses fixed height; 200% zoom and WCAG text-spacing overrides must not clip or overlap content.

### Long-form navigation

Primary navigation remains Overview, Glossary, and Reference. Guides are a numbered secondary learning sequence. The in-page contents rail is local to one article and must not compete with global navigation. On narrow screens, global navigation remains an explicit drawer and article contents remain in document flow.

### Responsive reference data

Reference tables remain tabular on wide screens. At mobile widths they recompose into labeled records using the same semantic row order. Do not shrink essential identifiers or require hidden horizontal panning.
