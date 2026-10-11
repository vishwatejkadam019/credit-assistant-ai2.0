import React, { useState, useEffect } from 'react';
import { aiAPI } from '../services/api';

export default function AIAdvisor() {
  const [advice, setAdvice] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    aiAPI.getLatestAdvice()
      .then(res => setAdvice(res.data))
      .catch(() => {});
  }, []);

  const handleGenerateAdvice = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await aiAPI.getAdvice();
      setAdvice(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate AI advice.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white p-8 rounded-lg shadow">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 border-b pb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Google Gemini AI Advisor</h2>
            <p className="text-gray-600 text-sm">Customized 5-step roadmap based on RBI guidelines and Indian credit systems.</p>
          </div>
          <button 
            onClick={handleGenerateAdvice} 
            disabled={loading}
            className="mt-4 md:mt-0 bg-green-600 text-white px-5 py-2 rounded font-semibold hover:bg-green-700 transition disabled:bg-gray-400"
          >
            {loading ? 'Analyzing with Gemini...' : 'Generate AI Advice'}
          </button>
        </div>

        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{error}</div>}

        {advice ? (
          <div>
            <div className="mb-6 flex items-center gap-3">
              <span className="text-gray-700 font-medium">Assessed Category:</span>
              <span className="bg-blue-100 text-blue-900 px-4 py-1 rounded-full font-bold uppercase text-sm">
                {advice.analysis}
              </span>
            </div>

            <h3 className="text-lg font-bold text-gray-800 mb-4">5-Step Action Roadmap to "Excellent"</h3>
            <div className="space-y-4">
              {advice.action_plan.map((step, idx) => (
                <div key={idx} className="p-4 border rounded-lg bg-gray-50 flex items-start gap-4">
                  <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                    {idx + 1}
                  </div>
                  <p className="text-gray-700 mt-1">{step}</p>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">
            Click "Generate AI Advice" to produce your tailored financial health roadmap.
          </div>
        )}
      </div>
    </div>
  );
}