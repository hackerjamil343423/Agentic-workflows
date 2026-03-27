"""
Newsletter HTML generator.
Takes structured content and produces a styled HTML newsletter using brand assets.

Usage:
    python tools/generate_newsletter.py --headline "Title" --intro "..." --sections '...' --cta "..." --cta-url "..."
    python tools/generate_newsletter.py --input .tmp/content_<topic>.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

TMP_DIR = Path(__file__).resolve().parent.parent / ".tmp"
TMP_DIR.mkdir(exist_ok=True)

# Brand colors from brand.md
BRAND = {
    "lime": "#D4F657",
    "cream": "#FAF9F6",
    "black": "#111111",
    "gray": "#555555",
    "light_gray": "#E5E5E5",
    "lime_hover": "#C5E84E",
}

NEWSLETTER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{headline}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'Inter', Arial, Helvetica, sans-serif;
    background-color: {cream};
    color: {black};
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }}

  .wrapper {{
    max-width: 600px;
    margin: 0 auto;
    background-color: {cream};
  }}

  /* Header */
  .header {{
    background-color: {black};
    padding: 40px 32px;
    text-align: center;
  }}

  .header h1 {{
    color: {lime};
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    line-height: 1.3;
  }}

  .header .date {{
    color: {light_gray};
    font-size: 13px;
    margin-top: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}

  /* Intro */
  .intro {{
    padding: 32px;
    font-size: 16px;
    color: {gray};
    border-bottom: 1px solid {light_gray};
  }}

  /* Content sections */
  .section {{
    padding: 28px 32px;
    border-bottom: 1px solid {light_gray};
  }}

  .section h2 {{
    font-size: 20px;
    font-weight: 700;
    color: {black};
    margin-bottom: 12px;
    letter-spacing: -0.3px;
  }}

  .section p {{
    font-size: 15px;
    color: {gray};
    line-height: 1.7;
  }}

  .section .highlight {{
    background-color: {black};
    color: {lime};
    padding: 2px 8px;
    border-radius: 3px;
    font-weight: 600;
    font-size: 13px;
    display: inline-block;
    margin-bottom: 8px;
  }}

  /* CTA */
  .cta-section {{
    padding: 40px 32px;
    text-align: center;
    background-color: {black};
  }}

  .cta-section p {{
    color: {light_gray};
    font-size: 15px;
    margin-bottom: 24px;
  }}

  .cta-button {{
    display: inline-block;
    background-color: {lime};
    color: {black};
    text-decoration: none;
    padding: 14px 36px;
    font-size: 16px;
    font-weight: 700;
    border-radius: 6px;
    letter-spacing: 0.3px;
  }}

  .cta-button:hover {{
    background-color: {lime_hover};
  }}

  /* Footer */
  .footer {{
    padding: 24px 32px;
    text-align: center;
    background-color: {black};
    border-top: 1px solid #222;
  }}

  .footer p {{
    color: #666;
    font-size: 12px;
    line-height: 1.5;
  }}

  .footer a {{
    color: {lime};
    text-decoration: none;
  }}
</style>
</head>
<body>
<div class="wrapper">

  <div class="header">
    <h1>{headline}</h1>
    <div class="date">{date}</div>
  </div>

  <div class="intro">
    {intro}
  </div>

  {sections_html}

  <div class="cta-section">
    <p>{cta_text}</p>
    <a href="{cta_url}" class="cta-button">{cta_button}</a>
  </div>

  <div class="footer">
    <p>You're receiving this because you subscribed.<br>
    <a href="{{unsubscribe_url}}">Unsubscribe</a> · <a href="{{preferences_url}}">Preferences</a></p>
  </div>

</div>
</body>
</html>"""

SECTION_TEMPLATE = """
  <div class="section">
    <span class="highlight">{tag}</span>
    <h2>{title}</h2>
    <p>{content}</p>
  </div>
"""


def generate_newsletter(
    headline: str,
    intro: str,
    sections: list[dict],
    cta_text: str = "Ready to take the next step?",
    cta_button: str = "Learn More",
    cta_url: str = "#",
) -> str:
    """Generate styled HTML newsletter from content."""

    date_str = datetime.now().strftime("%B %d, %Y")
    sections_html = ""

    for sec in sections:
        sections_html += SECTION_TEMPLATE.format(
            tag=sec.get("tag", "INSIGHT"),
            title=sec.get("title", ""),
            content=sec.get("content", ""),
        )

    html = NEWSLETTER_TEMPLATE.format(
        headline=headline,
        date=date_str,
        intro=intro,
        sections_html=sections_html,
        cta_text=cta_text,
        cta_button=cta_button,
        cta_url=cta_url,
        **BRAND,
    )

    # Save to .tmp
    filename = f"newsletter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = TMP_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Newsletter saved to {filepath}")
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate newsletter HTML")
    parser.add_argument("--input", help="Path to content JSON file")
    parser.add_argument("--headline", help="Newsletter headline")
    parser.add_argument("--intro", help="Intro paragraph")
    parser.add_argument("--sections", help="Sections as JSON string")
    parser.add_argument("--cta-text", default="Ready to take the next step?")
    parser.add_argument("--cta-button", default="Learn More")
    parser.add_argument("--cta-url", default="#")
    args = parser.parse_args()

    if args.input:
        with open(args.input, encoding="utf-8") as f:
            data = json.load(f)
        generate_newsletter(
            headline=data["headline"],
            intro=data["intro"],
            sections=data["sections"],
            cta_text=data.get("cta_text", args.cta_text),
            cta_button=data.get("cta_button", args.cta_button),
            cta_url=data.get("cta_url", args.cta_url),
        )
    elif args.headline:
        sections = json.loads(args.sections) if args.sections else []
        generate_newsletter(
            headline=args.headline,
            intro=args.intro or "",
            sections=sections,
            cta_text=args.cta_text,
            cta_button=args.cta_button,
            cta_url=args.cta_url,
        )
    else:
        print("Provide --input or --headline. Run with --help for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
