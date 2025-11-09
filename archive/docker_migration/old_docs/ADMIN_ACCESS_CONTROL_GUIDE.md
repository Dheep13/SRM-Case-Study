# Agent Access Control System - Administrator Guide

## 🎯 Overview

The Agent Access Control System provides comprehensive control over your AI agents' behavior, platform access, and security policies. As an administrator, you can:

- **Control Platform Access**: Enable/disable/restrict access to external platforms
- **Manage Agent Permissions**: Configure which agents can access which platforms
- **Set Rate Limits**: Control API usage to prevent quota exhaustion  
- **Block Content**: Filter sensitive or inappropriate content
- **Monitor Activity**: Track all agent access attempts in real-time
- **Test Configurations**: Verify access rules before deploying

## 🔐 Accessing the Control Panel

### Step 1: Enable Admin Mode
1. Double-click the **EvolveIQ** logo in the top navigation bar (twice within 3 seconds)
2. Or click the **Admin** button in the top-right corner
3. An alert will confirm admin mode is enabled

### Step 2: Navigate to Admin Dashboard
1. Click **Admin** in the left sidebar
2. Scroll down to the **Agent Access Control System** section (purple gradient background)
3. You'll see three tabs: **Platforms**, **Agents**, and **Audit Log**

## 📋 Features & Configuration

### 1. Platform Management

**What it does:** Control access to external APIs and services like GitHub, Tavily, Coursera, etc.

#### Platform Configuration Options

| Setting | Description | Values |
|---------|-------------|--------|
| **Access Level** | Overall access permission | `Allowed`, `Restricted`, `Blocked` |
| **Rate Limit** | Max requests per hour | Integer (0 = unlimited) |
| **Allowed Content Types** | Types of content agents can fetch | Comma-separated list |
| **API Endpoints** | Whitelisted URLs agents can access | List of full URLs |
| **Blocked Keywords** | Content filtering keywords | List of words to block |

#### Access Levels Explained

- 🟢 **Allowed**: Full access with no restrictions (except rate limits)
- 🟡 **Restricted**: Limited access, additional checks applied
- 🔴 **Blocked**: No access allowed, all requests denied

#### Example Platform Configuration

**GitHub:**
```
Access Level: Allowed
Rate Limit: 5000 requests/hour
Allowed Content Types: repositories, topics
API Endpoints: 
  - https://api.github.com/search/repositories
  - https://api.github.com/search/topics
Blocked Keywords: private, internal
```

### How to Configure a Platform

1. Navigate to **Platforms** tab
2. Find the platform you want to configure
3. **Change Access Level**: Use the dropdown on the right
4. **Update Rate Limit**: Enter number in "Rate Limit" field
5. **Modify Content Types**: Edit comma-separated list
6. **Add API Endpoints**:
   - Click "+ Add" button
   - Enter full URL (e.g., `https://api.example.com/v1/search`)
   - Click save
7. **Remove Endpoints**: Click "Remove" button next to endpoint
8. **Add Blocked Keywords**:
   - Click "+ Add" under Blocked Keywords
   - Enter keyword to block
9. **Save Changes**: Click "Save Changes" button at top

### 2. Agent Management

**What it does:** Configure individual agent behavior and permissions.

#### Available Agents

| Agent | Purpose | Default Platforms |
|-------|---------|------------------|
| **Content Scraper** | Discovers learning resources | Tavily, Coursera, Udemy, Microsoft, OpenAI, LangChain, Hugging Face |
| **Trend Analysis** | Analyzes industry trends | GitHub, LinkedIn |
| **Orchestrator** | Coordinates all agents | content_scraper, trend_analysis |

#### Agent Configuration Options

| Setting | Description | Typical Values |
|---------|-------------|----------------|
| **Enabled** | Whether agent is active | On/Off |
| **Max Search Results** | Maximum results per query | 10-20 |
| **Timeout** | Max execution time (seconds) | 20-60 |
| **Allowed Platforms** | Platforms agent can access | Checkbox list |

#### How to Configure an Agent

1. Navigate to **Agents** tab
2. Find the agent you want to configure
3. **Enable/Disable**: Toggle the checkbox at top-right
4. **Set Max Results**: Enter number in "Max Search Results" field
5. **Set Timeout**: Enter seconds in "Timeout" field
6. **Change Platforms**:
   - Check/uncheck platforms in the list
   - Only checked platforms will be accessible
7. **Test Access**: Click "Test" button next to a platform to verify access
8. **Save Changes**: Click "Save Changes" button at top

### 3. Audit Log

**What it does:** Monitor all agent access attempts and configuration changes.

#### Log Entry Types

- 🟡 **access_attempt**: An agent tried to access a platform
- 🔵 **config_change**: Admin modified configuration

#### Reading the Audit Log

Each entry shows:
- **Timestamp**: When the event occurred
- **Type**: access_attempt or config_change
- **Agent**: Which agent made the attempt
- **Platform**: Which platform was accessed (or description for config changes)
- **Status**: ✅ Allowed or ❌ Denied

