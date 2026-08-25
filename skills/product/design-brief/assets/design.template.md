<!--
DESIGN.md skeleton. Delete every comment and replace every square-bracket slot before writing the file.

Frontmatter keys: version, name, description, omitted, colors, typography, rounded, spacing, components.
Overview through Do's and Don'ts are the official spec sections. Agent Prompt Guide is a skill extension.
Colors are flat CSS strings. Keep borders, shadows, elevation, and light/dark behavior in prose.
Use only official component properties. Define backgroundColor and textColor together for every text-bearing component.
Every color needs a component reference unless a deliberate omission or documented CLI warning remains.
-->
---
# version: [schema version only when required]
name: [system name]
description: [one-line visual identity summary]

# omitted:
#   - section: [section]
#     reason: "[why it does not apply]"

colors:
  primary: "#______"
  on-primary: "#______"
  secondary: "#______"
  surface: "#______"
  on-surface: "#______"
  muted: "#______"
  on-muted: "#______"
  border: "#______"
  error: "#______"
  on-error: "#______"

typography:
  display:
    fontFamily: "[display face]"
    fontSize: 4rem
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -0.03em
  heading:
    fontFamily: "[display face]"
    fontSize: 2rem
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.02em
  body:
    fontFamily: "[body face]"
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "[body face]"
    fontSize: 0.75rem
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: 0.08em

rounded:
  none: 0px
  sm: 0.25rem
  md: 0.5rem
  full: 9999px

spacing:
  xs: 0.25rem
  sm: 0.5rem
  md: 1rem
  lg: 2rem
  xl: 4rem

components:
  page:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
  button-primary-hover:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-primary}"
  card:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.on-muted}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  error-message:
    backgroundColor: "{colors.error}"
    textColor: "{colors.on-error}"
    typography: "{typography.body}"
  divider:
    backgroundColor: "{colors.border}"
    height: 1px
---

# [System name]

## Overview

[Named direction, identity thesis, register, density, signature, and explicit trade-off.]

## Colors

[Palette argument and real referent. Explain each color's job. Describe light and dark behavior in prose without structured skin tokens.]

## Typography

[Typeface classification, pairing, scale, optical adjustments, weight discipline, numerals, variable axes, delivery, and fallbacks.]

## Layout

[Spacing base, density, grid posture, measure, alignment, and structural rhythm.]

## Elevation & Depth

[Borders, tonal layers, shadows, light direction, and depth tiers expressed as prose.]

## Shapes

[Corner hierarchy, border widths, stroke posture, and shape language expressed as prose.]

## Components

[Usage, states, sizing, and relationships for the component tokens.]

## Do's and Don'ts

- Do [specific enforceable identity rule].
- Don't [specific failure this identity is prone to].

## Agent Prompt Guide

[Short downstream guidance that refers to tokens and component roles. Use placeholders such as [Headline], [Body], [CTA Label], and [Nav Label].]

MUST NOT contain: product copy, product-domain token keys, feature names, audience pitches, requirement IDs, milestones, roadmap language, page arrangement, screen flow, UI-library names, structured skin groups, or frontmatter keys outside the official schema.
