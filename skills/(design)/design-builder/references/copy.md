# Copy Extraction

Extract structured content from URLs and organize into copy.yaml.

## When to Use

- User provides a URL to extract content from
- User wants to structure website content for redesign
- User needs copy.yaml as input for design extraction or frontend building

## Process

### Step 1: Get Project Context

1. Ask user for the URL to analyze
2. Ask user for the project name (kebab-case for directories)
3. Check for existing PRD at `.specs/docs/prd-{project-name}.md` -- use as context if available

### Step 2: Fetch and Analyze

1. Fetch the URL using WebFetch
2. If fetch fails, ask user to paste a screenshot instead
3. Identify the project type by analyzing the content:
   - Landing page: single page with hero, features, CTA, footer
   - Website: multi-page site with navigation between pages
   - Web app: interactive application with screens, widgets, auth
   - Mobile app: screens, tabs, gestures, native features
4. Confirm project type with user if unclear

Do not use prefixed types. Ask the user and adapt the schema to match what they are building.

### Step 3: Extract Content

Analyze the structure and extract all content:

- Navigation structure (logo, links, CTA)
- Section hierarchy with layout information
- Text content (headlines, body, CTAs) preserving original tone
- Visual placeholders with descriptions for image generation
- Copywriting patterns (tone, power words, CTA style)

### Step 4: Generate copy.yaml

Save to `.specs/docs/{project-name}/copy.yaml`. Create directories if needed.

## Output Schema

The schema adapts to the project type. Core structure:

```yaml
project:
  name: "project-name"
  type: "landing"
  language: "en"
  industry: "fintech"
  description: "Brief project description"

navigation:
  logo: "Brand Name"
  links:
    - label: "Features"
      href: "#features"
  cta:
    text: "Get Started"
    href: "#signup"

sections:
  - id: hero
    type: hero
    layout:
      columns: 2
      split: "55/45"
    content:
      badge: "New"
      headline: "Main headline here"
      subheadline: "Supporting text here"
      cta_primary:
        text: "Primary CTA"
        icon: "ArrowRight"
      cta_secondary:
        text: "Secondary CTA"
      trust_indicator: "Trusted by 10,000+ users"
    visual:
      type: "generate"
      description: "Detailed description of image to generate"
      floating_elements:
        - "Floating card 1"

  - id: features
    type: features
    layout:
      columns: 3
      background: "cream"
    content:
      eyebrow: "FEATURES"
      headline: "Section headline"
      items:
        - icon: "Zap"
          title: "Feature title"
          description: "Feature description"

  - id: testimonials
    type: testimonials
    content:
      headline: "What customers say"
      items:
        - quote: "Quote text"
          author: "Name"
          role: "Title, Company"
          avatar: "generate"

  - id: cta
    type: cta
    layout:
      background: "dark"
      centered: true
    content:
      headline: "Final CTA headline"
      benefits:
        - "Benefit 1"
      cta:
        text: "CTA button text"
        icon: "ArrowRight"

footer:
  logo: "Brand Name"
  description: "Brief company description"
  columns:
    - title: "Product"
      links: ["Features", "Pricing", "Changelog"]
    - title: "Company"
      links: ["About", "Blog", "Careers"]
  legal:
    copyright: "2025 Company Name"
    links: ["Privacy Policy", "Terms of Service"]

copywriting_notes:
  tone: "Professional yet approachable"
  patterns:
    - "CTAs use arrow icons"
    - "Headlines emphasize key words in italic"
  power_words:
    - "instantly"
    - "automatically"
```

### Web App Schema

For web apps, replace sections with screens:

```yaml
auth:
  screens:
    - id: login
      fields: ["email", "password"]
      actions: ["forgot_password", "signup_link"]

navigation:
  type: "sidebar"
  logo: "Brand"
  items:
    - icon: "Home"
      label: "Dashboard"
      route: "/dashboard"
  user_menu:
    - "Profile"
    - "Logout"

screens:
  - id: dashboard
    type: "dashboard"
    widgets:
      - type: "stat_card"
        title: "Total Balance"
        value: "$12,450.00"
        trend: "+5.2%"
      - type: "chart"
        title: "Spending by Category"
        chart_type: "donut"

components_needed:
  - "DataTable"
  - "Chart"
  - "StatCard"
```

### Mobile App Schema

For mobile apps, add native features:

```yaml
onboarding:
  screens:
    - id: welcome
      visual_description: "Illustration of person using phone"
      title: "Welcome to App"
      cta: "Get Started"

navigation:
  type: "bottom-tabs"
  tabs:
    - icon: "Home"
      label: "Home"
      screen: "home"

gestures:
  - "pull_to_refresh"
  - "swipe_to_delete"

native_features:
  - "biometric_auth"
  - "push_notifications"
```

## Rules

1. **Preserve original tone** -- structure content, don't rewrite it
2. **Use Lucide icons** -- suggest appropriate icon names
3. **Mark visuals** -- use `type: "generate"` with detailed descriptions
4. **Document patterns** -- capture copywriting patterns in `copywriting_notes`
5. **Be thorough** -- capture every section, don't skip content

## Fallback

If WebFetch fails:
1. Inform user the URL could not be accessed
2. Ask them to paste a screenshot
3. Analyze the screenshot and extract content

## Next Steps

After generating copy.yaml, suggest:
- "Run extract design to create design tokens from reference images"
- "Or provide reference images for design extraction"
