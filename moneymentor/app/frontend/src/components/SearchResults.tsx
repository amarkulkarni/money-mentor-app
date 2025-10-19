import React from 'react'
import { getToolStyle } from '../constants/toolStyles'

interface Source {
  source: string
  text: string
  score?: number
  relevance_score?: number
}

interface SearchResultsProps {
  query: string
  answer: string
  sources: Source[]
  isLoading: boolean
  onClose: () => void
  onNewSearch: (query: string) => void
}

const SearchResults: React.FC<SearchResultsProps> = ({
  query,
  answer,
  sources,
  isLoading,
  onClose,
  onNewSearch
}) => {
  const [searchInput, setSearchInput] = React.useState('')

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchInput.trim()) {
      onNewSearch(searchInput)
      setSearchInput('')
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-start justify-center overflow-y-auto">
      <div className="min-h-screen w-full flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full my-8">
          {/* Header */}
          <div className="border-b border-gray-200 p-6 flex items-center justify-between bg-gradient-to-r from-blue-50 to-purple-50 rounded-t-2xl">
            <div className="flex-1">
              <h3 className="text-lg font-bold text-gray-800">Search Results</h3>
              <p className="text-sm text-gray-600 mt-1">"{query}"</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Search Bar */}
          <div className="p-6 border-b border-gray-200">
            <form onSubmit={handleSearch} className="flex gap-2">
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder="Search for financial topics..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                type="submit"
                className="px-6 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all"
              >
                Search
              </button>
            </form>
          </div>

          {/* Content */}
          <div className="p-6 max-h-[60vh] overflow-y-auto">
            {isLoading ? (
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
              </div>
            ) : (
              <>
                {/* Answer */}
                <div className="mb-6">
                  <h4 className="text-sm font-semibold text-gray-500 mb-2">ANSWER</h4>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-gray-800 leading-relaxed">{answer}</p>
                  </div>
                </div>

                {/* Sources */}
                {sources && sources.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-gray-500 mb-3">
                      SOURCES ({sources.length})
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {sources.map((source, idx) => {
                        const toolStyle = getToolStyle(source.source)
                        return (
                          <div
                            key={idx}
                            className="flex items-center gap-2 bg-white rounded-full px-3 py-1.5 border border-gray-200 shadow-sm"
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
              </>
            )}
          </div>

          {/* Footer */}
          <div className="border-t border-gray-200 p-4 flex justify-end bg-gray-50 rounded-b-2xl">
            <button
              onClick={onClose}
              className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SearchResults

