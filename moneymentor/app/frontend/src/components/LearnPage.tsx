import React, { useState } from 'react'

interface LearnPageProps {
  onBack: () => void
}

const chapters = [
  {
    id: 1,
    title: '💰 Chapter 1: Introduction to Money',
    content: `Understanding money is the first step to financial success. Money is a medium of exchange that allows us to buy goods and services. In this chapter, you'll learn about:

• The history and evolution of money
• Different forms of money (cash, digital, cryptocurrency)
• How money flows in the economy
• The importance of financial literacy

Money isn't just about earning—it's about making smart decisions with what you have. Whether you're spending, saving, or investing, understanding the fundamentals will help you build a secure financial future.`
  },
  {
    id: 2,
    title: '📊 Chapter 2: Budgeting Basics',
    content: `A budget is your financial roadmap. It helps you track income and expenses to reach your goals. Key concepts include:

• The 50/30/20 rule: 50% needs, 30% wants, 20% savings
• Tracking your spending habits
• Creating a realistic monthly budget
• Using budgeting tools and apps
• Adjusting your budget as life changes

Remember: A budget isn't about restriction—it's about conscious choices. When you know where your money goes, you gain control over your financial destiny.`
  },
  {
    id: 3,
    title: '🏦 Chapter 3: Saving & Emergency Funds',
    content: `Saving money creates a safety net and opens opportunities. Learn how to build financial security:

• Why you need an emergency fund (3-6 months of expenses)
• The power of compound interest
• Different types of savings accounts
• Setting and achieving savings goals
• Automating your savings

Start small if needed. Even $10 a week adds up to $520 a year! The key is consistency and making saving a non-negotiable habit.`
  },
  {
    id: 4,
    title: '💳 Chapter 4: Managing Debt Wisely',
    content: `Not all debt is bad, but managing it poorly can hurt your financial health. Understand:

• Good debt vs. bad debt
• How credit cards work and interest rates
• The snowball vs. avalanche debt repayment methods
• Your credit score and why it matters
• Avoiding predatory lending

Smart debt management means using credit strategically, paying on time, and avoiding high-interest debt traps. Your future self will thank you!`
  },
  {
    id: 5,
    title: '📈 Chapter 5: Investing for the Future',
    content: `Investing grows your wealth over time. Start your investment journey by learning:

• The difference between saving and investing
• Stocks, bonds, and mutual funds explained
• The power of compound growth
• Risk vs. reward: diversification basics
• Starting with retirement accounts (401k, IRA)

You don't need to be rich to invest—you invest to become rich. Time in the market beats timing the market. Start early, stay consistent, and watch your money grow!`
  }
]

const LearnPage: React.FC<LearnPageProps> = ({ onBack }) => {
  const [currentChapter, setCurrentChapter] = useState(0)

  const handleNext = () => {
    if (currentChapter < chapters.length - 1) {
      setCurrentChapter(currentChapter + 1)
    }
  }

  const handlePrevious = () => {
    if (currentChapter > 0) {
      setCurrentChapter(currentChapter - 1)
    }
  }

  const chapter = chapters[currentChapter]

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <button
        onClick={onBack}
        className="mb-6 flex items-center gap-2 text-blue-600 hover:text-blue-700 transition-colors"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span className="font-medium">Back to Home</span>
      </button>

      {/* Chapter Content */}
      <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12">
        {/* Progress Indicator */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-600">
              Chapter {currentChapter + 1} of {chapters.length}
            </span>
            <span className="text-sm font-medium text-blue-600">
              {Math.round(((currentChapter + 1) / chapters.length) * 100)}% Complete
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${((currentChapter + 1) / chapters.length) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Chapter Title */}
        <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-6">
          {chapter.title}
        </h2>

        {/* Chapter Content */}
        <div className="prose prose-lg max-w-none">
          <p className="text-gray-700 leading-relaxed whitespace-pre-line">
            {chapter.content}
          </p>
        </div>

        {/* Navigation Buttons */}
        <div className="flex justify-between items-center mt-12 pt-8 border-t border-gray-200">
          <button
            onClick={handlePrevious}
            disabled={currentChapter === 0}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
              currentChapter === 0
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:shadow-md'
            }`}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Previous
          </button>

          {currentChapter === chapters.length - 1 ? (
            <button
              onClick={onBack}
              className="flex items-center gap-2 px-6 py-3 rounded-lg font-medium bg-gradient-to-r from-emerald-500 to-emerald-600 text-white hover:from-emerald-600 hover:to-emerald-700 shadow-md hover:shadow-lg transition-all"
            >
              Complete Course 🎉
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="flex items-center gap-2 px-6 py-3 rounded-lg font-medium bg-gradient-to-r from-blue-500 to-blue-600 text-white hover:from-blue-600 hover:to-blue-700 shadow-md hover:shadow-lg transition-all"
            >
              Next
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Chapter List */}
      <div className="mt-8 bg-white rounded-xl shadow-md p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-4">All Chapters</h3>
        <div className="space-y-2">
          {chapters.map((ch, idx) => (
            <button
              key={ch.id}
              onClick={() => setCurrentChapter(idx)}
              className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
                idx === currentChapter
                  ? 'bg-blue-50 border-2 border-blue-500 text-blue-700 font-medium'
                  : 'bg-gray-50 border-2 border-transparent text-gray-700 hover:bg-gray-100'
              }`}
            >
              {ch.title}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default LearnPage

