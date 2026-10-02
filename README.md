# crc32.com

Source for [crc32.com](https://crc32.com): Colin Crossman's CV and contact page.
Built with [Hugo](https://gohugo.io/) (extended, ≥ 0.123). No external theme, no
JavaScript, no third-party requests.

## Where things live

| What                                   | File                         |
| -------------------------------------- | ---------------------------- |
| CV: jobs, education, licenses, writing | `data/cv.yaml`               |
| Short intro / bio                      | `data/cv.yaml` → `profile`   |
| Contact page                           | `content/contact.md`         |
| Bitcoin resources page                 | `content/btc.md`             |
| Nav menu, social links, site settings  | `hugo.toml`                  |
| Templates                              | `layouts/`                   |
| Styles (light, dark, print)            | `assets/css/main.css`        |
| PDF résumé layout                      | `layouts/_default/cv-pdf.html`, `assets/css/cv-pdf.css` |
| PDF generator (run by deploy.sh)       | `scripts/build_pdf.py`       |
| Briefs, PGP key, last-built PDF        | `static/`                    |

## Common edits

**Add an article.** Add an entry at the top of `publications` in `data/cv.yaml`:

```yaml
  - kind: article          # article | brief | scholarship | other
    title: "Title Here"
    venue: Bitcoin Magazine
    date: 2026-10-01
    url: https://bitcoinmagazine.com/...
```

The page sorts by date, so order in the file is only for readability.

**Change jobs.** Edit `experience` in `data/cv.yaml`. Leave `end:` empty for a
current role.

**The PDF résumé** (`crossman-cv.pdf`) is generated from `data/cv.yaml` on
every deploy: `scripts/build_pdf.py` prints the hidden `/cv-pdf/` page
(`layouts/_default/cv-pdf.html`, styled by `assets/css/cv-pdf.css`) to PDF with
headless Chrome. Preview the layout at <http://localhost:1313/cv-pdf/> under
`hugo server`, or build just the PDF with:

```sh
hugo --minify && uv run scripts/build_pdf.py
```

## Local preview and deploy

```sh
hugo server            # http://localhost:1313, live reload
./deploy.sh            # build site + PDF, push to ../crc32.github.io
```

The browser's "Print" on the home page produces a clean paper CV (nav, avatar,
and footer are hidden by the print stylesheet).
