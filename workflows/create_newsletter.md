# Newsletter Creation Workflow

## Objective
Research a given topic using Tavily, write compelling newsletter copy, and produce a polished HTML newsletter using brand assets.

## Required Inputs
- `topic` — The newsletter topic (provided by the user each time)
- `TAVILY_API_KEY` — Set in `.env`
- Brand assets defined in `brand.md`

## Steps

### Step 1: Research the Topic
- Run `tools/research_tavily.py` with the topic
- The tool returns structured research: key facts, insights, statistics, and recent developments
- Review the research output for accuracy and relevance
- If the results are thin, re-run with a broader query or additional sub-queries

**Tool:** `tools/research_tavily.py`
**Input:** topic (string)
**Output:** Research summary saved to `.tmp/research_<sanitized_topic>.json`

### Step 2: Write the Newsletter Content
Based on the research, write the newsletter sections:
- **Headline:** Attention-grabbing, tied to the topic
- **Intro paragraph:** Hook the reader, set context
- **Main content:** 2-3 key sections with insights from research
- **Key takeaway / CTA:** Clear call to action
- **Footer:** Brand sign-off

Tone: modern, confident, high-contrast (like the brand aesthetic). Keep it concise — scannable over dense.

### Step 3: Design & Build the HTML Newsletter
The agent designs and writes the HTML directly (no template tool needed). Follow the brand design system below.

**Output:** HTML file saved to `.tmp/newsletter_<date>.html`

### Step 4: Review & Deliver
- Verify brand colors are applied correctly
- Layout is clean on desktop and mobile (max-width 600px)
- Links and CTA buttons work
- No placeholder text remains
- Deliver the final HTML file path to the user

## Brand Design System

### Color Palette
| Role | Color | Hex |
|------|-------|-----|
| Primary accent (CTAs, highlights) | Electric Lime Green | `#D4F657` |
| Background | Off-White / Cream | `#FAF9F6` |
| Headlines, primary text, dark sections | Rich Black | `#111111` |
| Body copy, subheadlines | Medium Gray | `#555555` |
| Borders, subtle dividers | Light Gray | `#E5E5E5` |

### Typography
- **Font:** Inter (Google Fonts)
- **Headline:** 28px, weight 800, color `#D4F657` on `#111111` background
- **Section titles:** 20px, weight 700, color `#111111`
- **Body:** 15px, weight 400, color `#555555`, line-height 1.7
- **Tags/labels:** 13px, weight 600, `#D4F657` on `#111111` pill

### Layout Structure
```
┌─────────────────────────────┐
│  HEADER (black bg)          │
│  Lime headline              │
│  Date / subtitle            │
├─────────────────────────────┤
│  INTRO (cream bg)           │
│  Hook paragraph             │
├─────────────────────────────┤
│  SECTION 1                  │
│  Tag pill · Title · Body    │
├─────────────────────────────┤
│  SECTION 2                  │
│  Tag pill · Title · Body    │
├─────────────────────────────┤
│  SECTION 3                  │
│  Tag pill · Title · Body    │
├─────────────────────────────┤
│  CTA (black bg)             │
│  Lime button, centered      │
├─────────────────────────────┤
│  FOOTER (black bg)          │
│  Unsubscribe / links        │
└─────────────────────────────┘
```

### Design Rules
- Max-width: 600px, centered
- All CSS must be inline or in `<style>` tag (email-compatible)
- CTA buttons: `#D4F657` bg, `#111111` text, bold, rounded 6px, generous padding
- Section dividers: 1px `#E5E5E5`
- High-contrast aesthetic: lime against black for maximum attention
- Responsive: test at 320px and 600px widths

## Error Handling
- **Tavily rate limit:** Wait and retry with exponential backoff. Document the limit in this workflow once discovered.
- **Empty research results:** Try rephrasing the query. Ask the user for subtopics if needed.
- **HTML rendering issues:** Check that all CSS is inline (email compatibility). Test in browser before delivering.

## Notes
- Topic changes every run — never hardcode a topic into any tool
- All outputs are temporary in `.tmp/` — the user gets the final HTML file path
- Commit and push all new/modified files to GitHub after each run
