import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { Message } from '../store';

/**
 * Exports chat messages as a PDF file
 * @param {Message[]} messages - Array of chat messages
 * @param {string} filename - Name of the PDF file to be saved
 */
export const exportChatAsPDF = async (messages: Message[], filename = 'chat-history.pdf') => {
  // Create a new PDF document
  const pdf = new jsPDF('p', 'mm', 'a4');
  const pageWidth = pdf.internal.pageSize.getWidth();
  const margin = 20;
  const contentWidth = pageWidth - (margin * 2);
  let yPosition = 20;

  // Add title
  pdf.setFontSize(16);
  pdf.text('Chat History', pageWidth / 2, yPosition, { align: 'center' });
  yPosition += 15;

  // Set font for messages
  pdf.setFontSize(11);

  // Add each message to the PDF
  messages.forEach((message) => {
    const sender = message.sender === 'user' ? 'You' : 'AI Assistant';
    const content = message.content;
    const date = new Date(message.timestamp).toLocaleString();
    
    pdf.setFont(undefined, 'bold');
    pdf.text(`${sender}:`, margin, yPosition);
    
    pdf.setFont(undefined, 'normal');
    
    // Handle multi-line text
    const textLines = pdf.splitTextToSize(content, contentWidth - 10);
    pdf.text(textLines, margin + 10, yPosition + 6);
    
    // Add timestamp in smaller font
    pdf.setFontSize(8);
    pdf.text(date, margin + 10, yPosition + 6 + (textLines.length * 5) + 2);
    pdf.setFontSize(11);
    
    yPosition += 10 + (textLines.length * 5) + 10;
    
    // Add a new page if needed
    if (yPosition > pdf.internal.pageSize.getHeight() - 20) {
      pdf.addPage();
      yPosition = 20;
    }
  });

  // Save the PDF
  pdf.save(filename);
};

/**
 * Alternative method to export chat as PDF from DOM element
 * @param {HTMLElement} chatContainer - DOM element containing the chat
 * @param {string} filename - Name of the PDF file to be saved
 */
export const exportChatElementAsPDF = async (chatContainer: HTMLElement, filename = 'chat-history.pdf') => {
  try {
    // Save original styling to restore later
    const originalHeight = chatContainer.style.height;
    const originalOverflow = chatContainer.style.overflow;
    const originalMaxHeight = chatContainer.style.maxHeight;
    
    // Temporarily modify the container to ensure all content is visible for capture
    chatContainer.style.height = 'auto';
    chatContainer.style.overflow = 'visible';
    chatContainer.style.maxHeight = 'none';
    
    // Create canvas from the chat container
    const canvas = await html2canvas(chatContainer, {
      scrollY: -window.scrollY,
      windowWidth: document.documentElement.offsetWidth,
      windowHeight: document.documentElement.offsetHeight,
      scale: 2, // Higher resolution
      useCORS: true, // Enable CORS for images
      allowTaint: true,
      logging: false
    });
    
    const imgData = canvas.toDataURL('image/png');
    
    // Calculate dimensions
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    
    // Calculate image width and height maintaining aspect ratio
    const imgWidth = pageWidth - 20; // 10mm margin on each side
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    
    let position = 10;
    
    // Add image to first page
    pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
    
    // Add new pages if needed
    let heightLeft = imgHeight;
    
    while (heightLeft > pageHeight - 20) {
      position = position - pageHeight + 20; // Move position up to continue on next page
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
      heightLeft -= (pageHeight - 20);
    }
    
    // Restore original styling
    chatContainer.style.height = originalHeight;
    chatContainer.style.overflow = originalOverflow;
    chatContainer.style.maxHeight = originalMaxHeight;
    
    // Save the PDF
    pdf.save(filename);
  } catch (error) {
    console.error('Error exporting chat as PDF:', error);
    
    // Fallback to text-based PDF if HTML canvas method fails
    const messages = Array.from(chatContainer.querySelectorAll('.message-content')).map(el => ({
      content: el.textContent || '',
      sender: el.classList.contains('message-user') ? 'user' : 'ai',
      timestamp: Date.now()
    }));
    
    exportChatAsPDF(messages as Message[], filename);
  }
};
