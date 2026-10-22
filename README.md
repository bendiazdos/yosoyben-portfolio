# Ben Diaz — grayscale portfolio

A buildless, responsive portfolio with a grayscale technical visual system and restrained orange (#e85a24, from the Husky reference) number/control accents, bold mono headings, thin grid rules, an interactive procedural form study, and five-chapter case studies.

## Pages

- `/` — landing page with a locally rendered 3D form and an Enter Work button.
- `/work/` — two-column six-project grid with artwork behind each hovered or keyboard-focused link.
- `/work/<slug>/` — five accessible chapters, expandable process notes, image enlargement, restrained cover parallax, and a next-project link.
- `/about/` — bio, skills, profile photograph placeholder, and résumé download location.
- `/connect/` — contact destination, or an email-draft form when an email is configured.

## Edit and preview

- `projects.json` contains project metadata.
- `content.json` preserves the supplied case-study copy. `build.py` reorganizes it into five chapters and adds concise design rationale based on the supplied descriptions.
- `settings.json` configures the contact email, résumé URL, and fallback contact destination.
- Run `python3 build.py` after content/template/configuration changes.
- `dist/style.css` and `dist/script.js` contain the visual system and interactions.
- Preview with `python3 -m http.server 4173 --directory dist`.
- No external runtime dependencies, analytics, or third-party form service are required.

## Pending content

- Set `email` in `settings.json` to the intended public professional address to enable the local email-draft form. Visitors send the message from their own email app; no message is sent automatically.
- Copy the real résumé PDF into `dist/assets/` and set `resume` to its root-relative URL. Until then the download control is disabled and marked as pending.
- Add a profile photograph when available.
- Lockheed Martin, Mattermost, and Leidos CLD retain typographic project covers pending final project images.
- Review the concise goals/process/visual rationale copy for the five projects whose original case studies were short. No research, measurements, or outcome metrics have been invented.

## Accessibility and motion

The form study defaults to paused for reduced-motion preferences. It has an explicit play/pause control, suspends rendering offscreen, and uses locally computed geometry. Chapter tabs support arrow keys, Home, End, and standard focus movement. The native image dialog supports Escape and restores focus. Parallax and transitions respect reduced motion.

## Publication

The Site is public and shareable. The existing yosoyben.com domain is unaffected. Original reference templates remain in `case-studies/` for reference, but are not loaded by the new pages.

## Vercel

See [VERCEL-DEPLOYMENT.md](VERCEL-DEPLOYMENT.md) for GitHub import settings, content updates, and custom-domain setup. The deployment configuration is in `vercel.json`.
