# FP | Francisco Buiras | Imagery Prompts (L14)

Prompt pack for the site placeholders and the ad creatives. Written for any
modern image generator (Midjourney, DALL·E, Flux, Ideogram). Generate at the
listed ratio, then export to Drive as **FP_FranciscoBuiras_L14_Imagery**.

## The style system (every prompt ends with these rules)

- Dark, moody environments: charcoal and deep navy, never white backgrounds
- One emerald accent light per image (#10B981 glow from a screen, lamp, or rim light)
- Photorealistic, 35mm lens, shallow depth of field, natural skin texture
- Founder looks focused, not comic-suffering: tired but composed
- No text, logos, or watermarks inside the image (overlays are added later)
- Grade: slightly desaturated with lifted emerald in the shadows

Suffix to append to every prompt below:
`photorealistic, 35mm lens, shallow depth of field, dark moody lighting with a single emerald green accent light, slightly desaturated cinematic grade, no text, no logos`

---

## Site placeholders (drop into `public/site-assets/`)

| File name | Where it goes | Ratio |
|-----------|---------------|-------|
| `portrait-dan.jpg` | Persona card Dan | 4:3 |
| `portrait-vanessa.jpg` | Persona card Vanessa | 4:3 |
| `portrait-chris.jpg` | Persona card Chris | 4:3 |
| `portrait-sofia.jpg` | Persona card Sofia | 4:3 |
| `operator-wide.jpg` | Wide shot under the guarantees | 21:9 |

### portrait-dan.jpg — the Drowning Operator
A Latin American male founder in his late 30s at a home-office desk late at night, face lit by a monitor full of spreadsheets and chat windows, three devices on the desk, coffee mug, posture composed but visibly overloaded, eyes on the screen, --ar 4:3 + suffix

### portrait-vanessa.jpg — burned by a VA
A Latina founder in her early 40s sitting at an office desk reviewing a tall stack of printed resumes, arms crossed, skeptical half-smile, laptop open to a hiring site, one emerald desk lamp lighting the resumes, --ar 4:3 + suffix

### portrait-chris.jpg — chaos at scale
A male founder in his mid 30s standing in front of a whiteboard covered in arrows and sticky notes, phone pressed to his ear, gesturing at the board, home office at dusk, single emerald lamp glow on the board, --ar 4:3 + suffix

### portrait-sofia.jpg — solo until now
A Latina founder in her early 30s closing a laptop at a tidy desk in golden-hour window light, relieved half-smile, notebook and single coffee cup, the only dark room in an otherwise bright scene, --ar 4:3 + suffix

### operator-wide.jpg — the Right Hand at work
A wide cinematic shot of a professional operations specialist at a minimal standing desk in a dark room, three monitors showing clean calendars, inboxes and dashboards, emerald screen glow lighting the scene, the desk impeccably organized, sense of calm control, --ar 21:9 + suffix

---

## Ad creatives (for the Drive ads folder, L13)

| File name | Used in | Ratio |
|-----------|---------|-------|
| `FP_FranciscoBuiras_Ad1.png` | Ad 1 · Dan | 4:5 (Meta feed) |
| `FP_FranciscoBuiras_Ad2.png` | Ad 2 · Vanessa | 4:5 |
| `FP_FranciscoBuiras_Ad3.png` | Ad 3 · Chris | 4:5 |
| `FP_FranciscoBuiras_Ad4.png` | Ad 4 · Sofia | 4:5 |
| `FP_FranciscoBuiras_Ad5.png` | Ad 5 · Destination | 1:1 graphic |

Ads 1–4: generate the matching portrait at 4:5 (same prompts, change the ratio),
then add text overlays in Canva:
- Ad 1 overlay: "16 hrs/wk" in emerald, subline "doing a $10/hour job"
- Ad 2 overlay: "Never again." headline, subline "unless someone else did the vetting"
- Ad 3 overlay: "If you took a week off…" headline, subline "would the business stop?"
- Ad 4 overlay: "You didn't leave your job for this." headline, subline "reclaim your 15 hours"

Ad 5 is a pure graphic (no face): on a `#050A0E` background, "15 hrs/wk" set
oversized in emerald #10B981, subline in white "what would you do with them?",
small Pareto spark logo bottom corner. Build in Canva with DM Sans bold.

---

## Swap-in instructions (site)

1. Save the five site images into `public/site-assets/` with the exact file names above.
2. Open `src/pages/Landing.jsx`, find each `<ImgPlaceholder … />` (a comment above the persona grid shows the pattern), and replace it with:
   `<img src="/Final-Project/site-assets/FILENAME.jpg" alt="DESCRIPTION" style={{ borderRadius: 12 }} />`
3. Commit and push — auto-deploy takes care of the rest.
