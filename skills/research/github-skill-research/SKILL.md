---
name: github-skill-research
description: How to search GitHub for AI agent skills and specialized repositories (screenwriting, filmmaking, etc.) - handles misleading topic names and rate limits
---

# GitHub Skill/Repo Research Workflow

## When to Use
When asked to search GitHub for skills, repositories, or code related to a specific domain (especially AI agent skills, screenwriting, filmmaking, or specialized topics).

## Key Learnings (from screenwriting/filmmaking research)

### GitHub Topics Don't Always Mean What You Think
- `director` topic → software load balancing (Varnish DNS director), NOT film director
- `screenwriting` → actual screenwriting software/tools
- `filmmaking` → production tools, storyboarding, AI video
- `openclaw-skills` / `claude-skills` → AI agent skill repositories

### Effective Search Strategy

1. **Start with topic pages** (avoids rate limits):
   ```
   https://github.com/topics/screenwriting
   https://github.com/topics/filmmaking
   https://github.com/topics/openclaw-skills
   ```

2. **If topic pages are empty or insufficient**, try search:
   ```
   https://github.com/search?q=screenwriting+OR+filmmaking+skills&type=repositories&sort=stars
   ```

3. **For AI agent skills specifically**, check:
   - `openclaw-skills` topic (655 repos)
   - `claude-skills` topic
   - Search with: `site:github.com skills screenwriting filmmaking`

### GitHub Rate Limit Handling
- Topic pages work when direct search hits "Too many requests"
- Anonymous search has lower limits; wait a few minutes if rate limited
- Sort by stars by appending `&sort=stars&order=desc`

### Relevant Topic URLs
| Domain | Topic URL |
|--------|-----------|
| Screenwriting | https://github.com/topics/screenwriting |
| Filmmaking | https://github.com/topics/filmmaking |
| Storyboarding | https://github.com/topics/storyboard |
| AI Skills | https://github.com/topics/openclaw-skills |
| Claude Skills | https://github.com/topics/claude-skills |

### Screenwriting/Filmmaking Repo Star Rankings (2026-04)
1. **wonderunit/storyboarder** - 3.6k ⭐ (storyboard visualization)
2. **storytold/artcraft** - 1.5k ⭐ (AI filmmaking engine)
3. **HITsz-TMG/AIGC-Claw** - 1.1k ⭐ (OpenClaw AIGC filmmaking skill)
4. **rnkn/fountain-mode** - 436 ⭐ (Emacs screenplay mode)
5. **piersdeseilligny/betterfountain** - 429 ⭐ (VS Code screenplay extension)

## Workflow
1. Check topic page first (lower rate limit risk)
2. Scroll to see top repos sorted by stars
3. Note: Most stars = most popular/recommended
4. If topic page empty, try search with domain keywords + "skills"
5. Document findings with star counts and descriptions
