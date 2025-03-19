import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ConfigEditorPage: React.FC = () => {
  const [configContent, setConfigContent] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    setIsLoading(true);
    setError('');
    try {
      const response = await axios.get('http://localhost:8000/config');
      setConfigContent(response.data.content);
    } catch (err) {
      setError('Failed to fetch configuration file.');
      console.error('Error fetching config:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const saveConfig = async () => {
    setIsSaving(true);
    setSaveSuccess(false);
    setError('');
    try {
      await axios.post('http://localhost:8000/config', { content: configContent });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000); // Clear success message after 3 seconds
    } catch (err) {
      setError('Failed to save configuration file.');
      console.error('Error saving config:', err);
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-gray-50 p-6 overflow-y-auto">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Configuration Editor</h2>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <span className="font-bold">Error:</span> {error}
        </div>
      )}
      
      {saveSuccess && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          Configuration saved successfully!
        </div>
      )}
      
      <div className="flex-grow mb-6">
        <textarea
          className="w-full h-[calc(100vh-250px)] font-mono text-sm border border-gray-300 rounded-md p-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={configContent}
          onChange={(e) => setConfigContent(e.target.value)}
        />
      </div>
      
      <div className="flex justify-end">
        <button
          onClick={fetchConfig}
          disabled={isLoading || isSaving}
          className="px-4 py-2 mr-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-300 disabled:opacity-50"
        >
          Reset
        </button>
        <button
          onClick={saveConfig}
          disabled={isLoading || isSaving}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {isSaving ? 'Saving...' : 'Save Configuration'}
        </button>
      </div>
    </div>
  );
};

export default ConfigEditorPage;
