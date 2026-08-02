PYTHON ?= python3
VERSION ?= $(shell cat VERSION)
REPO ?= hjosugi/framework-atlas

.PHONY: build check validate test site profiles manifest zip issues collect merge serve clean

build: profiles site manifest

profiles:
	$(PYTHON) scripts/generate_issue_markdown.py
	$(PYTHON) scripts/generate_profiles.py

site:
	$(PYTHON) scripts/build_site.py

manifest:
	$(PYTHON) scripts/manifest.py --write

validate:
	$(PYTHON) scripts/validate.py
	$(PYTHON) scripts/validate_data.py
	$(PYTHON) framework-depth-lab/scripts/validate.py

test:
	$(PYTHON) -m unittest discover -s tests -v
	node --check docs/app.js

check: build validate test
	$(PYTHON) scripts/verify_issue_export.py
	$(PYTHON) scripts/build_site.py --check
	$(PYTHON) scripts/manifest.py --check
	$(PYTHON) scripts/smoke_site.py
	$(PYTHON) scripts/build_zip.py --version $(VERSION) --check

zip: build
	$(PYTHON) scripts/build_zip.py --version $(VERSION)

collect:
	$(PYTHON) scripts/collect_github_topics.py --scope core --resume

merge:
	$(PYTHON) scripts/merge_discovered.py --min-confidence 0.85 --max-new 500

issues:
	@test -n "$(REPO)" || (echo "Usage: make issues REPO=OWNER/REPOSITORY" && exit 2)
	$(PYTHON) scripts/create_issues.py --repo $(REPO) --dry-run

serve:
	$(PYTHON) -m http.server 8000 --directory docs

clean:
	rm -rf docs/data docs/research-issues data/discovered data/snapshots
	rm -f docs/atlas-data.json docs/source.json dist/framework-atlas-*.zip dist/SHA256SUMS
