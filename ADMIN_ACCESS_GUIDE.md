# Admin Panel Access Guide

## Quick Access Methods

### Method 1: Double-Click Logo (Easiest)
1. Go to the top-left corner of the app
2. Look for "GenAI Learning Assistant" logo with sparkle icon ✨
3. **Double-click it** (click twice quickly)
4. You should see an alert: "Admin mode enabled!"
5. The ⚙️ settings button and "Admin" menu will appear

### Method 2: Browser Console
1. Open browser Developer Tools (F12)
2. Go to Console tab
3. Type: `localStorage.setItem('isAdmin', 'true')`
4. Press Enter
5. Refresh the page (F5)
6. Admin features will now be visible

### Method 3: Password Login (If implemented)
1. If there's a login button, use it
2. Password is: `admin123`

## What You Should See After Enabling Admin Mode

✅ **Settings Button**: A ⚙️ icon in the top-right navbar (next to student level dropdown)
✅ **Admin Menu**: An "Admin" link in the sidebar
✅ **Settings Modal**: Clicking the ⚙️ icon opens configuration options
✅ **Admin Dashboard**: Clicking "Admin" in sidebar shows system health and logs

## Admin Features Available

1. **Settings Modal** (⚙️ icon):
   - AI Configuration (model, temperature)
   - Trending Algorithm (weights, threshold)
   - RAG Settings (confidence, iterations)
   - Agent Control (enable/disable agents)
   - System Settings

2. **Admin Dashboard** (Admin link in sidebar):
   - System health status
   - Configuration overview
   - Audit log of changes
   - System information

## Troubleshooting

### If you don't see the logo:
- Look for text "GenAI Learning Assistant" with a sparkle icon
- It's in the top-left navbar, next to the menu (☰) button

### If double-click doesn't work:
- Try clicking rapidly 3-4 times
- Wait 3 seconds between attempts
- Use Method 2 (browser console) as backup

### If settings button doesn't appear:
- Make sure isAdmin is set: Check console for `localStorage.getItem('isAdmin')`
- Should return "true"
- If not, use Method 2 to set it manually

### Screen doesn't refresh:
- Press F5 to refresh the page after enabling admin mode

## Verification

After enabling admin mode, you should see:
- ⚙️ Settings button in navbar (top-right)
- "Admin" menu item in sidebar
- Alert message confirming admin mode

If you can't find it, take a screenshot and describe what you see!