#### Using the Audit Log

1. Navigate to **Audit Log** tab
2. Click **Refresh** to load latest entries
3. Review recent activity
4. Look for denied attempts (red ❌) to identify issues
5. Track configuration changes for compliance

## 🛡️ Security Best Practices

### 1. Platform Security

**Recommended Settings:**

- **Production Environments:**
  ```
  Rate Limits: Conservative (500-1000 req/hour)
  Access Levels: Restricted for third-party platforms
  Blocked Keywords: private, confidential, internal, secret
  ```

- **Development Environments:**
  ```
  Rate Limits: Higher (2000-5000 req/hour)
  Access Levels: Allowed for most platforms
  Blocked Keywords: Minimal filtering
  ```

### 2. Rate Limit Guidelines

| Platform | Free Tier Limit | Recommended Setting |
|----------|----------------|---------------------|
| GitHub | 60/hour (no auth) | 50/hour |
| GitHub | 5000/hour (authenticated) | 1000/hour |
| Tavily | 1000/month | 100/hour |
| OpenAI | Varies by plan | Based on your quota |

### 3. Content Filtering

**Always block these keywords:**
- `password`, `secret`, `token`, `api_key`
- `private`, `confidential`, `internal`
- `admin`, `root`, `sudo`

**Industry-specific blocks:**
- Financial: `ssn`, `credit_card`, `account_number`
- Healthcare: `hipaa`, `phi`, `medical_record`
- Education: `grade`, `student_id`, `exam_answer`

### 4. Agent Permissions

**Principle of Least Privilege:**
- Only grant platforms an agent actually needs
- Content Scraper doesn't need GitHub access
- Trend Analysis doesn't need documentation sites

**Example:**
```
Content Scraper:
  ✅ Tavily (web search)
  ✅ Coursera, Udemy (course data)
  ✅ Microsoft Learn, OpenAI Docs (documentation)
  ❌ GitHub (not needed for content scraping)
  ❌ LinkedIn (not needed for content scraping)

Trend Analysis:
  ✅ GitHub (repository trends)
  ✅ LinkedIn (professional trends)
  ❌ Tavily (not needed for trends)
  ❌ Course platforms (not needed for trends)
```

## 🧪 Testing Access Control

### Test Individual Platform Access

1. Go to **Agents** tab
2. Find the agent you want to test
3. Locate a platform in the "Allowed Platforms" list
4. Click the **Test** button next to the platform
5. A message will appear showing if access is allowed or denied
6. Check the result:
   - ✅ Green "Access ALLOWED" = Configuration is working
   - ❌ Red "Access DENIED" = Check configuration

### Common Test Scenarios

**Test 1: Verify Agent Can Access Required Platform**
```
Agent: content_scraper
Platform: tavily
Expected: ✅ Access ALLOWED
```

**Test 2: Verify Blocked Platform is Denied**
```
Agent: content_scraper
Platform: github (not in allowed list)
Expected: ❌ Access DENIED
```

**Test 3: Verify Blocked Platform Level**
```
Agent: trend_analysis
Platform: reddit (access_level = blocked)
Expected: ❌ Access DENIED
```

## 📊 Common Use Cases

### Use Case 1: Blocking a Platform

**Scenario:** You want to prevent all agents from accessing Reddit.

**Steps:**
1. Go to **Platforms** tab
2. Find "Reddit" platform
3. Change Access Level to **Blocked**
4. Click **Save Changes**
5. Verify in **Audit Log** tab

### Use Case 2: Adding a New API Endpoint

**Scenario:** Your organization has an internal learning portal at `https://learn.company.com/api`

**Steps:**
1. Go to **Platforms** tab
2. Find a similar platform (e.g., "Microsoft Learn")
3. Click "+ Add" under API Endpoints
4. Enter: `https://learn.company.com/api`
5. Update Allowed Content Types if needed (e.g., add "courses")
6. Click **Save Changes**
7. Go to **Agents** tab
8. Enable the platform for Content Scraper agent
9. Test access

### Use Case 3: Reducing Rate Limits

**Scenario:** You're hitting API quota limits and need to reduce usage.

**Steps:**
1. Go to **Platforms** tab
2. For each platform, reduce Rate Limit by 50%
   - Example: GitHub 5000 → 2500
   - Example: Tavily 1000 → 500
3. Click **Save Changes**
4. Monitor **Audit Log** for denied attempts
5. Adjust limits as needed

### Use Case 4: Temporary Agent Disable

**Scenario:** Trend Analysis agent is causing issues, need to disable it temporarily.

**Steps:**
1. Go to **Agents** tab
2. Find "Trend Analysis Agent"
3. Uncheck the **Enabled** checkbox
4. Click **Save Changes**
5. Agent will no longer run during discovery
6. Re-enable when issue is resolved

## 🚨 Troubleshooting

### Issue: "Discovery returns 0 results"

