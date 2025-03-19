import React from 'react';
import { useChatStore } from '../store';

const MetricCard: React.FC<{ title: string; value: string | number }> = ({ title, value }) => (
  <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100">
    <h3 className="text-sm font-medium text-gray-500 mb-1">{title}</h3>
    <p className="text-xl font-semibold text-gray-800">{value}</p>
  </div>
);

const BackendUpdatesPanel: React.FC = () => {
  const backendStatus = useChatStore((state) => state.backendStatus);

  return (
    <div className="h-full bg-gray-50 p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-6">System Metrics</h2>
      <div className="space-y-4">
        <MetricCard 
          title="Token Usage" 
          value={`${backendStatus.tokenUsage} tokens`}
        />
        <MetricCard 
          title="Inference Speed" 
          value={`${backendStatus.inferenceSpeed} ms`}
        />
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Active Tools</h3>
          <div className="flex flex-wrap gap-2">
            {backendStatus.activeTools.map((tool, index) => (
              <span 
                key={index}
                className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
              >
                {tool}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BackendUpdatesPanel;
