import json
import urllib.request

with open("members.json", encoding="utf-8") as f:
    registry = json.load(f)

changed = False

for member in registry.get("members", []):
    url = member.get("url")
    if not url:
        continue

    ok = False
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "~ring-monitor/1.0"},
            method="GET",
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            html = response.read(2_000_000).decode("utf-8", errors="ignore")
            ok = (
                200 <= response.status < 400
                and (
                    'data-webring="~ring"' in html
                    or "data-webring='~ring'" in html
                )
            )
    except Exception:
        ok = False

    failures = int(member.get("consecutiveFailures", 0))

    if ok:
        if member.get("status") != "active" or failures:
            changed = True
        member["status"] = "active"
        member["consecutiveFailures"] = 0
    else:
        failures += 1
        if member.get("consecutiveFailures") != failures:
            changed = True
        member["consecutiveFailures"] = failures
        if failures >= 3 and member.get("status") != "inactive":
            member["status"] = "inactive"
            changed = True

if changed:
    with open("members.json", "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
        f.write("\n")
