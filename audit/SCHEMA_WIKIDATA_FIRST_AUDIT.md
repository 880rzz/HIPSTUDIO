# HIPStudio schema — Wix/Wikidata-first audit

Checked: 2026-09-14

## Source precedence

1. Current public HIPStudio/Wix pages define the public entity, services, contact context and visible legal separation.
2. Wikidata `Q138482177` is the first identity link in `Organization.sameAs` and supplies an independently addressable public entity.
3. `content/legal-controller.json` remains authoritative for the Hipstudió Kft. legal name and registered office.
4. The Budapest studio remains a separate `Place` referenced through `Organization.location`.

## Confirmed alignment

- Wix schema identifies HIPStudio as `Organization` / `ProfessionalService` and places Wikidata `Q138482177` first in `sameAs`.
- Wikidata records HIPStudio as a photographic studio, advertising agency and marketing agency, with inception `2006-02-27`, official website `https://www.hipstudio.hu`, founder Bánhalmi Norbert and Budapest context.
- The current HIPStudio legal/privacy page states that Bánhalmi Norbert founded the HIPStudio communication and creative brand on 2006-02-27, while Hipstudió Kft. is the current operator and controller.

## Generated contract

- `Organization.@id`: `https://www.hipstudio.hu/#organization`
- `sameAs[0]`: `https://www.wikidata.org/wiki/Q138482177`
- `foundingDate`: `2006-02-27`
- registered office: sourced from `content/legal-controller.json`
- public studio: separate `Place` node
- founder: separate `Person` node linked to Wikidata `Q56391118`

The regression and projection layers must preserve this order and may not silently remove the verified inception date.
