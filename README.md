# Metanoia
A gamified habit tracker forged at the intersection of discipline and transformation.

## Solo Leveling DSA System
Metanoia now ships with a Solo Leveling System backend and a static frontend that generates daily DSA quests, XP totals, and streak status in the same JSON format as the backend.

### Frontend (GitHub Pages ready)
The UI lives in the `docs/` directory so it can be hosted with GitHub Pages.

**Local preview**
```bash
cd docs
python -m http.server 8000
```
Then open `http://localhost:8000`.

**Host on GitHub Pages**
1. Push this repository to GitHub.
2. In your GitHub repo, open **Settings → Pages**.
3. Under **Build and deployment**, select:
   - **Source**: Deploy from a branch
   - **Branch**: `main` (or your default branch)
   - **Folder**: `/docs`
4. Save. GitHub will provide a public URL for the site.

### Backend (CLI)
The backend generates daily quests and evaluates results.

**Generate a plan**
```bash
python -m backend.main daily
```

**Evaluate results**
```bash
python -m backend.main evaluate --date 2024-01-01 --results '[{"title":"Two Sum","difficulty":"easy","time_minutes":12,"result":"AC"}]'
```
