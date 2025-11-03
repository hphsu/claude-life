import React, { forwardRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/utils/cn';

const inputVariants = cva(
  // Base styles
  'flex w-full rounded-md border bg-white px-3 py-2 text-sm transition-all file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-neutral-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'border-neutral-300 focus-visible:border-primary-500',
        error: 'border-error-DEFAULT focus-visible:border-error-dark focus-visible:ring-error-DEFAULT',
        success: 'border-success-DEFAULT focus-visible:border-success-dark focus-visible:ring-success-DEFAULT',
      },
      inputSize: {
        sm: 'h-9 text-xs',
        md: 'h-11 text-sm',
        lg: 'h-14 text-base',
      },
    },
    defaultVariants: {
      variant: 'default',
      inputSize: 'md',
    },
  }
);

export interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'>,
    VariantProps<typeof inputVariants> {
  label?: string;
  error?: string;
  hint?: string;
  leftAddon?: React.ReactNode;
  rightAddon?: React.ReactNode;
  required?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      variant,
      inputSize,
      type = 'text',
      label,
      error,
      hint,
      leftAddon,
      rightAddon,
      required,
      id,
      disabled,
      ...props
    },
    ref
  ) => {
    // Generate unique ID for label association if not provided
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;

    // Use error variant if error prop is present
    const effectiveVariant = error ? 'error' : variant;

    return (
      <div className="flex flex-col gap-1.5">
        {/* Label */}
        {label && (
          <label
            htmlFor={inputId}
            className="text-sm font-medium text-neutral-700"
          >
            {label}
            {required && (
              <span className="ml-1 text-error-DEFAULT" aria-label="required">
                *
              </span>
            )}
          </label>
        )}

        {/* Input wrapper for addons */}
        <div className="relative flex items-center">
          {/* Left addon */}
          {leftAddon && (
            <div
              className="pointer-events-none absolute left-3 flex items-center text-neutral-500"
              aria-hidden="true"
            >
              {leftAddon}
            </div>
          )}

          {/* Input field */}
          <input
            ref={ref}
            id={inputId}
            type={type}
            className={cn(
              inputVariants({ variant: effectiveVariant, inputSize }),
              leftAddon && 'pl-10',
              rightAddon && 'pr-10',
              className
            )}
            disabled={disabled}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={
              error
                ? `${inputId}-error`
                : hint
                ? `${inputId}-hint`
                : undefined
            }
            aria-required={required}
            {...props}
          />

          {/* Right addon */}
          {rightAddon && (
            <div
              className="pointer-events-none absolute right-3 flex items-center text-neutral-500"
              aria-hidden="true"
            >
              {rightAddon}
            </div>
          )}
        </div>

        {/* Error message */}
        {error && (
          <p
            id={`${inputId}-error`}
            className="text-sm text-error-DEFAULT"
            role="alert"
          >
            {error}
          </p>
        )}

        {/* Hint text (only shown if no error) */}
        {!error && hint && (
          <p
            id={`${inputId}-hint`}
            className="text-sm text-neutral-600"
          >
            {hint}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
