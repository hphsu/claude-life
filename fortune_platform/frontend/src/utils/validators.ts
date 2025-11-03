/**
 * Form validation utility functions
 * Compatible with react-hook-form and other form libraries
 */

export const validators = {
  /**
   * Validate required field
   */
  required: (value: string) => {
    return value.trim() !== '' || 'This field is required';
  },

  /**
   * Validate email format
   */
  email: (value: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value) || 'Invalid email address';
  },

  /**
   * Validate minimum length
   */
  minLength: (min: number) => (value: string) => {
    return value.length >= min || `Minimum ${min} characters required`;
  },

  /**
   * Validate maximum length
   */
  maxLength: (max: number) => (value: string) => {
    return value.length <= max || `Maximum ${max} characters allowed`;
  },

  /**
   * Validate birth date (not in future, not too far in past)
   */
  birthDate: (value: string) => {
    const date = new Date(value);
    const today = new Date();
    const maxDate = new Date(today.getFullYear() - 150, 0, 1);

    if (isNaN(date.getTime())) {
      return 'Invalid date format';
    }
    if (date > today) {
      return 'Birth date cannot be in the future';
    }
    if (date < maxDate) {
      return 'Invalid birth date';
    }
    return true;
  },

  /**
   * Validate time format (HH:MM)
   */
  time: (value: string) => {
    const timeRegex = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/;
    return timeRegex.test(value) || 'Invalid time format (HH:MM)';
  },

  /**
   * Validate phone number (basic international format)
   */
  phone: (value: string) => {
    const phoneRegex = /^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$/;
    return phoneRegex.test(value) || 'Invalid phone number';
  },

  /**
   * Validate password strength
   */
  password: (value: string) => {
    if (value.length < 8) {
      return 'Password must be at least 8 characters';
    }
    if (!/[A-Z]/.test(value)) {
      return 'Password must contain at least one uppercase letter';
    }
    if (!/[a-z]/.test(value)) {
      return 'Password must contain at least one lowercase letter';
    }
    if (!/[0-9]/.test(value)) {
      return 'Password must contain at least one number';
    }
    return true;
  },

  /**
   * Validate URL format
   */
  url: (value: string) => {
    try {
      new URL(value);
      return true;
    } catch {
      return 'Invalid URL format';
    }
  },

  /**
   * Validate numeric value
   */
  numeric: (value: string) => {
    return !isNaN(Number(value)) || 'Must be a valid number';
  },

  /**
   * Validate integer value
   */
  integer: (value: string) => {
    return Number.isInteger(Number(value)) || 'Must be a whole number';
  },

  /**
   * Validate range
   */
  range: (min: number, max: number) => (value: string) => {
    const num = Number(value);
    if (isNaN(num)) {
      return 'Must be a valid number';
    }
    if (num < min || num > max) {
      return `Value must be between ${min} and ${max}`;
    }
    return true;
  },
};
