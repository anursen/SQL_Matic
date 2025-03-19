// Simple UUID generator function (if import from 'uuid' fails)
const generateUUID = (): string => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
};

// Use either the imported uuidv4 or our simple generator
const createUUID = (): string => {
  try {
    // Try to use the imported uuid if available
    const { v4: uuidv4 } = require('uuid');
    return uuidv4();
  } catch (e) {
    // Fall back to our simple generator
    return generateUUID();
  }
};

const SESSION_ID_KEY = 'chat_session_id';
const SESSION_HISTORY_KEY = 'chat_session_history';

// Get current session ID from localStorage
export const getSessionId = (): string | null => {
  return localStorage.getItem(SESSION_ID_KEY);
};

// Create a new session ID and store it
export const createNewSession = (): string => {
  const newSessionId = createUUID();
  localStorage.setItem(SESSION_ID_KEY, newSessionId);
  
  // Add to session history
  saveSessionToHistory(newSessionId, `Session ${new Date().toLocaleString()}`);
  
  return newSessionId;
};

// Save session to history with label
export const saveSessionToHistory = (sessionId: string, label: string): void => {
  const history = getSessionHistory();
  
  // Add new session to history (or update existing one)
  history[sessionId] = {
    label,
    lastUsed: new Date().toISOString()
  };
  
  localStorage.setItem(SESSION_HISTORY_KEY, JSON.stringify(history));
};

// Get all saved sessions
export const getSessionHistory = (): Record<string, { label: string, lastUsed: string }> => {
  const history = localStorage.getItem(SESSION_HISTORY_KEY);
  return history ? JSON.parse(history) : {};
};

// Switch to an existing session
export const switchToSession = (sessionId: string): void => {
  const history = getSessionHistory();
  
  // Check if the session exists
  if (history[sessionId]) {
    localStorage.setItem(SESSION_ID_KEY, sessionId);
    
    // Update the last used timestamp
    history[sessionId].lastUsed = new Date().toISOString();
    localStorage.setItem(SESSION_HISTORY_KEY, JSON.stringify(history));
  }
};

// Update session label
export const renameSession = (sessionId: string, newLabel: string): void => {
  const history = getSessionHistory();
  
  if (history[sessionId]) {
    history[sessionId].label = newLabel;
    localStorage.setItem(SESSION_HISTORY_KEY, JSON.stringify(history));
  }
};
