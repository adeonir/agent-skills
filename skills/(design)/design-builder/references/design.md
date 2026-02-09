# Design Extraction

Extract design tokens from reference images and generate design.json.

## When to Use

- User provides reference images (pasted, file path, or URL)
- User wants to extract a design system from screenshots or mockups
- User wants to generate design tokens from a style description (no images)

## Process

### Step 1: Get Project Context

1. Ask user for the project name (if not already established)
2. Check for existing artifacts:
   - `.specs/docs/{project-name}/copy.yaml` -- content context
   - `.specs/docs/prd-{project-name}.md` -- product context
3. Use available artifacts to inform design decisions

### Step 2: Get Reference Input

**If images are provided** (pasted, file path, or URL):
1. Analyze each image for design tokens
2. If multiple images have conflicting styles, ask user which to prioritize:
   - Option A: describe style 1
   - Option B: describe style 2
   - Option C: merge (use X from A, Y from B)

**If no images are provided:**
1. Ask user about visual direction:
   - Tone (professional, playful, minimal, bold)
   - Color mood (warm neutrals, cool blues, vibrant, monochrome)
   - Typography mood (serif headings + sans body, all geometric, editorial)
   - Any inspirations or websites they admire
2. Generate tokens from the description

### Step 3: Deep Analysis

Extract from each image:
- Exact color values (HEX, not approximations)
- Font families (suggest Google Fonts equivalents if unsure)
- Spacing patterns (section padding, component gaps)
- Component styles (buttons, cards, badges, inputs)
- Animation and interaction patterns
- Background treatments (gradients, textures, patterns)

### Step 4: Generate design.json

Save to `.specs/docs/{project-name}/design.json`. Create directories if needed.

## Output Schema

