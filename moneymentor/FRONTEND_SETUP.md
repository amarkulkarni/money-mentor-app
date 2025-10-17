# MoneyMentor Frontend Setup Guide

Quick guide to get the React frontend running.

## Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

## Step 1: Install Dependencies

```bash
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor/app/frontend
npm install
```

This will install:
- React 18
- Vite (build tool)
- Tailwind CSS (styling)
- TypeScript
- All necessary dev dependencies

**Time**: ~2-3 minutes

## Step 2: Start Development Server

```bash
npm start
```

This starts the Vite dev server at `http://localhost:5173`

Features:
- ✅ Hot Module Replacement (HMR)
- ✅ Instant updates on file save
- ✅ API proxy to backend
- ✅ Fast refresh

## Step 3: Test the App

1. Open browser: `http://localhost:5173`
2. You should see the MoneyMentor chat interface
3. Type a question: "How do I create a budget?"
4. Watch it send to backend, show typing indicator, then display answer

## Step 4: Build for Production

When ready to deploy:

```bash
npm run build
```

This creates optimized files in `frontend/dist/`

Then restart FastAPI to serve the frontend:

```bash
cd ../
python main.py
```

Visit `http://localhost:8000` - the frontend is now served by FastAPI!

## Features You'll See

✅ **Header**: "💸 MoneyMentor — Learn. Earn. Grow."
✅ **Chat Interface**: Clean, modern design
✅ **User Messages**: Blue bubbles on right
✅ **AI Responses**: Gray bubbles on left with sources
✅ **Typing Indicator**: Animated dots while waiting
✅ **Source Citations**: Expandable source snippets
✅ **Timestamps**: On each message
✅ **Responsive**: Works on mobile/tablet/desktop

## Color Palette

- **Primary** (Blue): #3B82F6
- **Accent** (Mint): #10B981  
- **Background**: #F9FAFB
- **Text**: #1E293B

## Troubleshooting

### Issue: npm install fails

```bash
# Try with legacy peer deps
npm install --legacy-peer-deps
```

### Issue: Port 5173 already in use

```bash
# Kill existing process
lsof -ti:5173 | xargs kill -9
```

### Issue: API calls failing

Make sure:
1. Backend is running: `curl http://localhost:8000/api/health`
2. Virtual env activated
3. Environment variables loaded

### Issue: Blank page after build

Check that:
1. Build completed: `ls frontend/dist/`
2. FastAPI is serving static files (check main.py)
3. Visit root URL, not /docs

## Development Workflow

### Make Changes

1. Edit files in `frontend/src/`
2. Save - changes appear instantly
3. Check browser console for errors
4. Use React DevTools for debugging

### Add New Features

```typescript
// Example: Add a "Clear Chat" button
// In App.tsx:
const clearChat = () => {
  setMessages([initialMessage])
}

// Add button to UI
<button onClick={clearChat}>Clear</button>
```

### Customize Styling

```typescript
// Use Tailwind classes:
className="bg-primary hover:bg-blue-600 text-white px-4 py-2 rounded-lg"

// Or extend theme in tailwind.config.js
```

## Production Checklist

Before deploying:

- [ ] Run `npm run build` successfully
- [ ] Test production build with `npm run preview`
- [ ] Check all API endpoints work
- [ ] Test on different browsers
- [ ] Test mobile responsiveness
- [ ] Check console for errors
- [ ] Verify sources display correctly
- [ ] Test loading states

## Next Steps

1. **Customize the UI**: Edit components in `src/components/`
2. **Add Features**: Conversation history, export chat, etc.
3. **Improve UX**: Add animations, sound effects, etc.
4. **Analytics**: Track user interactions
5. **Authentication**: Add user accounts

---

**Happy coding!** 💻
