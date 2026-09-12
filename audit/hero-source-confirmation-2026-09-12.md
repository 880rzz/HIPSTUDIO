# HIPStudio hero source confirmation — 2026-09-12

Status: user-confirmed first-party source for the unpublished master-site rebuild.

- HIPStudio YouTube channel: https://www.youtube.com/@wearehipstudio
- Selected home hero film: https://youtu.be/gnuMDSWR_tg
- Video ID: `gnuMDSWR_tg`

The user explicitly identified the channel as HIPStudio's own YouTube channel and explicitly selected this film for the home hero.

Implementation rule:
- do not hotlink Wix media;
- prefer a cleared self-hosted derivative if a lawful source file is available;
- otherwise use the official privacy-enhanced YouTube embed (`youtube-nocookie.com`);
- do not create a generic YouTube player box or expose standard player chrome as the main visual treatment;
- preserve accessible fallback and reduced-motion behavior;
- to preserve the existing zero-third-party-request privacy gate, do not assign the iframe `src` until explicit user activation unless a compliant consent state already exists.

This resolves the previous uncertainty about which first-party film the hero should use. It does not by itself authorize downloading or transcoding the YouTube stream into a new local derivative.
