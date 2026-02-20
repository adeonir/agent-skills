# Design Export

Send variants to Figma for refinement and mockups.

## When to Use

- User wants to send a variant to Figma for refinement
- User says "send to Figma", "export to Figma", "export design"

## Process

### Step 1: Verify Figma MCP

Check if the `figma-dev-mode-mcp-server` MCP is configured. If not, instruct the user:

1. Open Figma desktop app
2. Toggle to Dev Mode (Shift+D)
3. Enable "Desktop MCP server" in the inspect panel
4. Run: `claude mcp add --transport sse figma-dev-mode-mcp-server http://127.0.0.1:3845/sse`

Do not proceed until MCP is confirmed available.

### Step 2: Select Variants

Locate variants at `.specs/docs/{project-name}/variants/`. Ask the user which variants to send -- one, some, or all.

If no variants exist, suggest running generate variants first.

### Step 3: Send to Figma

For each selected variant:

1. Serve locally: `npx http-server .specs/docs/{project-name}/variants/{variant} -o -p 8081`
2. Confirm the page is rendering in the browser
3. Send to Figma via MCP -- each variant becomes a separate editable frame

The MCP captures the live browser state as editable frames -- not screenshots. Layout structure, typography, colors, and spacing are preserved as Figma layers.

## Rules

1. **Always verify MCP first** -- never skip the connection check
2. **User confirms visually** -- each page must be reviewed in browser before sending

## Error Handling

- **MCP not configured**: Provide setup instructions (Step 1)
- **No variants found**: Suggest running generate variants
- **Port 8081 in use**: Suggest an alternative port
- **MCP connection fails**: Confirm Figma desktop is open with Dev Mode active
