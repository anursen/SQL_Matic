import React, { useState } from 'react';
import { useEvaluationStore } from '../store/evaluationStore';

const EvaluationPage: React.FC = () => {
  const { isLoading, error, results, runEvaluation } = useEvaluationStore();
  const [numQueries, setNumQueries] = useState<string>('10');
  
  const handleRunEvaluation = () => {
    const parsedNum = parseInt(numQueries);
    runEvaluation(isNaN(parsedNum) ? undefined : parsedNum);
  };
  
  return (
    <div className="flex flex-col h-full bg-gray-50 p-6 overflow-y-auto">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">SQL Query Evaluation</h2>
      
      {/* Controls */}
      <div className="flex items-center space-x-4 mb-6">
        <div className="flex items-center">
          <label htmlFor="numQueries" className="mr-2 text-gray-700">Number of queries:</label>
          <input
            id="numQueries"
            type="number"
            value={numQueries}
            onChange={(e) => setNumQueries(e.target.value)}
            className="w-20 px-2 py-1 border border-gray-300 rounded"
            min="1"
          />
        </div>
        <button
          onClick={handleRunEvaluation}
          disabled={isLoading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Running...' : 'Run Evaluation'}
        </button>
      </div>
      
      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {/* Summary metrics */}
      {results && !isLoading && (
        <>
          <div className="grid grid-cols-4 gap-4 mb-6">
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <div className="text-sm text-gray-500">Total Queries</div>
              <div className="text-2xl font-semibold">{results.total_queries}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <div className="text-sm text-gray-500">Success Rate</div>
              <div className="text-2xl font-semibold">{results.success_rate?.toFixed(2)}%</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <div className="text-sm text-gray-500">Avg Similarity</div>
              <div className="text-2xl font-semibold">{results.average_similarity?.toFixed(4)}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <div className="text-sm text-gray-500">Time</div>
              <div className="text-2xl font-semibold">{results.execution_time?.toFixed(2)}s</div>
            </div>
          </div>
          
          {/* Evaluation table */}
          <h3 className="text-xl font-semibold text-gray-700 mb-3">Query Results Comparison</h3>
          <div className="bg-white rounded-lg shadow overflow-x-auto mb-6">
            <table className="w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">#</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User Input</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ground Truth SQL</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Assistant SQL</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Similarity</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {results.similarities && results.similarities.length > 0 ? (
                  results.similarities.map((item) => (
                    <tr key={item.query_id} className={item.similarity >= 0.8 ? "bg-green-50" : "bg-red-50"}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.query_id}</td>
                      <td className="px-6 py-4 text-sm text-gray-900">{item.query}</td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        <div className="max-h-20 overflow-auto">
                          <code className="text-xs block p-2 bg-gray-100 rounded">{item.ground_truth_sql}</code>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        <div className="max-h-20 overflow-auto">
                          <code className="text-xs block p-2 bg-gray-100 rounded">{item.assistant_sql}</code>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <span 
                          className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            item.similarity >= 0.8 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {item.similarity.toFixed(4)}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="px-6 py-4 text-center text-sm text-gray-500">
                      No evaluation data available
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          
          {/* Failed cases section - only show if there are failed cases */}
          {results.failed_cases && results.failed_cases.length > 0 && (
            <>
              <h3 className="text-xl font-semibold text-gray-700 mb-3">Failed Queries</h3>
              <div className="bg-white rounded-lg shadow overflow-x-auto mb-6">
                <table className="w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">#</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Query</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Error</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {results.failed_cases.map((item) => (
                      <tr key={item.query_id} className="bg-red-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.query_id}</td>
                        <td className="px-6 py-4 text-sm text-gray-900">{item.query}</td>
                        <td className="px-6 py-4 text-sm text-red-600">
                          {item.error || "Failed to meet similarity threshold"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </>
      )}
      
      {isLoading && (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      )}
      
      {!isLoading && !results && !error && (
        <div className="flex items-center justify-center h-64 text-gray-500">
          Run an evaluation to see results
        </div>
      )}
    </div>
  );
};

export default EvaluationPage;
