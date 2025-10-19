import { useState } from 'react'
import HomePage from './components/HomePage'
import LearnPage from './components/LearnPage'
import CertifyPage from './components/CertifyPage'
import ChatPage from './components/ChatPage'
import SearchResults from './components/SearchResults'
import { ChatResponse } from './types'

type Page = 'home' | 'learn' | 'certify' | 'chat'

interface SearchResult {
  query: string
  answer: string
  sources: any[]
}

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home')
  const [searchQuery, setSearchQuery] = useState('')
  const [showSearchResults, setShowSearchResults] = useState(false)
  const [searchResult, setSearchResult] = useState<SearchResult | null>(null)
  const [isSearching, setIsSearching] = useState(false)

  const handleSearch = async (query: string) => {
    if (!query.trim()) return
    
    setSearchQuery(query)
    setShowSearchResults(true)
    setIsSearching(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: query,
          k: 5
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get response')
      }

      const data: ChatResponse = await response.json()

      setSearchResult({
        query,
        answer: data.answer,
        sources: data.sources || []
      })
    } catch (error) {
      console.error('Error:', error)
      setSearchResult({
        query,
        answer: 'Sorry, I encountered an error. Please try again.',
        sources: []
      })
    } finally {
      setIsSearching(false)
    }
  }

  const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    handleSearch(searchQuery)
  }

  return (
    <div className="min-h-screen bg-[#F9FAFB] flex flex-col">
      {/* Header */}
      <header className="relative overflow-hidden border-b border-gray-200/50 shadow-sm bg-gradient-to-r from-blue-50 via-blue-100 to-purple-50">
        {/* Content */}
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {/* Logo and Brand */}
          <div className="flex items-center justify-center mb-4">
            <button
              onClick={() => setCurrentPage('home')}
              className="flex items-center gap-3 hover:opacity-80 transition-opacity"
            >
              <div className="text-4xl">💸</div>
              <div>
                <h1 className="text-3xl md:text-4xl font-bold text-[#1E293B]">
                  MoneyMentor
                </h1>
                <p className="text-sm text-gray-600 font-medium">
                  Learn. Earn. Grow.
                </p>
              </div>
            </button>
          </div>

          {/* Search Bar */}
          <form onSubmit={handleSearchSubmit} className="max-w-2xl mx-auto">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for financial topics..."
                className="w-full px-4 py-2.5 pr-24 rounded-xl border-2 border-white/50 bg-white/80 backdrop-blur-sm focus:outline-none focus:border-blue-300 focus:ring-4 focus:ring-blue-100 transition-all shadow-lg text-sm text-gray-800 placeholder-gray-500"
              />
              <button
                type="submit"
                className="absolute right-1.5 top-1/2 -translate-y-1/2 px-4 py-1.5 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 shadow-md hover:shadow-lg transition-all font-medium flex items-center gap-1.5 text-sm"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Search
              </button>
            </div>
          </form>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {currentPage === 'home' && (
          <HomePage onNavigate={setCurrentPage} />
        )}
        {currentPage === 'learn' && (
          <LearnPage onBack={() => setCurrentPage('home')} />
        )}
        {currentPage === 'certify' && (
          <CertifyPage onBack={() => setCurrentPage('home')} />
        )}
        {currentPage === 'chat' && (
          <ChatPage onBack={() => setCurrentPage('home')} />
        )}
      </main>

      {/* Footer */}
      <footer className="relative overflow-hidden border-t border-gray-200/50 py-6 bg-gradient-to-r from-blue-50/50 via-purple-50/50 to-blue-50/50">
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm text-gray-600">
            MoneyMentor • Powered by GPT-4o-mini & RAG • Not financial advice
          </p>
          <p className="text-xs text-gray-500 mt-2">
            © 2025 MoneyMentor. Built with ❤️ for financial literacy.
          </p>
        </div>
      </footer>

      {/* Search Results Modal */}
      {showSearchResults && searchResult && (
        <SearchResults
          query={searchResult.query}
          answer={searchResult.answer}
          sources={searchResult.sources}
          isLoading={isSearching}
          onClose={() => setShowSearchResults(false)}
          onNewSearch={handleSearch}
        />
      )}
    </div>
  )
}

export default App
