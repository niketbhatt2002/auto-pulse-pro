#!/usr/bin/env python3
"""Fetch GitHub user statistics."""

import json
import os
from datetime import datetime
import requests

def fetch_github_stats():
    """Fetch stats from GitHub API."""
    token = os.environ.get('GH_TOKEN')
    username = os.environ.get('GITHUB_USERNAME', 'niketbhatt2002')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Fetch user data
    user_url = f'https://api.github.com/users/{username}'
    user_resp = requests.get(user_url, headers=headers)
    user_data = user_resp.json() if user_resp.status_code == 200 else {}
    
    # Fetch repos
    repos_url = f'https://api.github.com/users/{username}/repos?per_page=100&sort=updated'
    repos_resp = requests.get(repos_url, headers=headers)
    repos_data = repos_resp.json() if repos_resp.status_code == 200 else []
    
    # Calculate stats
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data if isinstance(repo, dict))
    total_forks = sum(repo.get('forks_count', 0) for repo in repos_data if isinstance(repo, dict))
    languages = {}
    for repo in repos_data:
        if isinstance(repo, dict) and repo.get('language'):
            lang = repo['language']
            languages[lang] = languages.get(lang, 0) + 1
    
    top_repos = sorted(
        [r for r in repos_data if isinstance(r, dict)],
        key=lambda x: x.get('stargazers_count', 0),
        reverse=True
    )[:5]
    
    stats = {
        'updated_at': datetime.utcnow().isoformat() + 'Z',
        'username': username,
        'profile': {
            'name': user_data.get('name', username),
            'bio': user_data.get('bio', ''),
            'followers': user_data.get('followers', 0),
            'following': user_data.get('following', 0),
            'public_repos': user_data.get('public_repos', 0),
        },
        'stats': {
            'total_stars': total_stars,
            'total_forks': total_forks,
            'top_languages': dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]),
        },
        'top_repos': [
            {
                'name': repo.get('name', ''),
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'language': repo.get('language', 'Unknown'),
                'url': repo.get('html_url', ''),
            }
            for repo in top_repos
        ]
    }
    
    # Save to file
    os.makedirs('data', exist_ok=True)
    with open('data/github-stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"✅ Updated GitHub stats for {username}")
    print(f"   Followers: {stats['profile']['followers']}")
    print(f"   Total Stars: {total_stars}")
    print(f"   Public Repos: {stats['profile']['public_repos']}")

if __name__ == '__main__':
    fetch_github_stats()
