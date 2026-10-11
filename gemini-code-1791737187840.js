import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { financialAPI, aiAPI } from '../services/api';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export default function Dashboard() {
  const [finData, setFinData] = useState(null);
  const [history, setHistory] = useState([]);
  const [utilization, setUtilization] = useState(null);
  const [advice, setAdvice] = useState(null);
  const [loading, setLoading] = useState(true);

  const COLORS = ['#ef4444', '#10b981'];

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [fRes, hRes, uRes] = await Promise.all([
        financialAPI.getFinancialData(),
        financialAPI.getHistory(),
        financialAPI.getUtilization(),
      ]);
      setFinData(fRes.data);
      setHistory(hRes.data.map(item => ({
        date: new Date(item.recorded_at).toLocaleDateString(),
        score: item.credit_score
      })));
      setUtilization(uRes.data);

      try {
        const aRes = await aiAPI.getLatestAdvice();
        setAdvice(aRes.data);
      } catch (err) {
        // AI advice not requested yet
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-600">Loading Dashboard...</div>;

  if (!finData) {
    return (
      <div className="p-8 max-w-4xl mx-auto text-center">
        <h2 className="text-2xl font-bold mb-4">Welcome to Credit Assistant</h2>
        <p className="text-gray-600 mb-6">No financial data found. Enter your financial details to activate your dashboard.</p>
        <Link to="/form" className="bg-blue-600 text-white px-6 py-2 rounded font-semibold hover:bg-blue-700">Enter Financial Data</Link>
      </div>
    );
  }

  const pieData = utilization ? [
    { name: 'Used Credit', value: utilization.used_credit },
    { name: 'Available Limit', value: utilization.available_credit }
  ] : [];

  const getScoreBadge = (score) => {
    if (score < 600) return { label: 'Poor', bg: 'bg-red-100 text-red-800' };
    if (score < 750) return { label: 'Fair', bg: 'bg-yellow-100 text-yellow-800' };
    if (score < 800) return { label: 'Good', bg: 'bg-blue-100 text-blue-800' };
    return { label: 'Excellent', bg: 'bg-green-100 text-green-800' };
  };

  const badge = getScoreBadge(finData.credit_score);
  const latestDelta = history.length > 0 ? (history[history.length - 1]?.score - (history[history.length - 2]?.score || history[0]?.score)) : 0;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Top Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow border-t-4 border-blue-600">
          <div className="text-gray-500 text-sm font-medium">CIBIL Credit Score</div>
          <div className="flex items-baseline justify-between mt-2">
            <span className="text-4xl font-extrabold text-gray-800">{finData.credit_score}</span>
            <span className={`px-3 py-1 rounded-full text-sm font-bold ${badge.bg}`}>{badge.label}</span>
          </div>
          <div className="mt-3 text-xs text-gray-500">
            Recent Delta: <span className={latestDelta >= 0 ? "text-green-600 font-bold" : "text-red-600 font-bold"}>
              {latestDelta >= 0 ? `+${latestDelta}` : latestDelta} pts
            </span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-t-4 border-indigo-600">
          <div className="text-gray-500 text-sm font-medium">Credit Utilization</div>
          <div className="text-3xl font-bold text-gray-800 mt-2">{finData.credit_utilization.toFixed(1)}%</div>
          <p className="text-xs text-gray-500 mt-3">Target: Below 30%</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-t-4 border-purple-600">
          <div className="text-gray-500 text-sm font-medium">Debt-To-Income (DTI)</div>
          <div className="text-3xl font-bold text-gray-800 mt-2">{finData.dti_ratio.toFixed(1)}%</div>
          <p className="text-xs text-gray-500 mt-3">Target: Below 40%</p>
        </div>
      </div>

      {/* Bottlenecks Alert */}
      {(finData.credit_utilization > 30 || finData.dti_ratio > 40) && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded">
          <h4 className="font-bold text-red-800">Financial Bottleneck Alerts Detected</h4>
          <ul className="list-disc pl-5 text-sm text-red-700 mt-1">
            {finData.credit_utilization > 30 && (
              <li>High Utilization ({finData.credit_utilization.toFixed(1)}%): Exceeds recommended 30% threshold.</li>
            )}
            {finData.dti_ratio > 40 && (
              <li>High DTI Ratio ({finData.dti_ratio.toFixed(1)}%): Over 40% of monthly income goes toward debts/expenses.</li>
            )}
          </ul>
        </div>
      )}

      {/* Visualizations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Credit Score History</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history}>
                <XAxis dataKey="date" />
                <YAxis domain={[300, 900]} />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#1d4ed8" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Credit Utilization Breakdown</h3>
          <div className="h-64 flex justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} dataKey="value" label>
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(val) => `₹${val.toLocaleString()}`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* AI Roadmap Quick Action */}
      <div className="bg-white p-6 rounded-lg shadow flex flex-col md:flex-row justify-between items-center">
        <div>
          <h3 className="text-lg font-bold text-gray-800">Tailored AI Recommendations</h3>
          <p className="text-gray-600 text-sm">Get personalized suggestions based on Indian banking norms and CIBIL rules.</p>
        </div>
        <Link to="/advisor" className="mt-4 md:mt-0 bg-blue-600 text-white px-6 py-2 rounded font-semibold hover:bg-blue-700">
          {advice ? 'View Full Advice' : 'Get Gemini AI Advice'}
        </Link>
      </div>
    </div>
  );
}