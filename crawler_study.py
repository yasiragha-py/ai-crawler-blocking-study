import requests
import pandas as pd
import time

sites = [
    # SaaS (25)
    "https://stripe.com", "https://shopify.com", "https://notion.so", "https://slack.com",
    "https://zoom.us", "https://hubspot.com", "https://salesforce.com", "https://asana.com",
    "https://trello.com", "https://monday.com", "https://airtable.com", "https://figma.com",
    "https://canva.com", "https://dropbox.com", "https://mailchimp.com", "https://zendesk.com",
    "https://atlassian.com", "https://intercom.com", "https://calendly.com", "https://webflow.com",
    "https://squarespace.com", "https://wix.com", "https://freshworks.com", "https://clickup.com",
    "https://loom.com",

    # E-commerce (25)
    "https://amazon.com", "https://ebay.com", "https://etsy.com", "https://walmart.com",
    "https://target.com", "https://bestbuy.com", "https://aliexpress.com", "https://wayfair.com",
    "https://nike.com", "https://adidas.com", "https://zara.com", "https://hm.com",
    "https://ikea.com", "https://sephora.com", "https://chewy.com", "https://newegg.com",
    "https://homedepot.com", "https://lowes.com", "https://costco.com", "https://asos.com",
    "https://overstock.com", "https://gap.com", "https://macys.com", "https://nordstrom.com",
    "https://ulta.com",

    # Content / Blog / News (25)
    "https://nytimes.com", "https://theverge.com", "https://techcrunch.com", "https://wired.com",
    "https://forbes.com", "https://bbc.com", "https://cnn.com", "https://medium.com",
    "https://businessinsider.com", "https://bloomberg.com", "https://reuters.com", "https://engadget.com",
    "https://mashable.com", "https://buzzfeed.com", "https://vox.com", "https://axios.com",
    "https://theatlantic.com", "https://wsj.com", "https://huffpost.com", "https://slate.com",
    "https://vice.com", "https://hbr.org", "https://fastcompany.com", "https://entrepreneur.com",
    "https://inc.com",

    # Mixed / Top general (25)
    "https://google.com", "https://youtube.com", "https://facebook.com", "https://instagram.com",
    "https://linkedin.com", "https://twitter.com", "https://reddit.com", "https://pinterest.com",
    "https://wikipedia.org", "https://github.com", "https://spotify.com", "https://netflix.com",
    "https://airbnb.com", "https://booking.com", "https://tripadvisor.com", "https://yelp.com",
    "https://glassdoor.com", "https://indeed.com", "https://coursera.org", "https://udemy.com",
    "https://khanacademy.org", "https://quora.com", "https://stackoverflow.com", "https://wordpress.com",
    "https://tumblr.com",
]

categories = (["SaaS"] * 25) + (["E-commerce"] * 25) + (["Content/News"] * 25) + (["Mixed/General"] * 25)

ai_bots = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "CCBot", "Applebot-Extended"]

headers = {"User-Agent": "Mozilla/5.0 (AEOShark Research Bot)"}


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

for site, category in zip(sites, categories):
    row = {"site": site, "category": category}
    try:
        response = requests.get(f"{site}/robots.txt", headers=headers, timeout=10)
        content = response.text

        for bot in ai_bots:
            row[bot] = check_bot_status(content, bot)

        row["status_code"] = response.status_code
        print(f"Checked: {site} ({category}) — Status {response.status_code}")

    except Exception as e:
        for bot in ai_bots:
            row[bot] = "Error"
        row["status_code"] = "Failed"
        row["error"] = str(e)
        print(f"Failed: {site} — {e}")

    results.append(row)
    time.sleep(0.5)

df = pd.DataFrame(results)
df.to_csv("ai_crawler_full_study.csv", index=False)
print("\nDone. Saved to ai_crawler_full_study.csv")
print(f"Total sites checked: {len(results)}")