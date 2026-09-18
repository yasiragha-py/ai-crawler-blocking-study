import requests
import pandas as pd
import time

# Sites that failed in the first run
failed_sites = {
    "https://figma.com": "SaaS",
    "https://hm.com": "E-commerce",
    "https://asos.com": "E-commerce",
    "https://youtube.com": "Mixed/General",
    "https://reddit.com": "Mixed/General",
    "https://pinterest.com": "Mixed/General",
    "https://wikipedia.org": "Mixed/General",
    "https://github.com": "Mixed/General",
    "https://spotify.com": "Mixed/General",
    "https://netflix.com": "Mixed/General",
    "https://airbnb.com": "Mixed/General",
    "https://booking.com": "Mixed/General",
    "https://tripadvisor.com": "Mixed/General",
    "https://quora.com": "Mixed/General",
    "https://stackoverflow.com": "Mixed/General",
    "https://wordpress.com": "Mixed/General",
    "https://tumblr.com": "Mixed/General",
}

ai_bots = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "CCBot", "Applebot-Extended"]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def check_bot_status(robots_text, bot_name):
    lines = robots_text.split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if line.lower() == f"user-agent: {bot_name.lower()}":
            for next_line in lines[i+1:]:
                next_line = next_line.strip()
                if next_line.lower().startswith("user-agent:"):
                    break
                if next_line.lower() == "disallow: /":
                    return "Blocked"
                if next_line.lower().startswith("disallow:") and next_line.lower() != "disallow:":
                    return "Partially Blocked"
            return "Allowed (explicitly listed)"
    return "Allowed (not mentioned)"


results = []

for site, category in failed_sites.items():
    row = {"site": site, "category": category}
    success = False

    for attempt in range(3):
        try:
            response = requests.get(f"{site}/robots.txt", headers=headers, timeout=15)
            content = response.text

            for bot in ai_bots:
                row[bot] = check_bot_status(content, bot)

            row["status_code"] = response.status_code
            print(f"Checked: {site} ({category}) — Status {response.status_code} [attempt {attempt+1}]")
            success = True
            break

        except Exception as e:
            print(f"Attempt {attempt+1} failed for {site}: {e}")
            time.sleep(2)

    if not success:
        for bot in ai_bots:
            row[bot] = "Error"
        row["status_code"] = "Failed"
        row["error"] = "Failed after 3 attempts"

    results.append(row)
    time.sleep(1)

df = pd.DataFrame(results)
df.to_csv("ai_crawler_retry_results.csv", index=False)
print("\nDone. Saved to ai_crawler_retry_results.csv")