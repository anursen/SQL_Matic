/**
 * Simple logging utility for the frontend
 */

// Define log levels
enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

// Configuration options
interface LoggerConfig {
  level: LogLevel;
  enableConsole: boolean;
  includeTimestamp: boolean;
  storeLogs: boolean;
  maxStoredLogs: number;
}

class Logger {
  private config: LoggerConfig;
  private logs: string[] = [];

  constructor() {
    // Default configuration
    this.config = {
      level: LogLevel.INFO,
      enableConsole: true,
      includeTimestamp: true,
      storeLogs: true,
      maxStoredLogs: 1000,
    };

    // Check if we're in development mode
    if (process.env.NODE_ENV === 'development') {
      this.config.level = LogLevel.DEBUG;
    }
  }

  /**
   * Configure the logger
   */
  configure(options: Partial<LoggerConfig>): void {
    this.config = { ...this.config, ...options };
  }

  /**
   * Format a log message
   */
  private formatMessage(level: string, message: string, ...args: any[]): string {
    let formattedMessage = message;
    
    // Replace %s, %d, %i, %f, %j with corresponding argument
    if (args.length > 0) {
      formattedMessage = message.replace(/%([sdifj])/g, (match, type) => {
        const arg = args.shift();
        
        if (type === 'j') {
          try {
            return JSON.stringify(arg);
          } catch (e) {
            return String(arg);
          }
        }
        
        return String(arg);
      });
    }
    
    const timestamp = this.config.includeTimestamp ? `[${new Date().toISOString()}] ` : '';
    return `${timestamp}[${level}] ${formattedMessage}`;
  }

  /**
   * Store a log message
   */
  private store(message: string): void {
    if (this.config.storeLogs) {
      this.logs.push(message);
      
      // Trim logs if exceeding max stored logs
      if (this.logs.length > this.config.maxStoredLogs) {
        this.logs = this.logs.slice(-this.config.maxStoredLogs);
      }
    }
  }

  /**
   * Get all stored logs
   */
  getLogs(): string[] {
    return [...this.logs];
  }

  /**
   * Clear all stored logs
   */
  clearLogs(): void {
    this.logs = [];
  }

  /**
   * Log a debug message
   */
  debug(message: string, ...args: any[]): void {
    if (this.config.level <= LogLevel.DEBUG) {
      const formattedMessage = this.formatMessage('DEBUG', message, ...args);
      if (this.config.enableConsole) {
        console.debug(formattedMessage);
      }
      this.store(formattedMessage);
    }
  }

  /**
   * Log an info message
   */
  info(message: string, ...args: any[]): void {
    if (this.config.level <= LogLevel.INFO) {
      const formattedMessage = this.formatMessage('INFO', message, ...args);
      if (this.config.enableConsole) {
        console.info(formattedMessage);
      }
      this.store(formattedMessage);
    }
  }

  /**
   * Log a warning message
   */
  warn(message: string, ...args: any[]): void {
    if (this.config.level <= LogLevel.WARN) {
      const formattedMessage = this.formatMessage('WARN', message, ...args);
      if (this.config.enableConsole) {
        console.warn(formattedMessage);
      }
      this.store(formattedMessage);
    }
  }

  /**
   * Log an error message
   */
  error(message: string, ...args: any[]): void {
    if (this.config.level <= LogLevel.ERROR) {
      const formattedMessage = this.formatMessage('ERROR', message, ...args);
      if (this.config.enableConsole) {
        console.error(formattedMessage);
      }
      this.store(formattedMessage);
    }
  }
}

// Create and export a singleton instance
export const logger = new Logger();
