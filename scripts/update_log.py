#!/usr/bin/env python3
"""Update activity log with daily summary."""

import json
import os
from datetime import datetime
import pytz

def update_log():
    """Generate daily summary and append to activity log."""
    
    tz = pytz.timezone('America/Toronto')
    now = datetime.now(tz)
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S %Z')
    
    # Collect data from all sources
    summary = {
        'date': date_str,
        'time': time_str,
        'stats': None,
        'news_count': 0,
        'quote': None,
        'weather': None,
        'trending_count': 0,
        'health_checks': {}
    }
    
    # Load GitHub stats
    try:
        with open('data/github-stats.json', 'r') as f:
            data = json.load(f)
            summary['stats'] = {
                'followers': data.get('profile', {}).get('followers', 0),
                'stars': data.get('stats', {}).get('total_stars', 0),
                'repos': data.get('profile', {}).get('public_repos', 0)
            }
    except:
        pass
    
    # Load news count
    try:
        with open('data/tech-news.json', 'r') as f:
            data = json.load(f)
            summary['news_count'] = len(data.get('stories', []))
    except:
        pass
    
    # Load quote
    try:
        with open('data/quote.json', 'r') as f:
            data = json.load(f)
            summary['quote'] = {
                'text': data.get('quote', '')[:50] + '...' if len(data.get('quote', '')) > 50 else data.get('quote', ''),
                'author': data.get('author', '')
            }
    except:
        pass
    
    # Load weather
    try:
        with open('data/weather.json', 'r') as f:
            data = json.load(f)
            curr = data.get('current', {})
            summary['weather'] = {
                'condition': curr.get('condition', ''),
                'temp': curr.get('temperature_c')
            }
    except:
        pass
    
    # Load trending count
    try:
        with open('data/trending.json', 'r') as f:
            data = json.load(f)
            summary['trending_count'] = len(data.get('trending_repos', []))
    except:
        pass
    
    # Load health checks
    try:
        with open('data/health-checks.json', 'r') as f:
            data = json.load(f)
            for repo, check in data.get('checks', {}).items():
                summary['health_checks'][repo] = check.get('status', 'unknown')
    except:
        pass
    
    # Generate markdown entry
    entry = f"""
## 📅 {date_str}

**Generated at:** {time_str}

### 📊 GitHub Stats
"""
    
    if summary['stats']:
        entry += f"- Followers: {summary['stats']['followers']}\n"
        entry += f"- Total Stars: {summary['stats']['stars']}\n"
        entry += f"- Public Repos: {summary['stats']['repos']}\n"
    else:
        entry += "- *No stats available*\n"
    
    entry += f"\n### 📰 Tech News\n- Fetched {summary['news_count']} stories from Hacker News\n"
    
    entry += "\n### 💬 Quote of the Day\n"
    if summary['quote']:
        entry += f"> \"{summary['quote']['text']}\"\n> — {summary['quote']['author']}\n"
    else:
        entry += "- *No quote available*\n"
    
    entry += "\n### 🌤️ Weather (Toronto)\n"
    if summary['weather']:
        entry += f"- {summary['weather']['condition']}"
        if summary['weather']['temp']:
            entry += f" | {summary['weather']['temp']}°C"
        entry += "\n"
    else:
        entry += "- *No weather data*\n"
    
    entry += f"\n### 🔥 Trending\n- Tracked {summary['trending_count']} trending repos\n"
    
    entry += "\n### 🏥 Health Checks\n"
    if summary['health_checks']:
        for repo, status in summary['health_checks'].items():
            icon = {'healthy': '✅', 'warning': '⚠️', 'error': '❌', 'not_found': '❓'}.get(status, '❓')
            entry += f"- {icon} `{repo}`: {status}\n"
    else:
        entry += "- *No health checks run*\n"
    
    entry += "\n---\n"
    
    # Append to log file
    os.makedirs('logs', exist_ok=True)
    log_file = 'logs/activity.md'
    
    # Read existing content
    existing = ""
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            existing = f.read()
    
    # Create or update log
    if not existing:
        header = """# 📝 Activity Log

Auto-generated daily summaries from Auto Pulse Pro.

---
"""
        existing = header
    
    # Insert new entry after header (most recent first)
    parts = existing.split('---', 1)
    if len(parts) == 2:
        new_content = parts[0] + '---' + entry + parts[1]
    else:
        new_content = existing + entry
    
    with open(log_file, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Daily summary logged for {date_str}")
    print(f"   Stats: {summary['stats']}")
    print(f"   Weather: {summary['weather']}")

if __name__ == '__main__':
    update_log()
