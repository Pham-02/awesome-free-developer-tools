# Repository maintenance

## Automated link checks

The `Check links` GitHub Actions workflow runs:
- On pushes to `main` or `master`
- On pull requests
- Every Monday
- Manually through the Actions tab

It checks Markdown links with Lychee. Automated checks can produce false positives when a site blocks bots, rate-limits requests, or has a temporary outage. Review a failure in a browser before deleting an entry.

## Monthly free-plan and license review

The `Monthly free-plan review reminder` workflow opens one issue on the first day of each month. Maintainers and contributors can use it to divide the review work.

The workflow does **not** automatically certify pricing or licensing. A reachable website may have removed its free plan, and an open-source project may have changed its license. Check official pricing pages, documentation, and license files.

## Running the offline inventory script

Requires Python 3. Run from the repository root:

```bash
python scripts/check_markdown_links.py
```

This inventories Markdown links and reports repeated URLs. It does not make network requests.

## Required GitHub repository settings

For scheduled workflows and issue creation:
1. Open repository **Settings → Actions → General**.
2. Under Workflow permissions, allow the `GITHUB_TOKEN` to read and write repository contents as needed for workflows. The monthly reminder specifically needs permission to write issues; its workflow declares `issues: write`.
3. Ensure Actions are enabled for the repository.
4. If your repository uses a branch other than `main` or `master`, update the branch list in `.github/workflows/link-check.yml`.

The monthly reminder uses `GITHUB_TOKEN`; no personal access token or secret is required for the standard repository issue-creation flow.
