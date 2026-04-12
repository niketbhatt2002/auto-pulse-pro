#!/usr/bin/env python3
"""Fetch top tech news from Hacker News."""

import json
import os
from datetime import datetime
import requests

def fetch_tech_news():
    """Fetch top stories from Hacker News API."""
    
    # Get top story IDs
    top_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    resp = requests.get(top_url)
    story_ids = resp.json()[:10] if resp.status_code == 200 else []
    
    stories = []
    for story_id in story_ids:
        story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
        story_resp = requests.get(story_url)
        if story_resp.status_code == 200:
            story = story_resp.json()
            if story and story.get('title'):
                stories.append({
                    'title': story.get('title', ''),
                    'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    'score': story.get('score', 0),
                    'comments': story.get('descendants', 0),
                    'by': story.get('by', 'anonymous'),
                    'hn_link': f"https://news.ycombinator.com/item?id={story_id}"
                })
    
    news_data = {
        'updated_at': datetime.utcnow().isoformat() + 'Z',
        'source': 'Hacker News',
        'stories': stories
    }
    
    # Save to file
    os.makedirs('data', exist_ok=True)
    with open('data/tech-news.json', 'w') as f:
        json.dump(news_data, f, indent=2)
    
    print(f"✅ Fetched {len(stories)} tech news stories")
    for i, story in enumerate(stories[:3], 1):
        print(f"   {i}. {story['title'][:50]}...")

if __name__ == '__main__':
    fetch_tech_news()
