---
name: github-api-research-fallback
description: Use GitHub API as fallback when web search/scraping is blocked by bot detection. Reliable for finding AI/ML tools, prompts, workflows, and repositories.
---

# GitHub API Research Workflow

## When to Use

When web search/scraping fails due to bot detection (Google, Bing, etc.), use the GitHub API as a reliable fallback for finding AI/ML tools, prompts, and workflows.

## Core Approach

### 1. Search GitHub Repositories

```python
import requests

url = f"https://api.github.com/search/repositories?q={query}&sort=updated&per_page=5"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers, timeout=10)
data = response.json()
```

### 2. Get Repository Details

```python
# Get repo info
url = f"https://api.github.com/repos/{owner}/{repo}"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
repo_data = r.json()
# Fields: description, stargazers_count, topics, updated_at, html_url
```

### 3. Get README Content

```python
import base64

url = f"https://api.github.com/repos/{owner}/{repo}/readme"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
data = r.json()
if 'content' in data:
    content = base64.b64decode(data['content']).decode('utf-8')
```

### 4. Get Recent Commits

```python
url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=5"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
commits = r.json()
latest_message = commits[0]['commit']['message']
```

## Search Query Patterns

- `AI video prompt engineering` - for prompt tips
- `seedance video generation` - for Seedance-specific
- `AI short drama script adaptation` - for script workflows
- `AI storyboard generation workflow` - for storyboarding
- `AI video style consistency` - for consistency tools
- `character consistency AI video` - for character locking

## Quality Indicators

- Stars count (>100 is generally good quality)
- Recent updates (check `updated_at`)
- Description clarity
- Topics tags

## Limitations

- GitHub API rate limits: 10 requests/minute for unauthenticated
- Only finds GitHub-hosted content
- May miss non-repo sources (blogs, official docs)

## Example: Full Research Pipeline

```python
import requests
import base64
from collections import defaultdict

def search_github_topics(topics):
    """Search multiple topics and aggregate results"""
    all_results = []
    
    for topic in topics:
        try:
            url = f"https://api.github.com/search/repositories?q={topic.replace(' ', '+')}&sort=updated&per_page=5"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            data = r.json()
            
            for item in data.get('items', []):
                all_results.append({
                    'search_topic': topic,
                    'name': item['full_name'],
                    'description': item['description'],
                    'url': item['html_url'],
                    'stars': item['stargazers_count']
                })
        except Exception as e:
            print(f"Error searching {topic}: {e}")
    
    return all_results
```
