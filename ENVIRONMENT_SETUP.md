# Environment Variables Setup for Cloud Foundry

## 🎯 Quick Setup

Your `.env` file will be automatically used to set all environment variables in Cloud Foundry!

### Option 1: Automatic (Recommended)

```powershell
# Deploy and set env vars in one go
.\deploy_to_cf.bat
# When prompted, answer 'Y' to set environment variables
```

### Option 2: Set Variables Separately

```powershell
# Just set/update environment variables
.\set_env_vars.bat
```

### Option 3: Verify Current Variables

```powershell
# Check what's currently set in CF
.\verify_env.bat
```

---

## 📋 How It Works

### 1. Your `.env` File Structure

```env
# Comments are ignored (lines starting with #)

# Required variables
OPENAI_API_KEY=sk-proj-xxxxx
TAVILY_API_KEY=tvly-xxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Optional variables
GITHUB_TOKEN=ghp_xxxxx
```

### 2. Script Reads `.env`

The `set_env_vars.bat` script:
- ✅ Reads each line from `.env`
- ✅ Skips comments (lines starting with `#`)
- ✅ Skips empty lines
- ✅ Removes quotes from values
- ✅ Sets each variable in Cloud Foundry
- ✅ Shows progress for each variable
- ✅ Restages app to apply changes

### 3. Variables Are Set in CF

Each variable from `.env` is set using:
```powershell
cf set-env genai-learning-assistant VARIABLE_NAME "value"
```

---

## 🔐 Required Variables

These must be in your `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | `sk-proj-xxxxx` |
| `TAVILY_API_KEY` | Tavily API for web search | `tvly-xxxxx` |
| `SUPABASE_URL` | Your Supabase project URL | `https://xxxxx.supabase.co` |
| `SUPABASE_KEY` | Supabase anonymous key | `eyJhbGci...` |

## 📌 Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub API token for trends | Not set |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith tracing | `false` |
| `LANGCHAIN_API_KEY` | LangSmith API key | Not set |
| `LANGCHAIN_PROJECT` | LangSmith project name | Not set |

---

## 🛠️ Commands

### Set All Variables from `.env`
```powershell
.\set_env_vars.bat
```

### Verify Current Variables
```powershell
.\verify_env.bat
```

### Manually Set One Variable
```powershell
cf set-env genai-learning-assistant VARIABLE_NAME "value"
cf restage genai-learning-assistant
```

### View All Variables
```powershell
cf env genai-learning-assistant
```

### Remove a Variable
```powershell
cf unset-env genai-learning-assistant VARIABLE_NAME
cf restage genai-learning-assistant
```

---

## ⚠️ Important Notes

### 1. `.env` File Security
- ✅ `.env` is in `.gitignore` (never committed)
- ✅ Only exists on your local machine
- ✅ Variables are securely stored in CF

### 2. Quotes in Values
The script automatically handles:
```env
# Both formats work
OPENAI_API_KEY=sk-xxxxx
OPENAI_API_KEY="sk-xxxxx"
```

### 3. Special Characters
If your value contains spaces or special characters, use quotes:
```env
SOME_VAR="value with spaces"
```

### 4. Comments
All these are ignored:
```env
# Full line comment
  # Indented comment

# DISABLED_VAR=some_value  (commented out)
```

---

## 🔄 Update Workflow

### When You Change `.env` Locally

```powershell
# 1. Update your local .env file
# 2. Run the script to sync to CF
.\set_env_vars.bat

# The script will:
# - Read new values from .env
# - Update all variables in CF
# - Restage the app automatically
```

### After Adding New Variables

```powershell
# 1. Add to .env
echo NEW_VARIABLE=new_value >> .env

# 2. Set in CF
.\set_env_vars.bat
```

---

## 🐛 Troubleshooting

### Script Can't Find `.env`
```powershell
# Make sure .env exists
dir .env

# Create from example if missing
copy .env.example .env
# Then edit .env with your actual values
```

### Not Logged In to CF
```powershell
cf login -a https://api.cf.us10-001.hana.ondemand.com -o f8861a98trial
```

### Variables Not Taking Effect
```powershell
# Restage the app
cf restage genai-learning-assistant

# Or restart
cf restart genai-learning-assistant
```

### Check If Variable Is Set
```powershell
cf env genai-learning-assistant | findstr "OPENAI_API_KEY"
```

---

## 📊 Example Workflow

```powershell
# 1. Initial setup - create .env from example
copy .env.example .env

# 2. Edit .env with your actual keys
notepad .env

# 3. Deploy app
.\deploy_to_cf.bat

# 4. When prompted, answer 'Y' to set env vars
# OR run separately:
.\set_env_vars.bat

# 5. Verify everything is set
.\verify_env.bat

# 6. Access your app
# https://genai-learning-assistant.cfapps.us10-001.hana.ondemand.com
```

---

## ✅ Best Practices

1. **Keep `.env` Secure** - Never commit to Git
2. **Use `.env.example`** - Template for others
3. **Verify After Setting** - Run `verify_env.bat`
4. **Update When Needed** - Re-run `set_env_vars.bat` anytime
5. **Document New Vars** - Add to `.env.example` (without values)

---

## 🎉 Summary

You now have **automatic environment variable management**:

- 🔄 Read from `.env` file automatically
- ✨ One command to set all variables
- 🔍 Easy verification
- 🚀 Integrated with deployment

Just maintain your `.env` file locally, and the scripts handle the rest! 🎯



