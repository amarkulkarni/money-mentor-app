import { Message } from '../types'

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
          <div className="mt-2 space-y-2">
            <p className="text-xs text-gray-500 font-semibold">
              📚 Sources ({message.sources.length})
            </p>
            <div className="space-y-2">
              {message.sources.map((source, idx) => (
                <div
                  key={idx}
                  className="bg-gray-50 rounded-md p-3 border border-gray-200"
                >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-medium text-accent">
                    {source.source}
                  </span>
                  {(source.score !== undefined || source.relevance_score !== undefined) && (
                    <span className="text-xs text-gray-400">
                      Score: {(source.score || source.relevance_score || 0).toFixed(3)}
                    </span>
                  )}
                </div>
                  <p className="text-xs text-gray-600 line-clamp-2">
                    {source.text}
                  </p>
                </div>
              ))}
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

