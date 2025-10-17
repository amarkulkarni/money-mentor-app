# MoneyMentor Frontend

Beautiful React + Vite + Tailwind CSS frontend for MoneyMentor AI financial advisor.

## Features

- 💬 Real-time chat interface with AI financial advisor
- 🎨 Beautiful UI with Tailwind CSS (muted palette)
- 📚 Source citations for every answer
- ⚡ Fast development with Vite + HMR
- 📱 Responsive design
- 🔄 Loading states and typing indicators
- 🎯 TypeScript for type safety

## Quick Start

### 1. Install Dependencies

```bash
cd app/frontend
npm install
```

### 2. Start Development Server

```bash
npm start
```

The app will open at `http://localhost:5173`

Make sure the backend API is running at `http://localhost:8000`

### 3. Build for Production

```bash
npm run build
```

This creates optimized files in `dist/` folder, which FastAPI serves.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatWindow.tsx       # Message display area
│   │   ├── ChatInput.tsx        # Input field + send button
│   │   ├── MessageBubble.tsx    # Individual message styling
│   │   └── TypingIndicator.tsx  # Loading animation
│   ├── App.tsx                  # Main app component
│   ├── main.tsx                 # Entry point
│   ├── types.ts                 # TypeScript interfaces
│   └── index.css                # Global styles + Tailwind
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## API Integration

The frontend connects to the FastAPI backend:

- **Development**: Vite proxy forwards `/api/*` to `http://localhost:8000`
- **Production**: FastAPI serves frontend from `frontend/dist/`

### API Endpoints Used

- `POST /api/chat` - Send question, get AI answer with sources

## Color Palette

```css
Primary (Blue):    #3B82F6
Accent (Mint):     #10B981
Background:        #F9FAFB
Text:              #1E293B
```

## Components

### App.tsx
Main application with header, chat window, and footer.

### ChatWindow
Displays conversation history with auto-scroll and typing indicator.

### ChatInput
Text input with Enter-to-send and disabled state during loading.

### MessageBubble
Renders user/mentor messages with sources and timestamps.

### TypingIndicator
Animated dots showing the AI is "thinking".

## Development

### Available Scripts

```bash
npm start      # Start dev server with HMR
npm run build  # Build for production
npm run preview # Preview production build
```

### Adding New Features

1. Add new components in `src/components/`
2. Import into `App.tsx`
3. Update types in `src/types.ts` if needed
4. Style with Tailwind classes

## Deployment

The frontend is automatically served by FastAPI when built:

```bash
# Build frontend
cd app/frontend
npm run build

# Start FastAPI (serves frontend at /)
cd ../
python main.py

# Visit http://localhost:8000
```

## Troubleshooting

### Port 5173 already in use
```bash
# Kill the process
lsof -ti:5173 | xargs kill -9
```

### API not connecting
1. Ensure FastAPI is running on port 8000
2. Check Vite proxy configuration in `vite.config.ts`
3. Check browser console for CORS errors

### Build fails
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

**MoneyMentor Frontend** - Your AI Financial Companion 💸
