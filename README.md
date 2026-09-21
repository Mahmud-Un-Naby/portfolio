# Mahmud Un Naby — Portfolio

Personal portfolio of Mahmud Un Naby, competitive programmer and Computer Science and Engineering student at Mawlana Bhashani Science and Technology University.

Live site: https://mahmud-un-naby.github.io/portfolio/

Built with HTML, CSS, and JavaScript. Hosted on GitHub Pages from the root of the main branch.

To preview locally, run `python3 -m http.server 8000` and visit http://localhost:8000. No build step is required.

This repository contains the portfolio website only. Featured projects are presented through descriptions and public demos when available.

## Update profile and résumé

Confirmed public details live in `data/profile.json`. Update them as new information arrives, then run:

```sh
python3 scripts/build-profile.py
python3 scripts/export-resume.py
```

The first command rebuilds `resume.html` and the shared portfolio skills, contest results, and contact sections. The second needs Chrome or Chromium and exports `assets/documents/Mahmud-Un-Naby-Resume.pdf` with hyperlinks. Check the PDF after substantial content changes; its layout is designed for one A4 page.

Commit the data, generated HTML/PDF, and any accompanying changes, then push `main` to publish. Do not edit generated sections by hand. Other portfolio copy and project cards remain in `index.html`; keep them aligned when changing the corresponding profile facts.

Local intake notes (`CONTENT.md`, `LOCAL_NOTES.md`) and original PNG photos are ignored by Git. They remain available for future edits without being published.
