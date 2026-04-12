# 🚀 Auto Pulse Pro

> Your personal automated dashboard that keeps your GitHub contribution graph **dark green** with 10+ meaningful commits daily.

![Auto Updated](https://img.shields.io/badge/auto-updated-brightgreen)
![Commits Per Day](https://img.shields.io/badge/commits%2Fday-10%2B-blue)

## 📊 Live Dashboard

| Section | Last Updated |
|---------|--------------|
| [📈 GitHub Stats](data/github-stats.json) | Auto-updates 2x daily |
| [📰 Tech News](data/tech-news.json) | Fresh headlines daily |
| [💬 Daily Quote](data/quote.json) | New inspiration daily |
| [🌤️ Weather Log](data/weather.json) | Toronto conditions |
| [🔥 Trending Repos](data/trending.json) | What's hot on GitHub |
| [🏥 Health Checks](data/health-checks.json) | Your repos status |
| [📝 Activity Log](logs/activity.md) | Full history |

---

## ⚡ Quick Setup (5 minutes)

### Step 1: Fork or Clone This Repo

```bash
git clone https://github.com/YOUR_USERNAME/auto-pulse-pro.git
```

### Step 2: Create a GitHub Personal Access Token

1. Go to [GitHub Settings → Developer Settings → Personal Access Tokens → Tokens (classic)](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Give it a name: `Auto Pulse Pro`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:user` (Read user profile data)
5. Click **Generate token**
6. **Copy the token** (you won't see it again!)

### Step 3: Add the Token to Your Repo

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Name: `GH_TOKEN`
4. Value: *paste your token*
5. Click **Add secret**

### Step 4: Configure Your Repos (Optional)

Edit `.github/workflows/daily-pulse.yml` and update the `REPOS_TO_CHECK` line with your repositories:

```yaml
REPOS_TO_CHECK: "your-username/repo1,your-username/repo2,your-username/repo3"
```

### Step 5: Enable GitHub Actions

1. Go to your repo → **Actions** tab
2. Click **"I understand my workflows, go ahead and enable them"**

**Done!** 🎉 The automation will start running on schedule.

---

## 🕐 Commit Schedule

| Time (UTC) | Commit | Content |
|------------|--------|---------|
| 06:00 | 🌅 Morning Stats | GitHub profile snapshot |
| 07:00 | 📰 Tech News | Top Hacker News stories |
| 08:00 | 💬 Daily Quote | Programming wisdom |
| 09:00 | 🏥 Health Check 1 | First repo status |
| 10:00 | 🏥 Health Check 2 | Second repo status |
| 11:00 | 🏥 Health Check 3 | Third repo status |
| 14:00 | 📊 Stats Update | Midday refresh |
| 17:00 | 🌤️ Weather Log | Toronto conditions |
| 20:00 | 🔥 Trending | Hot repos today |
| 23:00 | 📝 Daily Summary | Changelog update |

**Result: 10 commits/day, 7 days/week = Dark green contribution graph!**

---

## 🔧 Manual Trigger

Want to test it immediately? 

1. Go to **Actions** → **Daily Pulse** 
2. Click **"Run workflow"** → **"Run workflow"**

---

## 📁 Project Structure

```
auto-pulse-pro/
├── .github/workflows/
│   └── daily-pulse.yml      # GitHub Actions scheduler
├── scripts/
│   ├── fetch_stats.py       # GitHub stats fetcher
│   ├── fetch_news.py        # Hacker News fetcher
│   ├── fetch_quote.py       # Quote fetcher
│   ├── fetch_weather.py     # Weather fetcher
│   ├── fetch_trending.py    # Trending repos fetcher
│   ├── health_check.py      # Repo health checker
│   └── update_log.py        # Activity logger
├── data/                    # Auto-updated JSON files
├── logs/                    # Activity history
└── README.md
```

---

## ⚠️ Important Notes

- All data is **real and meaningful** - not fake commits
- GitHub Actions are **free** for public repos
- Private repos get 2,000 minutes/month free
- Each workflow run uses ~1 minute

---

## 📜 License

MIT - Do whatever you want with it!

---

**Made with 💚 for your GitHub graph**
