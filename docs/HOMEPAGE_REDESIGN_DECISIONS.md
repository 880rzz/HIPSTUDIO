# HIPStudio homepage redesign decisions

## Removed from the primary homepage

- Centered slogan-first hero and generic secondary CTA.
- Equal three-card service and feature grids.
- Decorative orb, glow and glass-style treatments.
- Repeated "one system / three pillars" marketing claims.
- Unqualified Business / Operations promise from the creative homepage.
- Auto-loaded third-party showreel or external media.
- Generic client-result, award, testimonial and scale claims.

## Retained and made explicit

- Verified 2006 founding history and Budapest location.
- Existing first-party photo, video and podcast capability facts.
- Explicit-click HIPStudio showreel link only.
- Official current contact route and human quote conversation.
- Evidence and responsibility limits: project roles, contracting party and scope remain quote-specific.

## Homepage source contract

`content/homepage-redesign.json` is the content source for the editorial homepage assembled by `tools/build.py`. The generated homepage has one primary 30-minute CTA, an asymmetric problem-to-response sequence, a four-step working method, two concrete situations, and a provenance/trust strip. It intentionally does not establish client outcomes, current relationships, regulated-service scope, or Business / Operations delivery claims.

## TODO before production approval

- A self-hosted, rights-cleared showreel file and poster are required before replacing the explicit external playback link with an inline video.
- Legal/privacy, media-rights, infrastructure, publication and public-readback gates remain governed by the existing release documents.
