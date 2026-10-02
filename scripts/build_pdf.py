# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright>=1.49"]
# ///
"""Render the PDF résumé from the built Hugo site.

Run by deploy.sh after `hugo` has built ./public:

    uv run scripts/build_pdf.py

What it does:
  1. Serves ./public on a throwaway localhost port (the page uses root-relative
     URLs, so file:// would not work).
  2. Opens /cv-pdf/ (layouts/_default/cv-pdf.html) in headless Chrome and
     prints it to US Letter PDF with page numbers in the footer.
  3. Writes the PDF to public/crossman-cv.pdf (what gets deployed) and to
     static/crossman-cv.pdf (so the repo and `hugo server` stay current).
  4. Deletes public/cv-pdf/ so the print-only page never ships.

Browser: uses $CHROME_PATH if set, else your installed Google Chrome, else
Playwright's own Chromium. If none is found, install one with:

    uv run --with playwright playwright install chromium
"""

from __future__ import annotations

import argparse
import functools
import http.server
import shutil
import sys
import threading
from pathlib import Path

from playwright.sync_api import Browser, Playwright, sync_playwright

# Repo root = parent of scripts/.
ROOT = Path(__file__).resolve().parent.parent

# Page-number footer. Chrome fills in the .pageNumber/.totalPages spans.
# Footer templates don't inherit page CSS, so styles must be inline.
FOOTER = """
<div style="width:100%; font: 7.5pt Helvetica, Arial, sans-serif; color:#8a857c;
            padding: 0 0.6in; display:flex; justify-content:space-between;">
  <span>Colin Crossman · CV · crc32.com</span>
  <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
</div>
"""


def serve(directory: Path) -> http.server.ThreadingHTTPServer:
    """Start a quiet static file server for `directory` on a free port."""

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args) -> None:  # silence per-request logging
            pass

    handler = functools.partial(QuietHandler, directory=str(directory))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def launch(pw: Playwright, chrome_path: str | None) -> Browser:
    """Launch the first browser that works: explicit path, Chrome, Chromium."""
    attempts = []
    if chrome_path:
        attempts.append(("CHROME_PATH", {"executable_path": chrome_path}))
    attempts.append(("Google Chrome", {"channel": "chrome"}))
    attempts.append(("Playwright Chromium", {}))

    errors = []
    for label, kwargs in attempts:
        try:
            browser = pw.chromium.launch(**kwargs)
            print(f"  using {label}")
            return browser
        except Exception as exc:  # noqa: BLE001 - try the next option
            errors.append(f"{label}: {str(exc).splitlines()[0]}")
    sys.exit(
        "No usable Chrome/Chromium found.\n  "
        + "\n  ".join(errors)
        + "\nInstall one with: uv run --with playwright playwright install chromium"
    )


def main() -> None:
    import os

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--public", type=Path, default=ROOT / "public",
                        help="Hugo output directory (default: ./public)")
    parser.add_argument("--name", default="crossman-cv.pdf",
                        help="PDF filename (default: crossman-cv.pdf)")
    parser.add_argument("--no-static", action="store_true",
                        help="don't copy the PDF into static/")
    args = parser.parse_args()

    public: Path = args.public.resolve()
    page_dir = public / "cv-pdf"
    if not (page_dir / "index.html").exists():
        sys.exit(f"{page_dir}/index.html not found; run `hugo` first.")

    out = public / args.name
    server = serve(public)
    url = f"http://127.0.0.1:{server.server_address[1]}/cv-pdf/"

    try:
        with sync_playwright() as pw:
            browser = launch(pw, os.environ.get("CHROME_PATH"))
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            page.emulate_media(media="print")
            page.pdf(
                path=str(out),
                format="Letter",
                margin={"top": "0.55in", "bottom": "0.6in",
                        "left": "0.6in", "right": "0.6in"},
                print_background=True,
                display_header_footer=True,
                header_template="<span></span>",  # empty, but required
                footer_template=FOOTER,
                tagged=True,   # accessible (tagged) PDF
                outline=True,  # bookmarks from the h2/h3 headings
            )
            browser.close()
    finally:
        server.shutdown()

    # The print-only page has done its job; keep it off the live site.
    shutil.rmtree(page_dir)

    if not args.no_static:
        shutil.copyfile(out, ROOT / "static" / args.name)

    print(f"  wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}"
          f" ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