```json
{
  "meta": {
    "name": "Project Design System",
    "version": "1.0",
    "extracted_from": ["reference-1.png", "reference-2.png"]
  },

  "principles": {
    "overall": "Premium fintech with warmth - sophisticated but approachable",
    "keywords": ["trustworthy", "premium", "warm", "clean", "modern"],
    "avoid": [
      "Generic purple gradients",
      "Inter as lazy fallback",
      "Icons without real images",
      "Identical layouts across sections",
      "Missing hover states",
      "Cramped spacing"
    ]
  },

  "colors": {
    "primary": {
      "main": "#1C3F3A",
      "light": "#2A5A52",
      "dark": "#152E2A"
    },
    "accent": {
      "main": "#C4F233",
      "hover": "#D4FF4D"
    },
    "neutral": {
      "white": "#FFFFFF",
      "cream": "#F8F6F0",
      "sand": "#EBE8D8",
      "gray": "#718096",
      "charcoal": "#2D2D2D",
      "black": "#1A1A1A"
    },
    "semantic": {
      "success": "#38A169",
      "warning": "#ECC94B",
      "error": "#E53E3E",
      "info": "#3182CE"
    },
    "usage": {
      "backgrounds": [
        "white for main sections",
        "cream for alternating sections",
        "primary.main for emphasis/CTA sections"
      ],
      "text": {
        "primary": "charcoal for headings",
        "secondary": "gray for body",
        "onDark": "white on dark backgrounds"
      },
      "interactive": "primary.main for links and buttons"
    }
  },

  "typography": {
    "fonts": {
      "heading": "Playfair Display",
      "body": "Inter",
      "mono": "JetBrains Mono"
    },
    "scale": {
      "hero": {
        "size": "clamp(2.5rem, 5vw, 4rem)",
        "weight": 700,
        "lineHeight": 1.1,
        "letterSpacing": "-0.02em"
      },
      "h2": {
        "size": "clamp(2rem, 4vw, 3rem)",
        "weight": 600,
        "lineHeight": 1.2
      },
      "h3": {
        "size": "1.25rem",
        "weight": 600,
        "lineHeight": 1.4
      },
      "body": {
        "size": "1rem",
        "weight": 400,
        "lineHeight": 1.6
      },
      "small": {
        "size": "0.875rem",
        "weight": 400,
        "lineHeight": 1.5
      },
      "label": {
        "size": "0.75rem",
        "weight": 500,
        "letterSpacing": "0.05em",
        "textTransform": "uppercase"
      }
    },
    "emphasis": {
      "technique": "Italic serif for emotional keywords",
      "example": "The first assistant that truly understands your *money*"
    }
  },

  "spacing": {
    "philosophy": "Generous breathing room - whitespace is a feature",
    "section": {
      "y": "clamp(80px, 10vw, 140px)",
      "x": "clamp(20px, 5vw, 80px)"
    },
    "container": {
      "maxWidth": "1200px"
    },
    "grid": {
      "columns": 12,
      "gap": "24px"
    },
    "component": {
      "xs": "4px",
      "sm": "8px",
      "md": "16px",
      "lg": "24px",
      "xl": "32px",
      "2xl": "48px"
    }
  },

  "components": {
    "button": {
      "primary": {
        "bg": "primary.main",
        "text": "neutral.white",
        "radius": "9999px",
        "padding": "16px 32px",
        "fontSize": "1rem",
        "fontWeight": 500,
        "hover": {
          "bg": "primary.light",
          "transform": "translateY(-2px)",
          "shadow": "lg"
        },
        "transition": "all 0.2s ease"
      },
      "secondary": {
        "bg": "transparent",
        "text": "primary.main",
        "border": "1.5px solid primary.main",
        "radius": "9999px",
        "hover": {
          "bg": "primary.main",
          "text": "neutral.white"
        }
      }
    },
    "card": {
      "default": {
        "bg": "neutral.white",
        "radius": "16px",
        "padding": "32px",
        "shadow": "md",
        "hover": {
          "transform": "translateY(-4px)",
          "shadow": "lg"
        },
        "transition": "all 0.3s ease"
      }
    },
    "badge": {
      "default": {
        "bg": "neutral.cream",
        "text": "primary.main",
        "radius": "9999px",
        "padding": "8px 16px",
        "fontSize": "0.75rem",
        "textTransform": "uppercase",
        "letterSpacing": "0.05em"
      }
    },
    "input": {
      "default": {
        "bg": "neutral.white",
        "border": "1px solid neutral.sand",
        "radius": "12px",
        "padding": "16px 20px",
        "focus": {
          "border": "primary.main",
          "shadow": "focus"
        }
      }
    },
    "icon": {
      "sizes": {
        "sm": "16px",
        "md": "20px",
        "lg": "24px",
        "xl": "32px",
        "feature": "48px"
      },
      "strokeWidth": 1.5
    }
  },

  "effects": {
    "shadows": {
      "sm": "0 1px 3px rgba(0,0,0,0.08)",
      "md": "0 4px 12px rgba(0,0,0,0.08)",
      "lg": "0 10px 40px rgba(0,0,0,0.1)",
      "xl": "0 20px 60px rgba(0,0,0,0.15)",
      "focus": "0 0 0 3px rgba(28,63,58,0.1)"
    },
    "transitions": {
      "fast": "all 0.15s ease",
      "default": "all 0.2s ease",
      "smooth": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
      "slow": "all 0.5s ease"
    }
  },

  "animations": {
    "fadeInUp": {
      "from": { "opacity": 0, "y": 20 },
      "to": { "opacity": 1, "y": 0 },
      "duration": "0.6s",
      "easing": "cubic-bezier(0.4, 0, 0.2, 1)"
    },
    "fadeIn": {
      "from": { "opacity": 0 },
      "to": { "opacity": 1 },
      "duration": "0.4s"
    },
    "hoverLift": {
      "transform": "translateY(-4px)",
      "duration": "0.3s"
    },
    "stagger": {
      "delay": "0.1s",
      "description": "Apply between list items"
    }
  },

  "backgrounds": {
    "patterns": {
      "grain": {
        "opacity": "2-3%",
        "description": "Subtle noise texture overlay"
      },
      "dots": {
        "size": "2px",
        "gap": "20px",
        "opacity": "5%"
      }
    },
    "gradients": {
      "subtle": "linear-gradient(180deg, white 0%, cream 100%)",
      "radial": "radial-gradient(ellipse at top, cream 0%, white 70%)",
      "dark": "linear-gradient(180deg, primary.main 0%, primary.dark 100%)"
    },
    "sections": {
      "light": "neutral.white",
      "alternate": "neutral.cream",
      "dark": "primary.main",
      "accent": "accent.main"
    }
  },

  "responsive": {
    "breakpoints": {
      "sm": "640px",
      "md": "768px",
      "lg": "1024px",
      "xl": "1280px"
    },
    "mobile": {
      "fontSize": "Reduce scale by 10-15%",
      "spacing": "Reduce section padding",
      "layout": "Stack to single column"
    }
  }
}
```

## Rules

1. **Extract EXACT values** -- use color picker precision, don't approximate
2. **Identify fonts** -- suggest Google Fonts equivalents if unsure
3. **Capture ALL states** -- hover, focus, active, disabled
4. **Document anti-patterns** -- in `principles.avoid`, list what NOT to do
5. **Be specific** -- values in px, rem, hex. Nothing generic.

## What to AVOID in design.json

- Generic purple gradients
- Inter as the only font
- 8px border-radius on everything
- Heavy drop shadows
- Cramped spacing
- Missing hover states
- Vague descriptions like "nice blue"

## Next Steps

After generating design.json, suggest:
- "Run build frontend to generate React components"
- "Run generate variants to preview 4 layout options before building"
- "Run export design to generate HTML for Figma/Penpot import"
