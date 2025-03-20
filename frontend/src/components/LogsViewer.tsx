import React, { useState, useEffect } from 'react';
import { logger } from '../utils/logger';

interface LogsViewerProps {
  refreshInterval?: number; // in milliseconds
  maxHeight?: string;
}

const LogsViewer: React.FC<LogsViewerProps> = ({ 
  refreshInterval = 2000, 
  maxHeight = '500px' 
}) => {
  const [logs, setLogs] = useState<string[]>([]);
  const [filter, setFilter] = useState<string>('');
  const [autoScroll, setAutoScroll] = useState(true);
  const logContainerRef = React.useRef<HTMLDivElement>(null);

  // Log level color mapping
  const getLogColor = (logEntry: string): string => {
    if (logEntry.includes('[ERROR]')) return 'text-red-600';
    if (logEntry.includes('[WARN]')) return 'text-yellow-600';
    if (logEntry.includes('[INFO]')) return 'text-blue-600';
    if (logEntry.includes('[DEBUG]')) return 'text-gray-600';
    return 'text-gray-800';
  };

  // Refresh logs periodically
  useEffect(() => {
    const fetchLogs = () => {
      setLogs(logger.getLogs());
      
      // Auto-scroll to bottom if enabled
      if (autoScroll && logContainerRef.current) {
        logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
      }
    };

    // Initial fetch
    fetchLogs();

    // Set up interval for refreshing
    const intervalId = setInterval(fetchLogs, refreshInterval);

    // Clean up interval on unmount
    return () => clearInterval(intervalId);
  }, [refreshInterval, autoScroll]);

  // Filter logs based on user input
  const filteredLogs = logs.filter(log => 
    filter === '' || log.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-800">Application Logs</h2>
        <div className="flex space-x-3">
          <button 
            onClick={() => logger.clearLogs()}
            className="px-3 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600"
          >
            Clear Logs
          </button>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="autoScroll"
              checked={autoScroll}
              onChange={(e) => setAutoScroll(e.target.checked)}
              className="mr-2"
            />
            <label htmlFor="autoScroll" className="text-sm text-gray-700">Auto-scroll</label>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter logs..."
          className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div 
        ref={logContainerRef}
        className="font-mono text-sm overflow-auto bg-gray-50 p-3 rounded border border-gray-200"
        style={{ maxHeight }}
      >
        {filteredLogs.length > 0 ? (
          <div className="space-y-1">
            {filteredLogs.map((log, index) => (
              <div key={index} className={`${getLogColor(log)} whitespace-pre-wrap break-words`}>
                {log}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-gray-500 text-center py-8">
            {filter ? 'No logs match your filter' : 'No logs available'}
          </div>
        )}
      </div>
    </div>
  );
};

export default LogsViewer;
