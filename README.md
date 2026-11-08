# Atelier Banger — website

Static reproduction of atelierbanger.com (Robin Miellet, Compagnon du Devoir). Hosted with GitHub Pages from the `main` branch.

## Layout

- `index.html`, `about/`, `services/`, `portfolio/` (+ one folder per project), `collection/`, `contact/`, `artisans/`, `privacy/`, `terms/` — the generated pages, same URLs as the original site.
- `assets/site.css`, `assets/site.js` — shared styles (Tailwind via CDN + a few custom rules) and behaviour (header, carousel, galleries, lightbox, portfolio filter, timeline, contact form).
- `builder/data.py` — **all content**: site details, featured carousel, portfolio projects, collection pieces, about timeline, workshop photos.
- `builder/build.py` — page templates. Run `python3 builder/build.py .` from the repo root to regenerate every page after editing `data.py`.

## Images

Images and the hero video currently load from `https://atelierbanger.com` (`ASSET` in `builder/data.py`). To host them here, copy the `images/` folder (same paths) into this repo, set `ASSET = ""` and rebuild.

## Contact form

GitHub Pages has no server, so "Send Inquiry" opens the visitor's mail app with the inquiry prefilled, addressed to info@atelierbanger.com. For a real form backend, connect Formspree, Netlify Forms or similar in `assets/site.js`.
