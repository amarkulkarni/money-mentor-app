import React from 'react'

interface CertifyPageProps {
  onBack: () => void
}

const CertifyPage: React.FC<CertifyPageProps> = ({ onBack }) => {
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

      {/* Under Construction Message */}
      <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
        <div className="text-8xl mb-6">🚧</div>
        <h2 className="text-4xl font-bold text-gray-800 mb-4">
          Certification Module Coming Soon
        </h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          We're building an amazing certification program to help you validate your financial literacy skills. Stay tuned!
        </p>

        {/* Feature Preview */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6">
            <div className="text-3xl mb-3">📝</div>
            <h3 className="text-lg font-bold text-gray-800 mb-2">Practice Tests</h3>
            <p className="text-sm text-gray-600">
              Test your knowledge with comprehensive practice exams
            </p>
          </div>

          <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-xl p-6">
            <div className="text-3xl mb-3">🏆</div>
            <h3 className="text-lg font-bold text-gray-800 mb-2">Earn Certificates</h3>
            <p className="text-sm text-gray-600">
              Get verified certificates to showcase your skills
            </p>
          </div>

          <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6">
            <div className="text-3xl mb-3">📊</div>
            <h3 className="text-lg font-bold text-gray-800 mb-2">Track Progress</h3>
            <p className="text-sm text-gray-600">
              Monitor your learning journey with detailed analytics
            </p>
          </div>
        </div>

        {/* Notify Me Button */}
        <button className="mt-12 px-8 py-4 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white font-medium rounded-lg hover:from-emerald-600 hover:to-emerald-700 shadow-lg hover:shadow-xl transition-all">
          Notify Me When Available
        </button>
      </div>
    </div>
  )
}

export default CertifyPage

