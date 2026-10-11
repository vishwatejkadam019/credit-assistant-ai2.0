import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function Navbar({ setIsAuthenticated }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    navigate('/login');
  };

  return (
    <nav className="bg-blue-900 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/dashboard" className="text-xl font-bold flex items-center gap-2">
          <span>💳</span> Credit Assistant
        </Link>
        <div className="flex gap-4 items-center">
          <Link to="/dashboard" className="hover:text-blue-200">Dashboard</Link>
          <Link to="/form" className="hover:text-blue-200">Update Data</Link>
          <Link to="/advisor" className="hover:text-blue-200">AI Advisor</Link>
          <button 
            onClick={handleLogout} 
            className="bg-red-600 hover:bg-red-700 text-white px-3 py-1.5 rounded text-sm font-semibold transition"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}