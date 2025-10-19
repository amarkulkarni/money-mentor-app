import { Message } from '../types'
import { getToolStyle } from '../constants/toolStyles'

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-3xl ${isUser ? 'w-auto' : 'w-full'}`}>
        {/* Message bubble */}
        <div
          className={`rounded-lg px-4 py-3 ${
            isUser
              ? 'bg-primary text-white'
              : 'bg-gray-100 text-text'
          }`}
        >
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>

        {/* Sources (only for mentor messages) */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-3">
            <p className="text-xs text-gray-500 font-semibold mb-2">
              📚 Sources ({message.sources.length})
            </p>
            <div className="flex flex-wrap gap-2">
              {message.sources.map((source, idx) => {
                const toolStyle = getToolStyle(source.source)
                return (
                  <div
                    key={idx}
                    className="flex items-center gap-2 bg-white rounded-full px-3 py-1.5 border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
                  >
                    <span className="text-sm">{toolStyle.icon}</span>
                    <span 
                      className={`text-xs px-2 py-0.5 rounded-full font-medium text-white bg-gradient-to-r ${toolStyle.gradient}`}
                    >
                      {source.source}
                    </span>
                    {(source.score !== undefined || source.relevance_score !== undefined) && (
                      <span className="text-xs font-mono text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                        {(source.score || source.relevance_score || 0).toFixed(3)}
                      </span>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Timestamp */}
        <div className={`text-xs text-gray-400 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {message.timestamp.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
          })}
        </div>
      </div>
    </div>
  )
}

