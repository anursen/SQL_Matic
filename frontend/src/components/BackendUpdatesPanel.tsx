import React, { useState, useEffect } from 'react';
import { useChatStore } from '../store';

const MetricCard: React.FC<{ title: string; value: string | number }> = ({ title, value }) => (
  <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100">
    <h3 className="text-sm font-medium text-gray-500 mb-1">{title}</h3>
    <p className="text-xl font-semibold text-gray-800">{value}</p>
  </div>
);

interface TableSchema {
  name: string;
  columns: {
    name: string;
    type: string;
    notnull: boolean;
    pk: boolean;
  }[];
}

const BackendUpdatesPanel: React.FC = () => {
  const backendStatus = useChatStore((state) => state.backendStatus);
  const [dbSchema, setDbSchema] = useState<{ tables: TableSchema[] } | null>(null);
  const [isSchemaExpanded, setIsSchemaExpanded] = useState<Record<string, boolean>>({});
  
  useEffect(() => {
    // Fetch schema when component mounts
    const fetchSchema = async () => {
      try {
        console.log("Fetching schema...");
        const response = await fetch('http://localhost:8000/schema');
        console.log("Schema response status:", response.status);
        if (response.ok) {
          const data = await response.json();
          console.log("Schema data received:", data);
          setDbSchema(data);
        }
      } catch (error) {
        console.error("Error fetching schema:", error);
      }
    };
    
    fetchSchema();
  }, []);
  
  const toggleTableExpand = (tableName: string) => {
    setIsSchemaExpanded(prev => ({
      ...prev,
      [tableName]: !prev[tableName]
    }));
  };

  return (
    <div className="h-full bg-gray-50 p-6 overflow-y-auto" style={{ maxHeight: '100vh' }}>
      <h2 className="text-xl font-semibold text-gray-800 mb-6">System Metrics(V2)</h2>
      <div className="space-y-4 mb-6">
        <MetricCard 
          title="Chat Token Usage" 
          value={`${backendStatus.tokenUsage} tokens`}
        />
        <MetricCard 
          title="Current Inference Speed" 
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
      
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Database Structure</h2>
      {dbSchema ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100">
          {dbSchema.tables.map(table => (
            <div key={table.name} className="border-b border-gray-100 last:border-0">
              <div 
                className="p-3 cursor-pointer hover:bg-gray-50 flex justify-between items-center"
                onClick={() => toggleTableExpand(table.name)}
              >
                <span className="font-medium text-gray-700">{table.name}</span>
                <span className="text-gray-400">
                  {isSchemaExpanded[table.name] ? '−' : '+'}
                </span>
              </div>
              
              {isSchemaExpanded[table.name] && (
                <div className="px-3 pb-3">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-left text-gray-500">
                        <th className="p-2">Column</th>
                        <th className="p-2">Type</th>
                        <th className="p-2">Constraints</th>
                      </tr>
                    </thead>
                    <tbody>
                      {table.columns.map(column => (
                        <tr key={column.name} className="border-t border-gray-100">
                          <td className="p-2">{column.name}</td>
                          <td className="p-2 text-gray-600">{column.type}</td>
                          <td className="p-2 space-x-1">
                            {column.pk && (
                              <span className="px-2 py-0.5 bg-amber-100 text-amber-800 rounded-md text-xs">
                                PK
                              </span>
                            )}
                            {column.notnull && (
                              <span className="px-2 py-0.5 bg-red-100 text-red-800 rounded-md text-xs">
                                NOT NULL
                              </span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="text-gray-500 text-center py-8">
          Loading database schema...
        </div>
      )}
    </div>
  );
};

export default BackendUpdatesPanel;
