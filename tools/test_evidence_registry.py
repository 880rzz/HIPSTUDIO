# coding: utf-8
from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
registry = json.loads((R/'content/evidence-registry.json').read_text())
provenance = json.loads((R/'content/provenance.json').read_text())
cases = json.loads((R/'content/case_studies.json').read_text())
people = json.loads((R/'content/people.json').read_text())

assert registry['version'] == 'evidence-registry-v1'
assert registry['status'] == 'review'
assert set(registry['publicationStatuses']) == {'verified_public_fact','approved_media','historical_reference_only','pending_review','unpublished'}

sets = {x['key']: x for x in registry['evidenceSets']}
required = {'hipstudio-heritage','professional-partners','portfolio-media','historical-partner-logos','pending-media','case-studies'}
assert required <= set(sets)

assert sets['hipstudio-heritage']['status'] == 'verified_public_fact'
assert {'hipstudio-founded','hipstudio-founder'} <= set(sets['hipstudio-heritage']['supports'])
claim_ids = {x['id'] for x in provenance['claims']}
assert {'hipstudio-founded','hipstudio-founder','professional-partners','portfolio-media'} <= claim_ids

assert sets['portfolio-media']['status'] == 'approved_media'
assert 'content/images.json' in sets['portfolio-media']['sources']
assert sets['pending-media']['status'] == 'pending_review'
assert sets['pending-media']['supports'] == []
assert 'audit/pending-images.json' in sets['pending-media']['sources']

assert sets['historical-partner-logos']['status'] == 'historical_reference_only'
logo_rule = sets['historical-partner-logos']['allowedUse'].lower()
for forbidden in ('current customer','client outcome','ongoing engagement'):
    assert forbidden in logo_rule

assert cases['items'] == []
assert sets['case-studies']['status'] == 'unpublished'
assert registry['publicClaimClasses']['caseStudies'] == []
assert registry['publicClaimClasses']['clientResults'] == []
assert registry['publicClaimClasses']['testimonials'] == []
assert registry['publicClaimClasses']['currentClientRelationships'] == []

assert len(people) == 2
for person in people:
    assert person['sources']
    for source in person['sources']:
        assert source in provenance['sources']

rules = registry['rules']
for key in ('clientResult','testimonial','currentRelationship','media','historicalReference','regulatedResponsibility'):
    assert key in rules and len(rules[key]) > 30

# Evidence registry itself must never broaden production claims beyond source-backed classes.
assert not registry['publicClaimClasses']['clientResults']
assert not registry['publicClaimClasses']['testimonials']
assert not registry['publicClaimClasses']['currentClientRelationships']

print('Evidence registry publication gate passed')
