import React, { useState } from 'react';
import { exportChatAsPDF, exportChatElementAsPDF } from '../utils/pdfExport';
import { Message } from '../store';

interface ExportButtonProps {
  messages: Message[];
  chatContainerRef?: React.RefObject<HTMLDivElement>;
  className?: string;
}

const ExportButton: React.FC<ExportButtonProps> = ({ 
  messages, 
  chatContainerRef,
  className = ''
}) => {
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async () => {
    if (isExporting) return;
    
    if (!messages || messages.length === 0) {
      alert('No chat messages to export');
      return;
    }

    setIsExporting(true);
    
    try {
      // If we have a reference to the chat container, use the DOM-based export
      if (chatContainerRef && chatContainerRef.current) {
        await exportChatElementAsPDF(chatContainerRef.current);
      } else {
        // Otherwise use the data-based export
        await exportChatAsPDF(messages);
      }
    } catch (error) {
      console.error('Failed to export chat:', error);
      alert('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <button 
      onClick={handleExport}
      disabled={isExporting}
      className={`px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed ${className}`}
      title="Export chat as PDF"
    >
      {isExporting ? 'Exporting...' : 'Export PDF'}
    </button>
  );
};

export default ExportButton;
