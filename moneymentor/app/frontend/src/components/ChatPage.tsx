import React, { useState } from 'react'
import ChatWindow from './ChatWindow'
import ChatInput from './ChatInput'
import SuggestionPrompts from './SuggestionPrompts'
import { Message, ChatResponse } from '../types'

interface ChatPageProps {
  onBack: () => void
}

const ChatPage: React.FC<ChatPageProps> = ({ onBack }) => {
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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 h-full flex flex-col">
      {/* Back Button */}
      <button
        onClick={onBack}
        className="mb-4 flex items-center gap-2 text-blue-600 hover:text-blue-700 transition-colors"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span className="font-medium">Back to Home</span>
      </button>

      {/* Chat Container */}
      <div className="flex-1 bg-white rounded-2xl shadow-xl border border-gray-200 flex flex-col overflow-hidden">
        {/* Show suggestions only when chat is empty */}
        {messages.length === 0 && (
          <div className="border-b border-gray-200">
            <SuggestionPrompts onSelectSuggestion={handleSendMessage} />
          </div>
        )}
        
        <ChatWindow messages={messages} isLoading={isLoading} />
        
        <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  )
}

export default ChatPage

