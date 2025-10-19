import React from 'react'

interface HomePageProps {
  onNavigate: (page: 'learn' | 'certify' | 'chat') => void
}

const HomePage: React.FC<HomePageProps> = ({ onNavigate }) => {
  const tiles = [
    {
      id: 'learn',
      icon: '📘',
      title: 'Learn Financial Basics',
      description: 'Master essential money management skills',
      color: 'from-blue-500 to-blue-600',
      hoverColor: 'hover:from-blue-600 hover:to-blue-700'
    },
    {
      id: 'certify',
      icon: '🎓',
      title: 'Get Certified',
      description: 'Prove your financial literacy skills',
      color: 'from-emerald-500 to-emerald-600',
      hoverColor: 'hover:from-emerald-600 hover:to-emerald-700'
    },
    {
      id: 'chat',
      icon: '💬',
      title: 'Ask MoneyMentor AI',
      description: 'Get instant answers to your questions',
      color: 'from-purple-500 to-purple-600',
      hoverColor: 'hover:from-purple-600 hover:to-purple-700'
    }
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Welcome Message */}
      <div className="text-center mb-12">
        <p className="text-lg text-gray-700 max-w-2xl mx-auto font-medium">
          💰 Ready to level up your financial skills? Choose your path and start your adventure today! 🚀
        </p>
      </div>

      {/* Tiles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {tiles.map((tile) => (
          <button
            key={tile.id}
            onClick={() => onNavigate(tile.id as 'learn' | 'certify' | 'chat')}
            className="group relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:scale-105 active:scale-100 overflow-hidden"
          >
            {/* Gradient Background */}
            <div className={`absolute inset-0 bg-gradient-to-br ${tile.color} ${tile.hoverColor} opacity-0 group-hover:opacity-10 transition-opacity duration-300`}></div>
            
            {/* Content */}
            <div className="relative p-8 flex flex-col items-center text-center space-y-4">
              <div className="text-6xl mb-2">{tile.icon}</div>
              <h3 className="text-2xl font-bold text-gray-800">{tile.title}</h3>
              <p className="text-gray-600">{tile.description}</p>
              
              {/* Arrow Icon */}
              <div className={`mt-4 w-12 h-12 rounded-full bg-gradient-to-br ${tile.color} flex items-center justify-center text-white transform group-hover:translate-x-1 transition-transform`}>
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* Quick Stats */}
      <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
        <div className="bg-white rounded-xl p-6 shadow-md">
          <div className="text-3xl font-bold text-blue-600">5</div>
          <div className="text-gray-600 mt-2">Learning Chapters</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-md">
          <div className="text-3xl font-bold text-emerald-600">AI-Powered</div>
          <div className="text-gray-600 mt-2">Smart Assistant</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-md">
          <div className="text-3xl font-bold text-purple-600">Free</div>
          <div className="text-gray-600 mt-2">Always & Forever</div>
        </div>
      </div>
    </div>
  )
}

export default HomePage

