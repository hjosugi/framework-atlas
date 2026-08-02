# Contributing

## Add or improve a framework

1. Edit `data/curated-frameworks.json` or open the `Framework research` issue form.
2. Add primary sources whenever possible: official documentation, release announcements, design documents, papers, maintainer talks, or repository history.
3. Separate an explicit influence claim from architectural similarity.
4. Run:

```bash
make build
make validate
make test
```

## Evidence rule

Do not write “A influenced B” merely because they look similar. Use one of these relationship states:

- `verified`: an official or maintainer source states the relationship.
- `supported`: repository history or a strong primary source supports it.
- `hypothesis`: a useful research lead, not a fact.
- `disputed`: credible sources conflict.

## Scope

Framework-adjacent libraries, runtimes, engines, and platforms may be included when they shaped framework design. Their `kind` must be explicit so they are not compared as if they were equivalent.
