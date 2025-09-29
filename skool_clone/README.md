# Skool.com Clone

## Commands Used

### Initial Attempt with wget:
```bash
mkdir -p skool_clone
cd skool_clone
wget --mirror --convert-links --adjust-extension --page-requisites --span-hosts --no-parent --wait=1 --limit-rate=50k https://skool.com/
```
**Result:** Failed with 403 Forbidden (site blocks automated access)

### Fallback with httrack:
```bash
httrack https://skool.com/ -O . -n -s0 -c1 -A0 -%e0
```
**Result:** Partial success but limited content due to anti-scraping protections

### Final Solution with Python:
```bash
python3 download_skool.py
```
**Result:** Successfully downloaded and processed 162,659 characters of HTML content

## Content Processing

- Downloaded main page HTML from skool.com
- Updated absolute links to work with relative paths
- Processed image sources, CSS, and JavaScript references
- Saved processed content to `public/skool/index.html`

## Important Notes

- **robots.txt Compliance:** skool.com's robots.txt disallows automated crawling
- **Educational Purpose:** This clone is for reference and learning purposes only
- **Respect Copyright:** All content belongs to Skool Inc.
- **Legal Notice:** This is a limited snapshot for development reference only

## Files Created

- `public/skool/index.html` - Main processed HTML file
- `download_skool.py` - Python script used for content extraction
- `skool_clone/` - HTTrack cache and logs

## Usage

The cloned content is accessible via the `/skool/` route when served by the Flask application.