# MoneyMentor Frontend - Development Guide

This guide explains how to develop the MoneyMentor frontend when served from FastAPI instead of using a separate Vite dev server.

## Overview

**Architecture:**
```
Browser → FastAPI (port 8000) → Serves built React app from frontend/dist/
                               → API endpoints at /api/*
```

**Why this approach?**
- ✅ More stable (no Vite dev server issues)
- ✅ Production-like environment
- ✅ Single server to manage
- ✅ No port conflicts
- ✅ Same CORS configuration as production

**Trade-off:**
- ⏱️ Need to rebuild after changes (~2-3 seconds)
- 🚫 No hot module replacement (HMR)

---

## Quick Start

### Option 1: Use the Development Script (Recommended)

From the `moneymentor` directory:

```bash
./dev.sh
```

This script will:
1. Build the frontend
2. Restart FastAPI
3. Open http://localhost:8000 in your browser

### Option 2: Manual Steps

```bash
# 1. Build frontend
cd app/frontend
npm run build

# 2. Start FastAPI
cd ..
source ../venv/bin/activate
export $(cat ../.env | grep -v '^#' | xargs)
python main.py

# 3. Open browser
# Visit: http://localhost:8000
```

---

## Development Workflow

### Making Changes

```bash
# 1. Edit your React components
vim src/components/ChatWindow.tsx

# 2. Rebuild and deploy
./dev.sh

# 3. Refresh browser to see changes
```

### Faster Workflow (No Script)

If you have FastAPI running in one terminal:

```bash
# Terminal 1: Keep FastAPI running
cd moneymentor
source venv/bin/activate
export $(cat .env | grep -v '^#' | xargs)
cd app
python main.py

# Terminal 2: Build frontend as needed
cd moneymentor/app/frontend
npm run deploy    # or npm run build

# Then just refresh browser!
```

---

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatWindow.tsx       # Message display
│   │   ├── ChatInput.tsx        # User input
│   │   ├── MessageBubble.tsx    # Message styling
│   │   └── TypingIndicator.tsx  # Loading state
│   ├── App.tsx                  # Main app
│   ├── main.tsx                 # Entry point
│   ├── types.ts                 # TypeScript types
│   └── index.css                # Tailwind styles
├── dist/                        # Built files (gitignored)
├── package.json
├── vite.config.ts
└── DEVELOPMENT.md               # This file
```

---

## npm Scripts

```json
{
  "start": "vite",          // Vite dev server (if needed)
  "build": "tsc && vite build",  // Build for production
  "deploy": "npm run build ...",  // Build + message
  "preview": "vite preview"  // Preview production build
}
```

**Most used:** `npm run deploy`

---

## Build Output

When you run `npm run build`, Vite creates:

```
dist/
├── index.html           # Main HTML file
├── assets/
│   ├── index-[hash].js  # Bundled JavaScript
│   └── index-[hash].css # Bundled CSS
```

FastAPI serves this directly from the root path.

---

## Debugging

### Frontend Not Loading

**Check 1:** Is the build present?
```bash
ls -la app/frontend/dist/
```

**Check 2:** Is FastAPI running?
```bash
curl http://localhost:8000/api/health
```

**Check 3:** Check FastAPI logs
```bash
# If using dev.sh
tail -f fastapi.log

# Or check console output
```

### API Calls Failing

**Check:** Browser console (F12)
- Look for CORS errors
- Check network tab for failed requests
- Verify API endpoint URLs

**Test API directly:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
```

### Build Errors

**Clear cache and rebuild:**
```bash
cd app/frontend
rm -rf node_modules dist .vite
npm install
npm run build
```

---

## Customizing Components

### Example: Adding a "Clear Chat" Button

1. **Edit App.tsx:**
```typescript
// Add state handler
const clearChat = () => {
  setMessages([{
    id: '1',
    role: 'mentor',
    content: 'Chat cleared. How can I help you?',
    timestamp: new Date()
  }])
}

// Add button in header
<button onClick={clearChat} className="...">
  Clear Chat
</button>
```

2. **Rebuild:**
```bash
./dev.sh
```

3. **Refresh browser**

### Example: Changing Colors

Edit `tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: '#3B82F6',  // Change this!
      accent: '#10B981',
      // ...
    }
  }
}
```

Then: `./dev.sh`

---

## Performance

### Build Times
- **First build:** ~3-5 seconds
- **Subsequent builds:** ~1-2 seconds
- **With TypeScript errors:** Build fails fast

### Optimization Tips
1. Keep components small and focused
2. Use React.memo() for expensive components
3. Lazy load routes if you add routing
4. Monitor bundle size: `npm run build -- --analyze`

---

## Going Back to Vite Dev Server

If you want to use Vite's dev server later:

```bash
cd app/frontend
npm start

# Visit: http://localhost:5173
# (Vite will proxy /api/* to :8000)
```

The proxy is configured in `vite.config.ts`.

---

## Production Deployment

The same workflow works for production!

```bash
# 1. Build frontend
cd app/frontend
npm run build

# 2. Deploy backend
# FastAPI automatically serves frontend/dist/

# 3. Set environment variables
export OPENAI_API_KEY=...
export QDRANT_URL=...

# 4. Start server
python main.py
```

---

## Tips & Tricks

### Auto-rebuild on Save (Advanced)

Use `nodemon` or `watchman`:

```bash
npm install -g nodemon

# Watch for changes and rebuild
nodemon --watch src --ext tsx,ts,css \
  --exec "npm run build"
```

### Quick Test Without FastAPI

```bash
cd app/frontend
npm run preview

# Visit: http://localhost:4173
# (No backend API, but you can test UI)
```

### Browser Extension

Install React DevTools for better debugging.

---

## Common Issues

### Issue: "Cannot GET /"

**Solution:** Frontend not built or FastAPI not finding dist/
```bash
cd app/frontend && npm run build
```

### Issue: API calls return 404

**Solution:** Check CORS and proxy settings
- API should be at `/api/*`
- Check `main.py` CORS configuration

### Issue: Stale content showing

**Solution:** Hard refresh browser
- Mac: `Cmd + Shift + R`
- Windows: `Ctrl + Shift + R`

---

## Questions?

- Check main README.md
- See SETUP_GUIDE.md for backend setup
- Check API_TESTING.md for API examples

---

**Happy Coding!** 💻💸

