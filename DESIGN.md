---
name: ManjoDB
description: "Relationships, first. A graph-native database identity drawn in commit-lane notation."
colors:
  lane-pink: "#FF4FA0"
  lane-pink-bright: "#FF74B4"
  lane-lilac: "#B98CFF"
  lane-pink-ink: "#D81B73"
  lane-violet-ink: "#6E3AD9"
  plum: "#2B0D3F"
  plum-deep: "#1E0830"
  vertex: "#F7EEFF"
  on-plum-muted: "#CDB8E6"
  plum-line: "rgba(247, 238, 255, .09)"
  plum-hairline: "rgba(247, 238, 255, .16)"
  paper: "#FBF7FF"
  white: "#FFFFFF"
  ink: "#1C0E2A"
  on-paper-muted: "#5E4A70"
  paper-line: "rgba(28, 14, 42, .10)"
typography:
  display:
    fontFamily: "Lexend, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(36px, 5vw, 64px)"
    fontWeight: 500
    lineHeight: 1.02
    letterSpacing: "-0.03em"
  title:
    fontFamily: "Lexend, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(18px, 1.6vw, 21px)"
    fontWeight: 400
    lineHeight: 1.6
  body:
    fontFamily: "Lexend, ui-sans-serif, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: "Lexend, ui-sans-serif, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.6
  button:
    fontFamily: "Lexend, ui-sans-serif, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 500
    lineHeight: 1
  code:
    fontFamily: "JetBrains Mono, ui-monospace, Cascadia Code, monospace"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.75
  label:
    fontFamily: "JetBrains Mono, ui-monospace, Cascadia Code, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.3
rounded:
  pill: "999px"
  panel: "20px"
  card: "18px"
  frame: "16px"
spacing:
  gap: "16px"
  lede: "24px"
  stack: "40px"
  block: "56px"
  gutter: "clamp(16px, 4vw, 56px)"
  band: "clamp(72px, 10vw, 140px)"
  lane: "calc(min(1240px, 100cqw) / 12)"
components:
  button-primary:
    backgroundColor: "{colors.lane-pink}"
    textColor: "{colors.plum-deep}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "0 22px"
    height: "48px"
  button-primary-hover:
    backgroundColor: "{colors.lane-pink-bright}"
    textColor: "{colors.plum-deep}"
  button-quiet:
    textColor: "{colors.vertex}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "0 22px"
    height: "48px"
  nav-link:
    textColor: "{colors.on-plum-muted}"
    typography: "{typography.body-sm}"
    padding: "6px 0"
  nav-link-hover:
    textColor: "{colors.vertex}"
  figure-on-plum:
    backgroundColor: "{colors.plum-deep}"
    rounded: "{rounded.panel}"
    padding: "clamp(24px, 4vw, 48px)"
  figure-on-paper:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.panel}"
    padding: "clamp(24px, 4vw, 48px)"
  code-block:
    backgroundColor: "{colors.plum-deep}"
    textColor: "{colors.vertex}"
    typography: "{typography.code}"
    rounded: "{rounded.panel}"
    padding: "28px 32px"
  card-on-paper:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "24px"
  table-header:
    textColor: "{colors.on-plum-muted}"
    typography: "{typography.label}"
    padding: "12px 14px 12px 0"
  file-link:
    textColor: "{colors.lane-pink}"
    padding: "8px 0"
---

# Design System: ManjoDB

## Overview

**Creative North Star: "Commit Lanes"**

ManjoDB is drawn in the graph notation developers already read every day: the lanes of `git log --graph`. Two rails, one branch, a commit and a merge make an M, and the same notation draws every diagram the product will ever show. The system refuses the category default, a node-network hexagon in a purple gradient. It reads as precise and engineering-serious: a small number of materials, used with discipline.

