# Newsletter Creation Workflow

## Objective
Research a given topic using Tavily, write compelling newsletter copy, and produce a polished HTML newsletter using brand assets.

## Required Inputs
- `topic` — The newsletter topic (provided by the user each time)
- `TAVILY_API_KEY` — Set in `.env`
- Brand assets are defined in `brand.md` and hardcoded into the generator tool

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
- Based on the research, write the newsletter sections:
  - **Headline:** Attention-grabbing, tied to the topic
  - **Intro paragraph:** Hook the reader, set context
  - **Main content:** 2-3 key sections with insights from research
  - **Key takeaway / CTA:** Clear call to action
  - **Footer:** Brand sign-off
- Match the tone: modern, confident, high-contrast (like the brand aesthetic)
- Keep it concise — scannable over dense

### Step 3: Generate the HTML Newsletter
- Run `tools/generate_newsletter.py` with the content
- The tool applies brand styling and produces a responsive HTML file
- Review the HTML output for layout and formatting issues

**Tool:** `tools/generate_newsletter.py`
**Input:** content JSON (headline, sections, CTA)
**Output:** HTML file saved to `.tmp/newsletter_<date>.html`

### Step 4: Review & Deliver
- Open the HTML output and verify:
  - Brand colors are applied correctly
  - Layout is clean on desktop and mobile
  - Links and CTA buttons work
  - No placeholder text remains
- Deliver the final HTML file path to the user

## Brand Reference
See `brand.md` in the project root for color palette and usage guidelines.

## Error Handling
- **Tavily rate limit:** Wait and retry with exponential backoff. Document the limit in this workflow once discovered.
- **Empty research results:** Try rephrasing the query. Ask the user for subtopics if needed.
- **HTML rendering issues:** Check that all CSS is inline (email compatibility). Test in browser before delivering.

## Notes
- Topic changes every run — never hardcode a topic into any tool
- All outputs are temporary in `.tmp/` — the user gets the final HTML file path
- Commit and push all new/modified files to GitHub after each run
