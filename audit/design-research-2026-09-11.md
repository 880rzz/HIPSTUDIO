# HIPStudio design research — 2026-09-11

Status: implementation guidance for the unpublished master-site rebuild. This is not a production approval.

## Why this exists

The current rebuild must avoid the visual defaults now strongly associated with AI/vibe-coded SaaS sites. Public design discussions in 2025–2026 repeatedly identify the same failure modes: purple/blue gradients, centered hero copy, one generic CTA, Inter-like default typography, three equal rounded cards, glassmorphism, repeated section rhythm, generic glows and copy that describes abstractions rather than what a company actually does.

Research references reviewed:
- https://www.reddit.com/r/AISEOforBeginners/comments/1tk9lwg/why_do_all_aigenerated_websites_look_the_same_now/
- https://www.reddit.com/r/webdesign/comments/1m2om61/
- https://www.reddit.com/r/UI_Design/comments/1tvb91q/ai_fatigue_from_seeing_same_designs/
- https://www.reddit.com/r/webdesign/comments/1vfck61/it_feels_like_there_are_more_ai_websites_than/
- https://www.reddit.com/r/mcp/comments/1v98u95/i_built_an_mcp_to_stop_ai_websites_from_all/

Forum discussion is treated as qualitative design research, not factual authority. The useful common signal is that intentional constraints and art direction matter more than adjective prompts such as “premium”, “modern” or “Apple-like”.

## HIPStudio visual constitution

### 1. Narrative before components
Every section must answer one of these jobs:
1. establish what problem HIPStudio solves;
2. show what is actually delivered;
3. prove that HIPStudio has done comparable work;
4. explain flexibility or delivery mechanics;
5. move the buyer to the next action.

If a block has no narrative job, remove it rather than decorating it.

### 2. Composition
- Do not use a repeated three-equal-card system as the primary layout language.
- Alternate full-bleed media, editorial splits, asymmetric grids, narrow reading columns and compact proof strips.
- Use deliberate image crops with at least three recurring ratios: cinematic 16:9 / 2:1, editorial 4:5, and documentary 3:2.
- Allow controlled edge breaks and offset alignment where content supports them.
- Negative space must separate ideas, not merely make the page longer.

### 3. Typography
- Keep native/system font loading for performance unless a self-hosted typeface with explicit license is later approved.
- Create personality through scale, line length, weight contrast and composition rather than loading a fashionable web font by default.
- Headlines: short, specific, editorial; avoid generic claims.
- Body copy: readable 60–72 character measure on long-form sections.
- Eyebrows are metadata, not decoration; use sparingly.

### 4. Color and surfaces
Core roles:
- warm paper / ivory for editorial reading surfaces;
- deep navy/near-black for cinematic/high-trust sections;
- restrained warm gold only for emphasis, rules, active states or small highlights;
- no purple/blue SaaS gradient language.

Gradient rule: gradients may create light, depth or transition, but may not replace composition. No decorative neon blobs.

### 5. Corner language
Use no more than three corner behaviors across the system:
- square / nearly square for editorial structures;
- modest radius for media containers;
- pill only for true compact controls where shape communicates interaction.

Do not make every card/button/container a pill or 24–32 px rounded rectangle.

### 6. Motion
- Motion must explain hierarchy or interaction.
- Menu opening/closing: short opacity/transform transition.
- Optional media reveal: subtle only.
- No generic scroll fade-up on every section.
- `prefers-reduced-motion` must remove non-essential motion and stop autoplay visuals where appropriate.

### 7. Navigation
Requested target: one compact hamburger control on desktop and mobile.

Full-screen menu requirements:
- category name plus short human description;
- clear current-language state;
- keyboard open/close;
- ESC close;
- focus trap while open;
- restore focus to trigger after close;
- body scroll lock;
- visible focus states;
- no hidden duplicate navigation announced by assistive tech.

Recommended Hungarian menu language:
- **Szolgáltatások** — „Amit ténylegesen elkészítünk: fotó, film, podcast és a kapcsolódó tartalom.”
- **Megoldások** — „Ha nem szolgáltatást keresel, hanem egy konkrét kommunikációs problémát kell megoldani.”
- **Munkák** — „Valódi projektek, képek, filmek és az, amit hitelesen meg tudunk mutatni belőlük.”
- **Rólunk** — „Kik dolgoznak a háttérben, hogyan oszlik meg a felelősség, és kivel szerződsz.”
- **Kapcsolat** — „Mondd el, mit kell elérni. Innen együtt rakjuk össze a szükséges stábot és formátumot.”

Equivalent EN/DE copy must be adapted, not mechanically translated.

### 8. Hero
Target state: self-hosted HIPStudio showreel or approved hero film, full-bleed.

Required implementation:
- local MP4/WebM if available;
- local poster image;
- `autoplay muted loop playsinline`;
- no controls in decorative autoplay state;
- dark art-directed overlay for text contrast;
- reduced-motion fallback to poster/static frame;
- no Wix CDN URL in production output;
- visible text remains useful when video does not load.

Current blocker: `content/videos.json` only records Wix CDN sources. A self-hostable asset with confirmed publication rights is still required before the hero can be production-ready.

### 9. Image density
The repository already contains many locally processed photo variants whose `publicationRights` field is recorded as `user_confirmed_2026-09-07`. These are better candidates for visual density than generic generated/stock imagery, but final placement still requires subject/context review and an explicit provenance manifest.

Do not infer client/project identity from a portrait alone.

### 10. Copy test
Every major section must pass this test:
- Can a buyer understand the problem without agency jargon?
- Can they tell what HIPStudio actually does?
- Is the output/result concrete?
- Is the flexibility explained with real variables (format, crew, timing, location, delivery) rather than “tailored solutions”?
- Is there evidence?
- Is the next action obvious?

## Current high-priority visual debt

1. Header still exposes classic desktop nav plus separate mobile `<details>` navigation; this contradicts the requested single full-screen hamburger model.
2. Home hero is static split image/text, not full-bleed media.
3. Current CSS relies heavily on repeated service-grid rhythm and needs more varied editorial composition.
4. Current visual system uses many pill buttons; retain pills only where they remain intentional controls.
5. Real cleared local photos are present but underused on the master home experience.
6. The page needs a provenance-aware media selection layer before broader media integration.

## Release rule

Do not call the design complete because it is visually polished in one viewport. Completion requires screenshot/browser evidence at 320, 390, 768, 1440 and 1920 widths, keyboard navigation evidence, reduced-motion behavior and WCAG AA checks.