**Possible Causes:**
1. All platforms are blocked
2. Content Scraper agent is disabled
3. Rate limits are set to 0
4. No endpoints configured for platforms

**Solution:**
1. Check **Agents** tab → Content Scraper → Enabled ✓
2. Check **Platforms** tab → Tavily, Coursera, etc. → Access Level = Allowed
3. Check Rate Limits > 0
4. Check API Endpoints are present
5. Click **Test** button to verify access
6. Check **Audit Log** for denied attempts

### Issue: "Access Denied" errors in console

**Possible Causes:**
1. Platform access level is Restricted or Blocked
2. Agent doesn't have platform in allowed list
3. API endpoint not whitelisted
4. Content type not allowed

**Solution:**
1. Go to **Audit Log** tab
2. Find the denied entry
3. Note the Agent and Platform
4. Check platform access level
5. Check agent's allowed platforms list
6. Verify API endpoint is whitelisted
7. Test access after changes

### Issue: "Rate limit exceeded"

**Possible Causes:**
1. Too many requests in short time
2. Rate limit set too low
3. Multiple agents accessing same platform

**Solution:**
1. Check **Platforms** tab → Platform → Rate Limit
2. Increase rate limit value
3. Or reduce **Agents** tab → Max Search Results
4. Or disable one agent temporarily
5. Monitor **Audit Log** for success/failure

### Issue: "Platform returns blocked content"

**Possible Causes:**
1. Content contains blocked keywords
2. Over-aggressive keyword filtering

**Solution:**
1. Check **Platforms** tab → Platform → Blocked Keywords
2. Remove unnecessary keywords
3. Make keywords more specific
4. Test with sample query

## 🔄 Resetting to Defaults

If you need to reset access control to default settings:

**Option 1: Manual Reset**
1. Review default values in table below
2. Go to each platform and restore default values
3. Go to each agent and restore default values
4. Click **Save Changes**

**Option 2: Code-Level Reset** (requires server restart)
1. Stop the backend server
2. Modify `agent_access_control.py` if needed
3. Restart the backend server
4. Configuration will reset to code defaults

### Default Platform Settings

| Platform | Access Level | Rate Limit | Content Types |
|----------|-------------|-----------|---------------|
| GitHub | Allowed | 5000 | repositories, topics |
| Tavily | Allowed | 1000 | web, news |
| Coursera | Allowed | 100 | courses, specializations |
| Udemy | Allowed | 100 | courses |
| Microsoft | Allowed | 200 | documentation, courses |
| OpenAI | Allowed | 1000 | documentation |
| LangChain | Allowed | 500 | documentation |
| Hugging Face | Allowed | 500 | courses, models |
| LinkedIn | Restricted | 50 | professional_posts |
| Reddit | Blocked | 0 | (none) |
| Twitter/X | Blocked | 0 | (none) |

### Default Agent Settings

| Agent | Enabled | Max Results | Timeout | Platforms |
|-------|---------|------------|---------|-----------|
| Content Scraper | Yes | 10 | 30s | tavily, coursera, udemy, microsoft, openai, langchain, huggingface |
| Trend Analysis | Yes | 15 | 20s | github, linkedin |
| Orchestrator | Yes | 25 | 60s | content_scraper, trend_analysis |

## 📞 Support & Documentation

### Additional Resources

- **Agent Access Control Guide**: `AGENT_ACCESS_CONTROL_GUIDE.md`
- **Discovery Fix Summary**: `DISCOVERY_FIX_SUMMARY.md`
- **Admin Guide**: `ADMIN_GUIDE.md`
- **Main README**: `README.md`

### API Endpoints

- Get Configuration: `GET /api/admin/agent-access`
- Update Configuration: `PUT /api/admin/agent-access`
- Get Audit Log: `GET /api/admin/agent-access/audit?limit=100`
- Test Access: `POST /api/admin/agent-access/test`

### Quick Reference Commands

**Test agent access (curl):**
```bash
curl -X POST http://localhost:8000/api/admin/agent-access/test \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "content_scraper",
    "platform": "tavily",
    "endpoint": "https://api.tavily.com/search",
    "content_type": "web"
  }'
```

**Get current configuration (curl):**
```bash
curl http://localhost:8000/api/admin/agent-access
```

---

## 🎓 Summary

The Agent Access Control System provides enterprise-grade security and control over your AI agents. By properly configuring platforms, agents, and security policies, you can:

✅ Protect sensitive data with content filtering  
✅ Control costs with rate limiting  
✅ Ensure compliance with access policies  
✅ Monitor all activity in real-time  
✅ Test configurations before deployment  

**Remember:**
- Save changes after modifications
- Test access after changes
- Monitor audit log regularly
- Follow security best practices
- Document custom configurations

For additional help, refer to the documentation files or contact your system administrator.

---

**Last Updated:** November 8, 2025  
**Version:** 1.0.0  
**Author:** EvolveIQ Development Team

