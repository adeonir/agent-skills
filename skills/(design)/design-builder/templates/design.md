---
name: {{project-name}}
source: {{image path, url, or "description-based"}}
created: {{YYYY-MM-DD}}
---

# Design Extraction: {{Project Name}}

## Output

Save as `.specs/docs/{{project-name}}/design.json` using the schema below.

## Schema

```json
{
  "metadata": {
    "source": "{{image-path or url}}",
    "extraction_date": "{{YYYY-MM-DD}}",
    "version": "1.1.0"
  },
  "principles": {
    "vision": "{{one-sentence design direction}}",
    "keywords": ["{{keyword}}", "{{keyword}}", "{{keyword}}"],
    "follow": [
      "{{guideline to follow}}",
      "{{guideline to follow}}"
    ],
    "avoid": [
      "{{anti-pattern to avoid}}",
      "{{anti-pattern to avoid}}"
    ]
  },
  "design_system": {
    "colors": {
      "primary": {
        "main": "{{hex}}",
        "light": "{{hex}}",
        "dark": "{{hex}}",
        "contrast": "{{hex}}"
      },
      "secondary": {
        "main": "{{hex}}",
        "light": "{{hex}}",
        "dark": "{{hex}}",
        "contrast": "{{hex}}"
      },
      "background": {
        "default": "{{hex}}",
        "paper": "{{hex}}",
        "elevated": "{{hex}}"
      },
      "text": {
        "primary": "{{hex}}",
        "secondary": "{{hex}}",
        "disabled": "{{hex}}",
        "contrast": "{{hex}}"
      },
      "semantic": {
        "success": "{{hex}}",
        "warning": "{{hex}}",
        "error": "{{hex}}",
        "info": "{{hex}}"
      }
    },
    "typography": {
      "font_family": {
        "heading": "{{font-name}}",
        "body": "{{font-name}}",
        "mono": "{{font-name}}"
      },
      "scale": {
        "hero": { "size": "{{rem/px}}", "weight": "{{400-900}}", "line_height": "{{number}}" },
        "h2": { "size": "{{rem/px}}", "weight": "{{400-900}}", "line_height": "{{number}}" },
        "h3": { "size": "{{rem/px}}", "weight": "{{400-900}}", "line_height": "{{number}}" },
        "body": { "size": "{{rem/px}}", "weight": "{{400-900}}", "line_height": "{{number}}" },
        "small": { "size": "{{rem/px}}", "weight": "{{400-900}}", "line_height": "{{number}}" },
        "label": { "size": "{{rem/px}}", "weight": "{{400-900}}", "line_height": "{{number}}", "letter_spacing": "{{em}}" }
      }
    },
    "spacing": {
      "unit": "{{rem/px}}",
      "scale": ["{{0}}", "{{4px}}", "{{8px}}", "{{16px}}", "{{24px}}", "{{32px}}", "{{48px}}", "{{64px}}"],
      "section_padding": { "x": "{{rem/px}}", "y": "{{rem/px}}" },
      "container_max_width": "{{rem/px}}"
    },
    "borders": {
      "radius": {
        "small": "{{px}}",
        "medium": "{{px}}",
        "large": "{{px}}",
        "pill": "{{px}}"
      },
      "width": {
        "thin": "{{px}}",
        "medium": "{{px}}",
        "thick": "{{px}}"
      }
    },
    "shadows": {
      "small": "{{css-shadow-value}}",
      "medium": "{{css-shadow-value}}",
      "large": "{{css-shadow-value}}",
      "elevated": "{{css-shadow-value}}"
    }
  },
  "components": {
    "{{component_name}}": {
      "style": {
        "background": "{{color-ref}}",
        "text_color": "{{color-ref}}",
        "border": "{{border-ref}}",
        "border_radius": "{{radius-ref}}",
        "padding": "{{spacing-ref}}"
      },
      "states": {
        "hover": { "background": "{{color-ref}}" },
        "active": { "background": "{{color-ref}}" },
        "focus": { "outline": "{{css-outline-value}}" },
        "disabled": { "opacity": "{{0-1}}" }
      }
    }
  },
  "layout": {
    "hero": {
      "composition": "{{layout description: centered, split, asymmetric}}",
      "height": "{{vh or px}}",
      "content_alignment": "{{center, left, right}}",
      "decorative_elements": ["{{element description}}"]
    },
    "sections": [
      {
        "name": "{{section-name}}",
        "grid": { "columns": "{{number}}", "gap": "{{rem/px}}" },
        "background": "{{color-ref or gradient}}",
        "padding": { "x": "{{rem/px}}", "y": "{{rem/px}}" },
        "pattern": "{{layout pattern: cards-grid, alternating, stacked, masonry}}"
      }
    ],
    "decorative": {
      "dividers": "{{style: none, gradient-line, svg-wave, geometric}}",
      "accents": ["{{accent description}}"]
    }
  },
  "animations": {
    "entrance": {
      "type": "{{fadeInUp, fadeIn, slideIn, scaleIn}}",
      "duration": "{{ms}}",
      "easing": "{{css-easing}}",
      "stagger_delay": "{{ms}}"
    },
    "interaction": {
      "hover_lift": { "transform": "{{css-transform}}", "duration": "{{ms}}" },
      "button_press": { "transform": "{{css-transform}}", "duration": "{{ms}}" }
    },
    "transitions": {
      "default": { "property": "{{all, opacity, transform}}", "duration": "{{ms}}", "easing": "{{css-easing}}" }
    }
  },
  "backgrounds": {
    "hero": "{{gradient, solid, image, pattern description}}",
    "sections": {
      "{{section-name}}": "{{background treatment}}"
    },
    "gradients": {
      "primary": "{{css-gradient-value}}",
      "accent": "{{css-gradient-value}}"
    }
  },
  "responsive": {
    "breakpoints": {
      "mobile": "{{px}}",
      "tablet": "{{px}}",
      "desktop": "{{px}}"
    },
    "mobile_adaptations": ["{{adaptation description}}"]
  },
  "notes": {
    "extraction": "{{Notes about extraction process}}",
    "uncertainties": "{{Unclear or ambiguous tokens that need confirmation}}"
  }
}
```
