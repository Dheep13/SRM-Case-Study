# Admin Configuration Guide

## Overview

This guide explains how to configure the GenAI Learning Assistant system through the admin interface and configuration files.

## Accessing Admin Features

1. **Via UI**: Click the settings icon (⚙️) in the navbar (admin mode required)
2. **Via Files**: Edit `admin_config.json` directly
3. **Via Database**: Modify `system_settings` table in Supabase

## Configuration Priority

1. **Database overrides** (Supabase `system_settings` table) - Highest priority
2. **Config files** (`admin_config.json`)
3. **Environment variables** (`.env` file)
4. **Hardcoded defaults**

## Configuration Categories

### AI Models

Controls the LLM behavior:

- **LLM Model**: Which GPT model to use (gpt-4-turbo-preview, gpt-4o, gpt-3.5-turbo)
- **Temperature**: 0.0-2.0, controls randomness (default: 0.7)
  - Lower = more focused/deterministic
  - Higher = more creative/random
- **Max Tokens**: Response length limit (100-4000, default: 2000)
- **Embeddings Model**: Used for vector search (default: text-embedding-3-small)

### Agents

Controls AI agent behavior:

- **Content Scraper**:
  - `enabled`: Enable/disable agent
  - `max_search_results`: 5-50 results (default: 10)
  - `search_depth`: "basic" or "advanced"
- **Trend Analyzer**:
  - `enabled`: Enable/disable agent
  - `max_trend_items`: 5-50 items (default: 15)
  - `sources`: ["github", "linkedin"]
- **Content Types**: Filter which types of resources to retrieve

### Trending Skills Algorithm

Controls how trending skills are calculated:

- **Trending Threshold**: 0-100 (default: 70)
  - Minimum average trend score to show a skill as "trending"
- **Mention Weight**: 0.0-1.0 (default: 0.5)
  - How much resource mentions contribute to score
- **GitHub Weight**: 0.0-1.0 (default: 0.3)
  - How much GitHub stars/engagement matters
- **LinkedIn Weight**: 0.0-1.0 (default: 0.2)
  - How much LinkedIn activity matters
- **Trend Window**: 7-90 days (default: 30)
  - How far back to look for trend data
- **Recency Decay Factor**: 0.0-1.0 (default: 0.1)
  - Weight newer data more heavily

### Example Trend Score Calculation

```
mention_score = (mentions / max_mentions) * 100
github_score = (stars / 1000) * 10
linkedin_score = (posts / 500) * 10

trend_score = (
    mention_weight * mention_score +
    github_weight * github_score +
    linkedin_weight * linkedin_score
) / (sum of weights)
```

### API Settings

- **GitHub API URL**: Default: https://api.github.com
- **Tavily Enabled**: Enable/disable web search

### RAG Workflow

Controls the Agentic RAG chatbot behavior:

- **Enable Reasoning**: Multi-step reasoning (default: true)
- **Enable Refinement**: Response refinement step (default: true)
- **Confidence Threshold**: 0.0-1.0 (default: 0.7)
  - Minimum confidence to return response without clarification
- **Max Refinement Iterations**: 1-5 (default: 2)
  - Maximum times to refine before giving up

## Fixing Trending Calculation Issues

### Issue: Skills Not Showing as Trending

**Symptoms**: No skills appear in "Trending" despite having data

**Solution**:
1. Lower `trending_threshold` (try 60 instead of 70)
2. Increase weights for sources you have data for
3. Check that trend data is being loaded (run `python load_and_visualize.py`)

### Issue: LinkedIn Engagement Not Counted

**Fixed**: The system now extracts LinkedIn engagement data from trending topics.

### Issue: Scores Too Low

**Solution**:
1. Adjust `min_baseline_score` (default: 50)
2. Adjust weights to favor your data sources
3. Check that resources are being discovered properly

### Issue: Stale Trends

**Solution**:
1. Lower `trend_window_days` to focus on recent data
2. Set `recency_decay_factor` to weight recent trends more (e.g., 0.2)
3. Re-run discovery: `python load_and_visualize.py "your query"`

## Best Practices

### For Trending Skills

1. **Balanced Weights**: Keep weights between 0.2-0.6 for each factor
2. **Not Too Strict**: Trending threshold of 70 is high; consider 60-65
3. **Fresh Data**: Re-run discovery weekly for current trends
4. **Monitor**: Check analytics dashboard for skill visibility

### For AI Models

1. **Temperature**: 0.7 good for balanced responses
   - Lower for factual (0.3-0.5)
   - Higher for creative (0.8-1.2)
2. **Max Tokens**: 2000 sufficient for most queries
   - Increase for longer responses
   - Decrease to reduce costs

### For Agents

1. **Search Results**: More results = slower, but more complete
2. **Disabled Agents**: Disable agents you don't need to save API costs
3. **Content Types**: Include all types for broad discovery

## Troubleshooting

### Settings Not Saving

1. Check Supabase connection in `.env`
2. Verify `system_settings` table exists (run `admin_schema.sql`)
3. Check browser console for errors

### Configuration Not Applied

1. Restart the application (`python api.py`)
2. Clear browser cache
3. Check that changes were saved to database

### Database Errors

1. Ensure Supabase project is active
2. Run `db_integration/admin_schema.sql` in Supabase SQL Editor
3. Check `SUPABASE_URL` and `SUPABASE_KEY` in `.env`

## API Endpoints

- `GET /api/admin/settings` - Get all settings
- `PUT /api/admin/settings` - Update settings
- `POST /api/admin/settings/reset` - Reset to defaults
- `GET /api/admin/audit-log` - Get change history
- `GET /api/admin/health` - Check system health

## Security Notes

- Settings modal requires admin authentication
- Sensitive settings (API keys) are never exposed in UI
- All configuration changes are logged in audit trail
- Export feature excludes sensitive data

## Support

For issues or questions:
1. Check this guide
2. Review audit log for recent changes
3. Check system health endpoint
4. Verify database schema is up to date

