PYTHON ?= python3
VERSION ?= v0.1.1

.PHONY: check validate test site zip issues clean

check: validate test
	$(PYTHON) scripts/verify_issue_export.py
	$(PYTHON) scripts/build_site.py --check
	$(PYTHON) scripts/smoke_site.py
	$(PYTHON) scripts/build_zip.py --version $(VERSION) --check

validate:
	$(PYTHON) scripts/validate.py

test:
	$(PYTHON) -m unittest discover -s tests -v

site:
	$(PYTHON) scripts/build_site.py

zip: site
	$(PYTHON) scripts/build_zip.py --version $(VERSION)

issues:
	$(PYTHON) scripts/export_issues.py --repo hjosugi/framework-atlas

clean:
	rm -f docs/atlas-data.json dist/framework-atlas-*.zip dist/SHA256SUMS
