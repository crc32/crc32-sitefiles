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
| PDF résumé, briefs, PGP key            | `static/`                    |

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

**Update the PDF.** Replace `static/crossman-cv.pdf`.

## Local preview and deploy

```sh
hugo server            # http://localhost:1313, live reload
./deploy.sh            # build + push to ../crc32.github.io
```

The browser's "Print" on the home page produces a clean paper CV (nav, avatar,
and footer are hidden by the print stylesheet).
