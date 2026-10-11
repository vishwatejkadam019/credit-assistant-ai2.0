import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { financialAPI } from '../services/api';

export default function FinancialForm() {
  const [formData, setFormData] = useState({
    credit_score: 700,
    monthly_income: 50000,
    monthly_expenses: 20000,
    total_debt: 100000,
    credit_limit: 250000,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    financialAPI.getFinancialData()
      .then(res => {
        if (res.data) {
          setFormData({
            credit_score: res.data.credit_score,
            monthly_income: res.data.monthly_income,
            monthly_expenses: res.data.monthly_expenses,
            total_debt: res.data.total_debt,
            credit_limit: res.data.credit_limit,
          });
        }
      })
      .catch(() => {});
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) || 0 });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await financialAPI.saveFinancialData(formData);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update financial metrics.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="bg-white p-8 rounded-lg shadow">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Update Financial Data</h2>
        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{error}</div>}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">CIBIL / Credit Score (300 - 900)</label>
            <input 
              type="number" 
              name="credit_score" 
              min="300" 
              max="900" 
              required 
              className="mt-1 w-full border rounded p-2"
              value={formData.credit_score} 
              onChange={handleChange} 
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Monthly Net Income (₹)</label>
            <input 
              type="number" 
              name="monthly_income" 
              min="1" 
              required 
              className="mt-1 w-full border rounded p-2"
              value={formData.monthly_income} 
              onChange={handleChange} 
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Monthly Expenses & EMI Payments (₹)</label>
            <input 
              type="number" 
              name="monthly_expenses" 
              min="0" 
              required 
              className="mt-1 w-full border rounded p-2"
              value={formData.monthly_expenses} 
              onChange={handleChange} 
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Total Outstanding Debt / Credit Card Balances (₹)</label>
            <input 
              type="number" 
              name="total_debt" 
              min="0" 
              required 
              className="mt-1 w-full border rounded p-2"
              value={formData.total_debt} 
              onChange={handleChange} 
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Total Approved Credit Limit (₹)</label>
            <input 
              type="number" 
              name="credit_limit" 
              min="1" 
              required 
              className="mt-1 w-full border rounded p-2"
              value={formData.credit_limit} 
              onChange={handleChange} 
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition font-semibold"
          >
            {loading ? 'Saving Metrics...' : 'Save & Refresh Dashboard'}
          </button>
        </form>
      </div>
    </div>
  );
}