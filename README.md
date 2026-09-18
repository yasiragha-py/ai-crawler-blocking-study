# AI Crawler Blocking Study

Which major websites block AI crawlers, and does it differ by industry?

We checked the `robots.txt` files of 98 major websites across four categories — SaaS, e-commerce, content/news publishers, and a mixed general category — for rules governing six AI crawlers: GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot, and Applebot-Extended.

Full write-up: [aeoshark.com/blog/ai-crawler-lockout](https://aeoshark.com/blog/) *(link once published)*

## Key findings

- 64% of content/news publishers block at least one AI crawler, vs 16% for SaaS and 16% for e-commerce
- 5 publishers block all six crawlers completely: The New York Times, BBC, Bloomberg, BuzzFeed, HuffPost
- ClaudeBot is the most frequently blocked crawler (21.4% of sites); Applebot-Extended the least (16.3%)

## Files

- `crawler_study.py` — main scraper, checks 100 sites against 6 AI bots
- `retry_failed.py` — retry pass for sites that failed on first attempt (timeouts/DNS)
- `final_98_sites.csv` — combined, cleaned dataset (98 of 100 sites; Quora and Tumblr excluded due to persistent connection failures)

## Methodology

Each site's `robots.txt` was fetched and parsed for `User-agent` blocks matching each of the six bots. A site was marked:

- **Blocked** — full `Disallow: /` under that bot's user-agent block
- **Partially Blocked** — a specific path disallowed, not the whole site
- **Allowed (explicitly listed)** — bot has a user-agent block with no disallow rule
- **Allowed (not mentioned)** — bot not referenced in robots.txt at all (default allow)

## Reproduce it

```bash
pip install requests pandas
python crawler_study.py
python retry_failed.py
```

## License

Data and code are free to use and cite. Attribution appreciated: link back to [aeoshark.com](https://aeoshark.com).
