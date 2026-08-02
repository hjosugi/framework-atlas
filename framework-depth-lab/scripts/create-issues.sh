#!/usr/bin/env bash
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required" >&2
  exit 1
fi

if [[ "${1:-}" != "--apply" ]]; then
  echo "Dry run. The following issue files would be created:"
  find issues -maxdepth 1 -name '*.md' -print | sort
  echo "Run scripts/create-issues.sh --apply after reviewing repository and authentication."
  exit 0
fi

for issue_file in $(find issues -maxdepth 1 -name '*.md' -print | sort); do
  title=$(sed -n 's/^title: "\(.*\)"$/\1/p' "$issue_file" | head -n 1)
  labels=$(sed -n 's/^labels: \[\(.*\)\]$/\1/p' "$issue_file" | tr -d ' ')
  body_file=$(mktemp)
  sed '1,/^---$/d; 1,/^---$/d' "$issue_file" > "$body_file"
  gh issue create --title "$title" --label "$labels" --body-file "$body_file"
  rm -f "$body_file"
done
