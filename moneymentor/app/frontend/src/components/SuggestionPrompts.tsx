import React from 'react'
import { TOOL_STYLES, getMultiToolGradient } from '../constants/toolStyles'

interface Suggestion {
  id: string
  text: string
  icon: string
  tools: string[]
}

interface SuggestionPromptsProps {
  onSelectSuggestion: (text: string) => void
}

const suggestions: Suggestion[] = [
  {
    id: '1',
    text: 'What is inflation and what is the current inflation rate?',
    icon: '📊',
    tools: ['RAG', 'Tavily']
  },
  {
    id: '2',
    text: 'If I invest $500 monthly at 7% for 20 years, how much will I have?',
    icon: '💰',
    tools: ['Calculator']
  },
  {
    id: '3',
    text: 'Explain compound interest and calculate returns if I invest $1000 at current rates for 5 years',
    icon: '🚀',
    tools: ['RAG', 'Tavily', 'Calculator']
  },
  {
    id: '4',
    text: "What's a 401k and what are today's contribution limits?",
    icon: '🏦',
    tools: ['RAG', 'Tavily']
  }
]

const SuggestionPrompts: React.FC<SuggestionPromptsProps> = ({ onSelectSuggestion }) => {
  return (
    <div className="p-6 space-y-4">
      <div className="text-center mb-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-2">
          Try these multi-tool queries
        </h2>
        <p className="text-sm text-gray-500">
          Click a suggestion to see how MoneyMentor combines different tools
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {suggestions.map((suggestion) => {
          const gradientColor = getMultiToolGradient(suggestion.tools)
          return (
            <button
              key={suggestion.id}
              onClick={() => onSelectSuggestion(suggestion.text)}
              className="group relative bg-white border-2 border-gray-200 rounded-xl p-4 text-left transition-all duration-200 hover:border-transparent hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]"
            >
              {/* Gradient border on hover */}
              <div className={`absolute inset-0 rounded-xl bg-gradient-to-r ${gradientColor} opacity-0 group-hover:opacity-100 transition-opacity duration-200 -z-10`} 
                   style={{ padding: '2px' }}>
                <div className="bg-white rounded-xl h-full w-full" />
              </div>

              <div className="flex items-start gap-3">
                <span className="text-3xl flex-shrink-0 mt-1">{suggestion.icon}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-800 mb-2 line-clamp-2">
                    {suggestion.text}
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {suggestion.tools.map((tool, index) => {
                      const toolStyle = TOOL_STYLES[tool.toLowerCase()] || TOOL_STYLES.default
                      return (
                        <span
                          key={index}
                          className={`text-xs px-2 py-1 rounded-full font-medium bg-gradient-to-r ${toolStyle.gradient} text-white`}
                        >
                          {tool}
                        </span>
                      )
                    })}
                  </div>
                </div>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default SuggestionPrompts

