import React from 'react';
import { useChatStore } from '../store';

const BackendUpdatesPanel: React.FC = () => {
  const backendStatus = useChatStore((state) => state.backendStatus);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Backend Status</h2>
      <div className="space-y-2">
        <div className="p-2 bg-gray-100 rounded">
          <p>Token Usage: {backendStatus.tokenUsage}</p>
        </div>
        <div className="p-2 bg-gray-100 rounded">
          <p>Inference Speed: {backendStatus.inferenceSpeed}ms</p>
        </div>
        <div className="p-2 bg-gray-100 rounded">
          <p>Active Tools: {backendStatus.activeTools.join(', ')}</p>
        </div>
      </div>
    </div>
  );
};

export default BackendUpdatesPanel;
