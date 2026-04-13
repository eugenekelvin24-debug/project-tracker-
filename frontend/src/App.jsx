import React, { useState } from 'react';

const AnalyzeJob = () => {
  const [description, setDescription] = useState('');
  const [formData, setFormData] = useState({
    company: '',
    title: '',
    location: '',
  });
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!description) return;
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/analyze-job/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: description }),
      });

      const result = await response.json();

      if (result.status === 'success') {
        // This is where the magic happens! 
        // We update the form with what the AI found.
        setFormData({
          company: result.data.company,
          title: result.data.title,
          location: result.data.location,
        });
      }
    } catch (error) {
      console.error("Error connecting to FastAPI:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-2xl mx-auto bg-gray-900 text-white rounded-xl shadow-2xl">
      <h2 className="text-2xl font-bold mb-6 text-blue-400">Smart Job Analyzer</h2>
      
      {/* 1. The Big Paste Area */}
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">Paste Job Description Here</label>
        <textarea
          className="w-full p-4 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none h-40"
          placeholder="e.g. Applied for a junior dev role at Amazon..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="mt-3 w-full bg-blue-600 hover:bg-blue-500 py-3 rounded-lg font-bold transition-all disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Auto-Fill Details"}
        </button>
      </div>

      <hr className="border-gray-700 mb-6" />

      {/* 2. The Auto-Filled Fields */}
      <div className="grid grid-cols-1 gap-4">
        <div>
          <label className="text-xs text-gray-400 uppercase">Company</label>
          <input
            type="text"
            value={formData.company}
            onChange={(e) => setFormData({...formData, company: e.target.value})}
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg"
          />
        </div>
        <div>
          <label className="text-xs text-gray-400 uppercase">Role / Title</label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg"
          />
        </div>
        <div>
          <label className="text-xs text-gray-400 uppercase">Location</label>
          <input
            type="text"
            value={formData.location}
            onChange={(e) => setFormData({...formData, location: e.target.value})}
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg"
          />
        </div>
      </div>
    </div>
  );
};

export default AnalyzeJob;