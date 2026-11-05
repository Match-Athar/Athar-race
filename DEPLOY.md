# Deploying the MATCH race board on GitHub Pages

The board builds itself from the **live Odoo API** plus the reference workbook and
publishes with GitHub Pages. No daily upload — once it's set up it refreshes on its own.

- Sales, transactions, staff and last-year come from the Odoo BI API (tax-included).
- Targets, the daily curve, prize ceilings, names, area managers and footfall come from
  `data/master.xlsx` (committed to the repo).
- Workflow: [`.github/workflows/publish.yml`](.github/workflows/publish.yml).

## What gets published

| Page | Published? | Contains |
|---|---|---|
| `index.html` — race board | ✅ yes | percentages, ranks, employee names |
| `public.html` — public board | ✅ yes | percentages and names, no amounts |
| `internal.html` — amounts | ❌ never | kept out of the build (`--public-only`) |

The published page is reachable by **anyone with the link**. Keep the repository
**private** (the reference workbook holds sales amounts), and confirm name-display consent.

> Publishing Pages from a **private** repo needs a paid GitHub plan (Pro / Team / Enterprise).
> On a free plan, keep the repo private and host the built `site/` folder elsewhere (e.g. Netlify).

## One-time setup

### 1. Push the project to a new private repo

```bash
git init
git add .
git commit -m "MATCH race board"
git branch -M main
git remote add origin https://github.com/<account>/<repo>.git
git push -u origin main
```

`.env` and `github-token.txt` are git-ignored, so your API token is **not** pushed.
`data/master.xlsx` **is** pushed (the build needs it) — that's why the repo must be private.

### 2. Add the API secrets

Repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Value |
|---|---|
| `ODOO_API_URL` | `https://matchperfume.odoo.com/api/bi/v1/pos/sales/detail` |
| `ODOO_API_TOKEN` | your production bearer token |
| `ODOO_TZ` | optional — `Asia/Riyadh` (default) or `Asia/Dubai` |

The full `/api/bi/v1/pos/sales/detail` path is required — the host alone returns HTML, not JSON.

### 3. Turn on Pages

Repo → **Settings → Pages → Source → GitHub Actions**.

### 4. Build it

The workflow runs automatically on every push and **every 10 minutes**. To run it now:
**Actions → Publish Athar board → Run workflow**. About a minute later the board is live at:

```
https://<account>.github.io/<repo>/
```

Send that link to the branches once; it updates itself.

## Months, the dropdown and the winners page

The board builds **one page with a month dropdown**, driven by `data/months.json`:

```json
{
  "default": "2026-11",           // which month the dropdown opens on
  "winners_from": "2026-11-10",   // October's winners page appears on/after this date
  "months": [
    { "ym": "2026-11", "ref": "data/master-2026-11.xlsx" },
    { "ym": "2026-10", "ref": "data/master-2026-10.xlsx", "winners": true }
  ]
}
```

- Each month has its **own workbook** (`data/master-YYYY-MM.xlsx`) with that month's targets, ceilings, curve.
- Sales for every month come from the live API for that month's date range.
- A month marked `"winners": true` shows a **prize-winners page** (car + each phone/iPad/watch/gold seat: branch + its top employee) **instead of** its race board, but only on/after `winners_from`. Before that date, selecting it shows its normal race board.
- The countdown and all labels follow the selected month automatically — **no code edit needed** for a new month.

### Previewing the winners page early (management cross-check)

Before the public `winners_from` date, add `?preview` to the URL to unlock the winners
page for internal review, with `?m=YYYY-MM` to open a specific month. A gold banner marks
it as "not public yet"; the public link (no `?preview`) still shows the race board until
the date. Example:

```
https://<account>.github.io/<repo>/?preview&m=2026-10
```

### Adding a new month
1. Add its workbook, e.g. `data/master-2026-12.xlsx`.
2. Add a line to `data/months.json` (and set `"default"` / `"winners"` as you want).
3. Push. The `data/**` path triggers a rebuild.

> November uses the full **"MATCH Sales Dashboard November 2026"** master
> (`data/master-2026-11.xlsx`): 116 branches, real targets, the 30-day curve, prize ceilings
> (all five tiers), area managers, footfall and last-year. Live sales/staff come from the Odoo
> API; the master supplies everything else. Replace this file with an updated export to refresh
> the plan.

## Notes

- **Actions minutes:** the 10-minute schedule is ~144 builds/day; each build pulls the
  month-to-date plus the same period last year. On a private repo that consumes paid-plan
  minutes — widen the `cron` in `publish.yml` (e.g. `*/30`) if you want to spend less.
- **Date range:** each build pulls from the 1st of the month to today. Today's sales count
  in totals; the pace/projection uses finished days only.
- **Local test before pushing:**

  ```bash
  python run.py --api --ref data/master.xlsx --out site
  ```

  Then open `site/index.html`. (`.env` supplies the URL and token locally.)
- **Branches with sales but no target** are printed as a warning at build time; add a target
  row in `data/master.xlsx` or an `EXCLUDE` entry in `athar/config.py` to clear them.
