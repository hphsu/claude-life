import { format, parseISO } from 'date-fns';

/**
 * Format date string or Date object to human-readable format
 * @param date - Date string (ISO 8601) or Date object
 * @param formatString - date-fns format string (default: 'PPP' = "Apr 29, 2025")
 * @returns Formatted date string
 */
export const formatDate = (
  date: string | Date,
  formatString: string = 'PPP'
): string => {
  const dateObj = typeof date === 'string' ? parseISO(date) : date;
  return format(dateObj, formatString);
};

/**
 * Format date and time
 * @param date - Date string or Date object
 * @returns Formatted date and time string (e.g., "Apr 29, 2025 at 2:30 PM")
 */
export const formatDateTime = (date: string | Date): string => {
  return formatDate(date, 'PPP p');
};

/**
 * Format time string from 24-hour to 12-hour format
 * @param time - Time string in HH:MM format (e.g., "14:30")
 * @returns Formatted time string (e.g., "2:30 PM")
 */
export const formatTime = (time: string): string => {
  const [hours, minutes] = time.split(':');
  const hour = parseInt(hours, 10);
  const ampm = hour >= 12 ? 'PM' : 'AM';
  const formattedHour = hour % 12 || 12;
  return `${formattedHour}:${minutes} ${ampm}`;
};

/**
 * Format currency amount
 * @param amount - Amount to format
 * @param currency - Currency code (default: 'USD')
 * @returns Formatted currency string
 */
export const formatCurrency = (
  amount: number,
  currency: string = 'USD'
): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
};

/**
 * Format percentage
 * @param value - Value to format (0-1 or 0-100)
 * @param decimals - Number of decimal places (default: 0)
 * @returns Formatted percentage string
 */
export const formatPercentage = (
  value: number,
  decimals: number = 0
): string => {
  const percentage = value > 1 ? value : value * 100;
  return `${percentage.toFixed(decimals)}%`;
};

/**
 * Truncate text with ellipsis
 * @param text - Text to truncate
 * @param maxLength - Maximum length before truncation
 * @returns Truncated text with ellipsis
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
};
