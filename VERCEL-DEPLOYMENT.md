# Vercel deployment

This is a static HTML/CSS/JavaScript site. The generated `dist/` files and all assets are committed, so deployment requires no package installation or cloud build runtime.

## GitHub import settings

- Account: `bendiazdos`
- Repository: `bendiazdos/yosoyben-portfolio`.
- Root Directory: the directory containing `vercel.json` and `dist/` (`.` if this folder is the repository root; `portfolio` if importing the parent workspace).
- Framework Preset: Other.
- Build Command: disabled/empty.
- Install Command: disabled/empty.
- Output Directory: `dist`.
- Environment Variables: none required.
- Production Branch: select the repository default branch.

`vercel.json` stores these deployment settings and preserves trailing-slash routes such as `/work/lockheed-martin/`. No SPA catch-all rewrite is needed.

## Content updates

Run `python3 build.py` locally after editing templates or JSON content. Commit the changed source and generated `dist/` files, then push to GitHub. Vercel publishes the committed static output. CSS and JavaScript live in `dist/`; do not delete that folder before running the generator.

## Custom domain

The intended domain is `yosoyben.com`. After the first successful Vercel deployment:

1. Add the domain in Project Settings → Domains.
2. Add its `www` variant if desired and select the preferred primary address.
3. At the current DNS provider, apply the exact A/CNAME and any verification records Vercel displays for this project. Do not copy generic DNS values.
4. Keep existing MX, SPF, DKIM, DMARC, and other unrelated DNS records intact.
5. Wait for Vercel to confirm DNS and issue HTTPS, then verify the landing page, nested project routes, images, and redirects.

The existing Sites URL remains available during setup. DNS migration should happen after the Vercel preview is verified.

References: https://vercel.com/docs/builds/configure-a-build and https://vercel.com/docs/domains/set-up-custom-domain
