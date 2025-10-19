import { useState } from 'react'
import ChatWindow from './components/ChatWindow'
import ChatInput from './components/ChatInput'
import SuggestionPrompts from './components/SuggestionPrompts'
import { Message, ChatResponse } from './types'

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Call API
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: content,
          k: 5
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get response')
      }

      const data: ChatResponse = await response.json()

      // Add mentor response
      const mentorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'mentor',
        content: data.answer,
        sources: data.sources,
        tool: data.tool,
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, mentorMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'mentor',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-purple-50/30 to-blue-50/30 flex flex-col">
      {/* Header */}
      <header className="relative overflow-hidden border-b border-gray-200/50 shadow-sm">
        {/* Notion-inspired gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-orange-50 via-purple-50 to-blue-50"></div>
        
        {/* Content */}
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-orange-600 via-purple-600 to-blue-600 bg-clip-text text-transparent">
            💸 MoneyMentor — Learn. Earn. Grow.
          </h1>
          <p className="text-sm text-gray-600 mt-2 font-medium">
            Your AI-powered financial advisor
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col">
        <div className="flex-1 bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col overflow-hidden">
          {/* Show suggestions only when chat is empty */}
          {messages.length === 0 && (
            <div className="border-b border-gray-200">
              <SuggestionPrompts onSelectSuggestion={handleSendMessage} />
            </div>
          )}
          
          <ChatWindow messages={messages} isLoading={isLoading} />
          
          <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
        </div>
      </main>

      {/* Footer */}
      <footer className="relative overflow-hidden border-t border-gray-200/50 py-4">
        {/* Subtle gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-orange-50/50 via-purple-50/50 to-blue-50/50"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-600">
          MoneyMentor • Powered by GPT-4o-mini & RAG • Not financial advice
        </div>
      </footer>
    </div>
  )
}

export default App