The world is built from full-width bands of ground, deep plum or lilac-tinted paper, each carrying a faint vertical lane grid registered to the content wrap. On those grounds everything is achromatic except the edges. Lanes and relationships carry the only color (pink for the relationship, lilac or violet for structure); vertices, headlines, body copy and grounds stay plum, ink, vertex white or paper. Every stroke is monoline with round caps, from the mark to the wordmark to the diagram lanes.

Density is calm and editorial: generous band padding, short headlines held to 16 characters a line, ledes held to 62 characters, and mono type reserved for anything a machine reads. There is one authored motion: the mark prints itself row by row, the way a graph log scrolls into a terminal, and then holds still.

**Key Characteristics:**
- Color lives only on edges, plus one pink active state; vertices and type stay achromatic.
- Full-width plum and paper bands; a band never changes ground partway through.
- A 12-column lane grid, registered to the 1240px wrap, on every band.
- Lexend for people, JetBrains Mono for machines.
- A drawn monoline wordmark, never typeset.
- One motion: the print-in.

## Colors

A plum and paper world in which pink and violet are reserved for relationships, so color always means "edge".

### Primary
- **Lane Pink** (#FF4FA0): the branch on plum. In the mark it is the one colored path; in diagrams it is the matched relationship, the evidence edge; in MQL text it marks relationship names (`DEPENDS_ON`, `OWNS`). It is also the single active state on plum: primary action fill, focus ring, text selection, download links. 5.58:1 on plum.
- **Lane Pink, Bright** (#FF74B4): hover state of the primary action only.
- **Lane Pink, Deep** (#D81B73): the branch on white and paper. 4.86:1 on white, 4.59:1 on paper.

### Secondary
- **Lane Lilac** (#B98CFF): rails on plum, the structural lanes of the mark and of diagrams. In diagrams, context rails drop to 55% opacity so the pink answer path leads. 6.7:1 on plum.
- **Lane Violet, Deep** (#6E3AD9): rails on white and paper. 6.42:1 on white.

### Neutral
- **Plum** (#2B0D3F): the dark ground. Owns whole bands, the app icon tile and the favicon tile.
- **Plum, Deep** (#1E0830): recessed panels on plum (figures, code blocks), the footer, and text on pink or lilac fills.
- **Vertex White** (#F7EEFF): vertices on plum, the reverse wordmark, and all primary text on plum. `build_logo.py` names this constant `PAPER`; on the page it is the vertex color, not the paper ground.
- **On-Plum Muted** (#CDB8E6): ledes, notes, nav links, table headers and MQL keywords on plum.
- **Plum Line** (rgba(247, 238, 255, .09)): the lane grid on plum, and table rules.
- **Plum Hairline** (rgba(247, 238, 255, .16)): list row dividers and thumbnail outlines on plum.
- **Paper** (#FBF7FF): the light ground for docs bands.
- **White** (#FFFFFF): lifted panels on paper (figures, tiles, cards, mock browser chrome). The deep lane inks are tuned against it.
- **Ink** (#1C0E2A): vertices, the light wordmark and all primary text on paper and white.
- **On-Paper Muted** (#5E4A70): ledes, notes, captions and diagram labels on paper.
- **Paper Line** (rgba(28, 14, 42, .10)): the lane grid on paper.

### Named Rules
**The Edges Only Rule.** Color marks an edge and nothing else: a lane, a relationship path, a relationship name in query text, a graph edge in terminal output. Vertices, headlines, body text and grounds are always achromatic. The one sanctioned extension is the active state: Lane Pink fills the primary action and draws focus, selection and download links, because an action is the path you take next.

**The Two Inks Rule.** Every lane color comes as a pair: bright on plum (Lane Pink, Lane Lilac), deep on paper and white (Lane Pink Deep, Lane Violet Deep), so every edge holds at least 4.5:1 against its ground. Never put the bright pair on paper or the deep pair on plum.

**The Never Alone Rule.** Color never carries meaning by itself. Every colored edge in a diagram is also named or numbered (edge IDs 81 and 84, the label `OWNS`), and every legend key pairs its swatch with a word.

## Typography

**Display Font:** Lexend (with ui-sans-serif, system-ui, sans-serif)
**Body Font:** Lexend (with ui-sans-serif, system-ui, sans-serif)
**Label/Mono Font:** JetBrains Mono (with ui-monospace, Cascadia Code, monospace)

**Character:** Lexend's open, even geometry sits close to the drawn monoline wordmark without imitating it; JetBrains Mono carries everything a terminal would print. Weights stay low: 400 for reading, 500 for headlines and actions, 600 only for a name in a compact row.

### Hierarchy
- **Display** (500, clamp(36px, 5vw, 64px), 1.02, -0.03em): one section headline per band, balanced wrap, held to 16ch. Headlines are short declarative sentences ending in a period ("Color lives on the edges.").
- **Title** (400, clamp(18px, 1.6vw, 21px), 1.6): the lede under each headline, in the muted text color, 24px below it.
- **Body** (400, 17px, 1.6; 16px below 560px): running text, held to 62ch with pretty wrapping.
- **Body Small** (400, 15px, 1.6): notes, captions, nav links, table text, card copy.
- **Code** (400, 14px, 1.75): MQL listings, terminal output, file paths, legend terms. Ligatures off and tabular figures on for inline code and numbers.
- **Label** (400, 13px, 1.3): file-name captions, mock window titles; table column headers step up to 500 in the muted color.

The hero tagline ("Relationships, first.") is set once, at 500 and clamp(28px, 3.4vw, 46px) with -0.03em tracking, beneath the wordmark.

### Named Rules
**The Drawn Name Rule.** The name is never typeset. Wherever "manjodb" appears as a brand (top bar, hero, footer, docs header) it is a wordmark or lockup file; the page's h1 is the wordmark image with alt text "ManjoDB". In running prose, the product is written "ManjoDB".

**The Mono Means Machine Rule.** JetBrains Mono is for what a machine reads or writes: queries, commands, paths, IDs, table cells, diagram vertex and edge labels. Everything a person reads is Lexend.

## Layout

Every band is full-bleed and carries the lane grid: twelve equal lanes registered to the content wrap (1240px maximum, with a fluid gutter of clamp(16px, 4vw, 56px)). Line 0 is the wrap's left edge; line 12 is its right edge; the 1px lines continue past the wrap to the band edges at the same pitch, in Plum Line on plum and Paper Line on paper. The grid is behind everything and never takes pointer events.

Layouts are built on the same 12 lanes, with no column gaps, so content edges land on lane lines. Two-part sections split 5 + 6 lanes with one lane of air (columns 1-5 and 7-12), or 7 + 5 when the left side carries a listing. File rows use the 12-lane grid directly. Card grids (swatches, lockup tiles, don't cards) use a 16px gap in 4 or 6 columns.

When the mark appears larger than a lockup, its view box is cropped to the rails (x 10 to 46) and it spans an even number of lanes, so the left rail, the middle lane and the right rail each sit on a lane line. At poster scale on wide screens the rails run past the top and bottom edges of the band; below 960px they are cut back to the mark's own frame.

Vertical rhythm: bands pad clamp(72px, 10vw, 140px) top and bottom; headline to lede 24px; lede to the next block 56px; inner stacks 40px. Below 960px all splits collapse to a single column and the lockup tiles and don't cards drop to two columns; below 560px the don't cards go single-column and the swatches drop from four columns to two.

### Named Rules
**The Registered Lanes Rule.** Nothing floats off the grid. Every band shows the lane grid, the content wrap spans lines 0 to 12, and splits, file rows and the large mark's rails start on lane lines; card grids fill the wrap with a 16px gap.

## Elevation & Depth

Depth is tonal on plum and lightly lifted on paper. On plum nothing casts a shadow: a recessed panel is Plum Deep set into Plum, and a framed tile uses a 1px vertex-white border at 14% opacity. On paper, white panels and tiles lift with one plum-tinted ambient shadow; the don't cards use only its tight contact layer.

### Shadow Vocabulary
- **Paper Lift** (`box-shadow: 0 1px 2px rgba(28, 14, 42, .06), 0 12px 32px -12px rgba(28, 14, 42, .18)`): white figures and lockup tiles on paper.
- **Paper Rest** (`box-shadow: 0 1px 2px rgba(28, 14, 42, .06)`): white cards that sit flatter, such as the misuse cards.

### Named Rules
**The Plum Is Flat Rule.** No shadow ever falls on plum. Depth there is a darker plum, not a shadow.

## Shapes

The form language is the stroke. Every line is monoline with round caps: the mark at 5.5 units, the wordmark at 9, diagram lanes at 7. Lanes are vertical and history reads top to bottom. Vertices are open rings that knock a gap out of the lanes beneath them (solid achromatic dots only in the favicon, where rings would close up); they are never colored.

Containers are soft rectangles with generous radii: 20px for figures, code blocks and lockup tiles; 18px for swatches and cards; 16px for mock product frames (terminal, browser, package row). Actions and inline labels are full pills (999px). Icon tiles (app icon and favicon) are plum squares with corners at about 22% of their side (112 on 512, 14 on 64).

## Components

### Buttons
Calm, round and unmistakable: one pink pill, one outlined pill.
- **Shape:** full pill (999px), at least 48px tall, 22px side padding, Lexend 500 at 16px.
- **Primary:** Lane Pink fill with Plum Deep text (6.07:1). One per view.
- **Hover / Focus:** fill shifts to Lane Pink Bright over 0.2s ease; focus draws a 2px Lane Pink outline offset 3px, the same ring used site-wide.
- **Quiet:** no fill, a 1px vertex-white border at 35% opacity, Vertex White text; on hover the border goes to full Vertex White.

### Navigation
- **Top bar:** sits over the first band, inset to the wrap edges, with the reverse lockup 30px tall at left and section links at right in Body Small, On-Plum Muted, turning Vertex White on hover. A skip link (a primary pill) appears on focus.
- **Mobile:** the build hides the section links below 560px with nothing in their place. Treat that as an open gap, not the pattern.

### Figures and Code Blocks
- **Figure on plum:** Plum Deep panel, 20px radius, clamp(24px, 4vw, 48px) padding, no shadow.
- **Figure on paper:** white panel, same radius and padding, Paper Lift shadow.
- **MQL code block:** Plum Deep panel, 20px radius, 28px 32px padding (22px 20px below 560px), Code type in Vertex White. Keywords (`find`, `where`, `follow`, `through`, `from`, `show`, `take`) are On-Plum Muted; relationship names and bindings (`link: DEPENDS_ON`, `OWNS`) are Lane Pink. Nothing else in the listing is colored.

### Tables
Results tables set every cell in mono with tabular figures, 15px, left-aligned, separated by 1px Plum Line rules. Column headers are Label type at 500 in On-Plum Muted. A table that shows example data is labeled "Synthetic example data" in mono directly above it.

### File List
Rows on plum on the 12-lane grid: a thumbnail tile (the asset on its intended ground, outlined by Plum Hairline), the asset name in Lexend 500, its path in mono On-Plum Muted, and a right-aligned "Download" link in Lexend 500, Lane Pink, that underlines on hover. Rows are divided by Plum Hairline rules.

### The Mark
The signature component, generated with every other logo file from one geometry by `brand/build_logo.py`. Change the geometry there, never by hand.
- **Grid:** 56 by 64 units. Lanes at x = 10, 28 and 46 (an 18-unit pitch). Rails run on lanes 1 and 3 from y = 7 to y = 57.
- **Branch:** one path leaves the rail at (10, 18), curves down to the commit at (28, 45) on the middle lane, and rises to merge into the right rail at (46, 18).
- **Vertices:** branch (10, 18), commit (28, 45), merge (46, 18). Open rings of radius 4.1 and stroke 2.8, each knocking out the lanes beneath to radius 5.1.
- **Stroke:** 5.5 units, round caps. Rails take the lilac or violet ink, the branch the pink ink, vertices the achromatic ink of their ground.
- **Variants:** light (Ink vertices, deep inks, for white and paper); reverse (Vertex White vertices, bright inks, for plum); one-color (`currentColor` throughout; inline the SVG so the color inherits); favicon (5.5 becomes 7.5 stroke, solid Vertex White vertices of radius 4.6, knockout 5.9, mark at 0.8 scale on a 64 plum tile); app icon (reverse mark at 6x on a 512 plum tile).
- **Clear space:** one lane (18 units) on every side.
- **Minimum size:** the mark at 24px tall; the lockup at 136px wide, where its mark reaches 24px. Below 24px, use the favicon file.

### The Wordmark and Lockup
- **Wordmark:** "manjodb" in lowercase, drawn as one monoline path at stroke 9 with round caps and joins. x-height runs from 50 to 100, ascenders to 20, the j's descender to 125. Bowls are circles of radius 25; the m's arches are radius 16 and the n's radius 20. The d and b stems run ascender to baseline, like the rails. The j's dot is a commit ring (radius 6, stroke 5.5).
- **Lockup:** the mark at 1.6x scale beside the wordmark, its rails running exactly from ascender (20) to baseline (100) so the rails and the d and b stems share height; at that scale the mark's 5.5 stroke becomes 8.8, matching the wordmark's 9.

### Lane Diagrams
Every diagram in docs and tools uses the mark's notation: vertices are open rings in the achromatic ink of the ground, relationships are round-capped vertical lanes and curves, and each ring knocks a gap out of the lanes it sits on. Context rails are Lane Lilac at 55% opacity; the answer path is Lane Pink at full strength. Vertex labels are mono in Vertex White (or Ink on paper); edge labels (IDs and relationship types) are smaller mono in the muted color. Every diagram draws a real query and its result, read top to bottom, and ships beside the query text and a caption that states the path in words. The same notation appears in terminal output as an ASCII graph with pink edges and dim metadata.

### The Print-In
The one authored motion. On load the mark reveals top to bottom in 14 discrete steps over 1.25s (a clip-path wipe after a 0.15s delay), like lines of `git log --graph` arriving in a terminal; each vertex ring then scales up from 20% and fades in over 0.5s on cubic-bezier(.16, 1, .3, 1), in the order branch (0.45s), merge (0.7s), commit (0.95s). It runs only when the visitor has not asked for reduced motion; otherwise the mark simply appears. Everything else moves only as a 0.2s ease state transition.

## Do's and Don'ts

### Do:
- **Do** reserve color for edges: lanes, relationship paths, relationship names in queries, and the single pink active state.
- **Do** switch lane inks with the ground: #FF4FA0 and #B98CFF on plum, #D81B73 and #6E3AD9 on white or paper.
- **Do** keep vertices open rings in Ink or Vertex White, knocking a gap out of the lanes beneath them; only the favicon uses solid vertices.
- **Do** register every layout to the 12-lane grid on the 1240px wrap, and show the grid on every band.
- **Do** use the generated files from `brand/build_logo.py`, and change geometry only in that script.
- **Do** give the mark one lane (18 units) of clear space, keep it at 24px tall or larger, and switch to the favicon below 24px.
- **Do** draw every diagram from a real query and its result, labeled as synthetic when the data is.
- **Do** name or number every colored edge so meaning never depends on color alone.

### Don't:
- **Don't** color a vertex. Color belongs to edges only.
- **Don't** add a gradient. Lanes are flat, one color each.
- **Don't** rotate the mark. Lanes run vertically; history reads top to bottom.
- **Don't** retype the wordmark in a font. Use the drawn files.
- **Don't** put a shadow on plum; recess with Plum Deep instead.
- **Don't** add a second authored motion, or play the print-in for visitors who prefer reduced motion.
- **Don't** set headlines, body text or a band ground in a lane color.
- **Don't** reach for a node-network hexagon or a purple gradient; that is the category default this identity refuses.
