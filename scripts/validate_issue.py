import json
import os
import re
import subprocess
import sys
import urllib.request
from urllib.parse import quote, urlparse

BODY = os.environ.get("ISSUE_BODY", "")
ISSUE_NUMBER = os.environ.get("ISSUE_NUMBER", "")
AUTHOR = os.environ.get("ISSUE_AUTHOR", "")
REPOSITORY = os.environ.get("REPOSITORY", "")

def fail(message):
    print("Validation failed:", message)
    if ISSUE_NUMBER and REPOSITORY:
        subprocess.run([
            "gh", "issue", "comment", ISSUE_NUMBER,
            "--repo", REPOSITORY,
            "--body", "❌ ~ring application rejected.\n\n" + message
        ], check=False)
        subprocess.run([
            "gh", "issue", "edit", ISSUE_NUMBER,
            "--repo", REPOSITORY,
            "--add-label", "rejected",
            "--state", "closed"
        ], check=False)
    sys.exit(1)

def input_field(label):
    pattern = r"### " + re.escape(label) + r"\s*\n\s*([^\n]+)"
    match = re.search(pattern, BODY, re.IGNORECASE)
    return match.group(1).strip() if match else ""

site_name = input_field("Site name")
site_url = input_field("Site URL")

description_match = re.search(
    r"### Description\s*\n\s*([\s\S]*?)(?=\n### |\Z)",
    BODY, re.IGNORECASE
)
description = description_match.group(1).strip() if description_match else ""

if not site_name or not site_url or not description:
    fail("The issue does not follow the required template.")

parsed = urlparse(site_url)
if parsed.scheme not in ("http", "https") or not parsed.netloc:
    fail("Site URL must be a valid HTTP(S) URL.")

normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/") or f"{parsed.scheme}://{parsed.netloc}"

try:
    request = urllib.request.Request(
        site_url,
        headers={"User-Agent": "~ring-verifier/1.0"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        if response.status < 200 or response.status >= 400:
            fail(f"Site returned HTTP {response.status}.")
        html = response.read(2_000_000).decode("utf-8", errors="ignore")
except Exception as exc:
    fail(f"Could not fetch the site: {exc}")

if 'data-webring="~ring"' not in html and "data-webring='~ring'" not in html:
    fail("The ~ring marker was not found on the submitted site.")

with open("members.json", encoding="utf-8") as f:
    registry = json.load(f)

members = registry.get("members", [])

try:
    github_request = urllib.request.Request(
        "https://api.github.com/users/" + quote(AUTHOR),
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "~ring-verifier/1.0",
        },
        method="GET",
    )
    with urllib.request.urlopen(github_request, timeout=15) as response:
        github_user = json.load(response)
    github_id = github_user.get("id")
    github_login = github_user.get("login")
except Exception as exc:
    fail(f"Could not resolve GitHub user: {exc}")

if not isinstance(github_id, int) or not github_login:
    fail("Could not resolve a valid GitHub user ID.")

if sum(1 for m in members if m.get("githubId") == github_id) >= 3:
    fail("This GitHub account already has 3 registered applications.")

def is_same_or_nested_url(existing, candidate):
    existing_url = existing.rstrip("/")
    candidate_url = candidate.rstrip("/")
    return (
        existing_url == candidate_url
        or candidate_url.startswith(existing_url + "/")
        or existing_url.startswith(candidate_url + "/")
    )

if any(is_same_or_nested_url(m.get("url", ""), normalized) for m in members):
    fail("This site or a parent/child path is already registered.")

members.append({
    "name": site_name,
    "url": normalized,
    "description": description,
    "github": github_login,
    "githubId": github_id,
    "status": "active",
    "consecutiveFailures": 0
})

def write_registry():
    payload = json.dumps(registry, ensure_ascii=False, indent=2) + "\n"
    with open("members.json", "w", encoding="utf-8") as f:
        f.write(payload)
    os.makedirs("docs", exist_ok=True)
    with open("docs/members.json", "w", encoding="utf-8") as f:
        f.write(payload)

write_registry()

subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
subprocess.run(["git", "add", "members.json", "docs/members.json"], check=True)
subprocess.run(["git", "commit", "-m", "chore: add ~ring member #" + ISSUE_NUMBER], check=True)
subprocess.run(["git", "push"], check=True)

subprocess.run([
    "gh", "issue", "comment", ISSUE_NUMBER,
    "--repo", REPOSITORY,
    "--body", "✅ Your site passed ~ring validation and has been added to the ring."
], check=False)
subprocess.run([
    "gh", "issue", "edit", ISSUE_NUMBER,
    "--repo", REPOSITORY,
    "--add-label", "approved",
    "--state", "closed"
], check=False)
