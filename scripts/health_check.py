#!/usr/bin/env python3
"""Health check for user's repositories."""

import json
import os
from datetime import datetime
import requests

def health_check():
    """Check health status of configured repositories."""
    
    token = os.environ.get('GH_TOKEN')
    repos_str = os.environ.get('REPOS_TO_CHECK', '')
    repo_index = int(os.environ.get('REPO_INDEX', 0))
    
    repos = [r.strip() for r in repos_str.split(',') if r.strip()]
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    } if token else {'Accept': 'application/vnd.github.v3+json'}
    
    # Load existing health checks
    health_file = 'data/health-checks.json'
    os.makedirs('data', exist_ok=True)
    
    try:
        with open(health_file, 'r') as f:
            health_data = json.load(f)
    except:
        health_data = {
            'updated_at': '',
            'checks': {}
        }
    
    # Check specific repo based on index
    if repo_index < len(repos):
        repo = repos[repo_index]
        
        try:
            # Fetch repo info
            url = f'https://api.github.com/repos/{repo}'
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                
                # Check for recent activity
                pushed_at = data.get('pushed_at', '')
                if pushed_at:
                    last_push = datetime.fromisoformat(pushed_at.replace('Z', '+00:00'))
                    days_since_push = (datetime.now(last_push.tzinfo) - last_push).days
                else:
                    days_since_push = None
                
                check_result = {
                    'status': 'healthy',
                    'checked_at': datetime.utcnow().isoformat() + 'Z',
                    'details': {
                        'exists': True,
                        'is_private': data.get('private', False),
                        'default_branch': data.get('default_branch', 'main'),
                        'stars': data.get('stargazers_count', 0),
                        'forks': data.get('forks_count', 0),
                        'open_issues': data.get('open_issues_count', 0),
                        'last_push': pushed_at,
                        'days_since_push': days_since_push,
                        'language': data.get('language', 'Unknown'),
                        'size_kb': data.get('size', 0),
                        'has_issues': data.get('has_issues', False),
                        'has_wiki': data.get('has_wiki', False),
                        'has_pages': data.get('has_pages', False),
                    },
                    'warnings': []
                }
                
                # Add warnings
                if days_since_push and days_since_push > 30:
                    check_result['warnings'].append(f'No activity for {days_since_push} days')
                if data.get('open_issues_count', 0) > 10:
                    check_result['warnings'].append(f'{data["open_issues_count"]} open issues')
                if not data.get('description'):
                    check_result['warnings'].append('No repository description')
                
                if check_result['warnings']:
                    check_result['status'] = 'warning'
                    
            elif resp.status_code == 404:
                check_result = {
                    'status': 'not_found',
                    'checked_at': datetime.utcnow().isoformat() + 'Z',
                    'details': {'exists': False},
                    'warnings': ['Repository not found or private']
                }
            else:
                check_result = {
                    'status': 'error',
                    'checked_at': datetime.utcnow().isoformat() + 'Z',
                    'details': {'http_status': resp.status_code},
                    'warnings': [f'API returned status {resp.status_code}']
                }
                
        except Exception as e:
            check_result = {
                'status': 'error',
                'checked_at': datetime.utcnow().isoformat() + 'Z',
                'details': {'error': str(e)},
                'warnings': [f'Check failed: {str(e)}']
            }
        
        health_data['checks'][repo] = check_result
        health_data['updated_at'] = datetime.utcnow().isoformat() + 'Z'
        
        # Save results
        with open(health_file, 'w') as f:
            json.dump(health_data, f, indent=2)
        
        status_icon = {'healthy': '✅', 'warning': '⚠️', 'error': '❌', 'not_found': '❓'}.get(check_result['status'], '❓')
        print(f"{status_icon} Health check for {repo}: {check_result['status'].upper()}")
        
        if check_result.get('details', {}).get('stars') is not None:
            print(f"   Stars: {check_result['details']['stars']}, Forks: {check_result['details']['forks']}")
        
        for warning in check_result.get('warnings', []):
            print(f"   ⚠️ {warning}")
    else:
        print(f"⚠️ Repo index {repo_index} out of range (only {len(repos)} repos configured)")

if __name__ == '__main__':
    health_check()
