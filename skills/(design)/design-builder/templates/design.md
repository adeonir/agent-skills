---
version: alpha
name: {{Project Name}}
description: {{One sentence summary of the brand and product}}

colors:
  {Required base palette. Hex SRGB only. Add semantic surface variants and on-X pairs as needed. Common convention: primary, secondary, tertiary, neutral.}
  primary: "{{#hex}}"
  on-primary: "{{#hex}}"
  primary-container: "{{#hex}}"
  on-primary-container: "{{#hex}}"
  secondary: "{{#hex}}"
  on-secondary: "{{#hex}}"
  tertiary: "{{#hex}}"
  on-tertiary: "{{#hex}}"
  background: "{{#hex}}"
  on-background: "{{#hex}}"
  surface: "{{#hex}}"
  on-surface: "{{#hex}}"
  surface-container: "{{#hex}}"
  outline: "{{#hex}}"
  error: "{{#hex}}"
  on-error: "{{#hex}}"

typography:
  {Semantic categories: display, headline, body, label. Each may divide into sm, md, lg. Required fields: fontFamily, fontSize, fontWeight, lineHeight. Optional: letterSpacing.}
  display-lg:
    fontFamily: {{Font Family}}
    fontSize: {{Npx}}
    fontWeight: {{number}}
    lineHeight: {{Dimension or number}}
    letterSpacing: {{em or px}}
  headline-lg:
    fontFamily: {{Font Family}}
    fontSize: {{Npx}}
    fontWeight: {{number}}
    lineHeight: {{Dimension or number}}
  body-lg:
    fontFamily: {{Font Family}}
    fontSize: {{Npx}}
    fontWeight: {{number}}
    lineHeight: {{Dimension or number}}
  body-md:
    fontFamily: {{Font Family}}
    fontSize: {{Npx}}
    fontWeight: {{number}}
    lineHeight: {{Dimension or number}}
  label-sm:
    fontFamily: {{Font Family}}
    fontSize: {{Npx}}
    fontWeight: {{number}}
    lineHeight: {{Dimension or number}}
    letterSpacing: {{em or px}}

rounded:
  {Scale levels are descriptive strings. Common: sm, DEFAULT, md, lg, xl, full.}
  sm: {{Dimension}}
  DEFAULT: {{Dimension}}
  md: {{Dimension}}
  lg: {{Dimension}}
  xl: {{Dimension}}
  full: 9999px

spacing:
  {Scale levels are descriptive strings. Mix unit base with named tokens.}
  unit: {{Npx}}
  container-padding: {{Dimension}}
  card-gap: {{Dimension}}
  section-margin: {{Dimension}}

components:
  {Each component maps a name to props from the allowlist: backgroundColor, textColor, typography, rounded, padding, size, height, width. Variants use sibling keys: button-primary, button-primary-hover, button-primary-disabled. Reference syntax: "{colors.primary}".}
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    height: 48px
    padding: 0 24px
  button-primary-hover:
    backgroundColor: "{colors.primary-container}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.lg}"
    padding: "{spacing.container-padding}"

motion:
  {Cover duration scale and easing language.}
  duration:
    fast: {{Nms}}
    base: {{Nms}}
    slow: {{Nms}}
  easing:
    standard: {{cubic-bezier(...) or named curve}}
    accelerate: {{cubic-bezier(...)}}
    decelerate: {{cubic-bezier(...)}}

variants:
  {Each named variant overrides one or more token blocks. Use for themes (light/dark), density modes (comfortable/compact), brand variants (A/B). Omit the block entirely if no variants are defined.}
  {{variant-name}}:
    colors:
      {Token overrides — only the keys that change}
    typography:
      {Token overrides — only the keys that change}
---

# {{Project Name}}

## Overview

{Holistic description of look and feel. Cover brand personality, target audience, emotional response (playful vs professional, dense vs spacious), and the foundational stylistic context the agent draws on when a specific token is not defined. Two to four short paragraphs.}

## Colors

{Describe key color palettes by descriptive name (e.g. "Midnight Forest Green") and explain how each maps to the semantic tokens above. Cover tone, contrast goals, accent usage, and any palette-to-role assignment (primary, secondary, tertiary, neutral).}

## Typography

{Describe font choices and pairing rationale. Explain the role of each typography token and how the display/headline/body/label scales map to UI hierarchy. Note any letter-spacing or line-height conventions.}

## Layout

{Cover spacing rhythm (e.g. 8px scale), container conventions, grid behavior, and density choices. Reference spacing tokens by name. If the product is screen-based, summarize navigation pattern and primary action placement here and detail flow in the Screen Flow section that follows.}

## Screen Flow

{Screen-based products only (web-app, mobile-app). Describe screen inventory, primary user paths, modal vs full-screen patterns, and required state variants (empty, loading, error). Omit this section for page-based products (landing-page, website).}

## Elevation & Depth

{Describe how depth is communicated (shadows, surfaces, layering, blur). If using surface-tint or surface-container variants, explain their role.}

## Shapes

{Describe corner radius philosophy (e.g. "soft, organic" or "sharp, technical"), border treatments, and how the rounded scale maps to component categories.}

## Motion

{Describe motion philosophy: easing language, duration ranges, and what motion communicates (responsiveness, hierarchy, emphasis). Reference the motion tokens above. Note any reduced-motion fallbacks.}

## Components

{Describe each component's role and behavior. Cover variants (hover, pressed, disabled), sizing rules, and when to use each variant. Reference the component tokens above.}

## Variants

{Describe non-component variants: themes (light/dark), density modes (comfortable/compact), brand variants (A/B). Explain when each applies and how token overrides cascade. Omit this section if no variants are defined.}

## Do's and Don'ts

**Do:**

{One bullet per pattern the design system endorses. Lead with the action.}

- {Action — short rationale}
- {Action — short rationale}

**Don't:**

{One bullet per anti-pattern. Each bullet contrasts a corresponding Do above.}

- {Anti-pattern — short rationale}
- {Anti-pattern — short rationale}
