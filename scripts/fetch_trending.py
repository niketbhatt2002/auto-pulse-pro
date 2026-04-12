#!/usr/bin/env python3
"""Fetch trending repositories from GitHub."""

import json
import os
from datetime import datetime, timedelta
import requests

def fetch_trending():
    """Fetch trending repos using GitHub Search API."""
    
    # Get repos created in last 7 days with most stars
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    url = (
        f"https://api.github.com/search/repositories"
        f"?q=created:>{week_ago}&sort=stars&order=desc&per_page=10"
    )
    
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        repos = []
        for repo in data.get('items', [])[:10]:
            repos.append({
                'name': repo.get('full_name', ''),
                'description': (repo.get('description') or '')[:100],
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'language': repo.get('language', 'Unknown'),
                'url': repo.get('html_url', ''),
                'created_at': repo.get('created_at', '')
            })
        
        trending_data = {
            'updated_at': datetime.utcnow().isoformat() + 'Z',
            'period': 'weekly',
            'trending_repos': repos
        }
        
    except Exception as e:
        trending_data = {
            'updated_at': datetime.utcnow().isoformat() + 'Z',
            'error': str(e),
            'trending_repos': []
        }
    
    # Save to file
    os.makedirs('data', exist_ok=True)
    with open('data/trending.json', 'w') as f:
        json.dump(trending_data, f, indent=2)
    
    if 'error' not in trending_data:
        print(f"✅ Fetched {len(repos)} trending repos")
        for i, repo in enumerate(repos[:3], 1):
            print(f"   {i}. {repo['name']} ⭐{repo['stars']}")
    else:
        print(f"⚠️ Trending fetch failed: {trending_data['error']}")

if __name__ == '__main__':
    fetch_trending()
