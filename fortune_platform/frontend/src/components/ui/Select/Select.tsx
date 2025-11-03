import React, { forwardRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { ChevronDown } from 'lucide-react';
import { cn } from '@/utils/cn';

const selectVariants = cva(
  // Base styles
  'flex w-full appearance-none rounded-md border bg-white px-3 py-2 pr-10 text-sm transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'border-neutral-300 focus-visible:border-primary-500',
        error: 'border-error-DEFAULT focus-visible:border-error-dark focus-visible:ring-error-DEFAULT',
        success: 'border-success-DEFAULT focus-visible:border-success-dark focus-visible:ring-success-DEFAULT',
      },
      selectSize: {
        sm: 'h-9 text-xs',
        md: 'h-11 text-sm',
        lg: 'h-14 text-base',
      },
    },
    defaultVariants: {
      variant: 'default',
      selectSize: 'md',
    },
  }
);

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectProps
  extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'size'>,
    VariantProps<typeof selectVariants> {
  label?: string;
  error?: string;
  hint?: string;
  options: SelectOption[];
  placeholder?: string;
  required?: boolean;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  (
    {
      className,
      variant,
      selectSize,
      label,
      error,
      hint,
      options,
      placeholder,
      required,
      id,
      disabled,
      ...props
    },
    ref
  ) => {
    // Generate unique ID for label association if not provided
    const selectId = id || `select-${Math.random().toString(36).substr(2, 9)}`;

    // Use error variant if error prop is present
    const effectiveVariant = error ? 'error' : variant;

    return (
      <div className="flex flex-col gap-1.5">
        {/* Label */}
        {label && (
          <label
            htmlFor={selectId}
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

        {/* Select wrapper for chevron icon */}
        <div className="relative">
          {/* Select field */}
          <select
            ref={ref}
            id={selectId}
            className={cn(
              selectVariants({ variant: effectiveVariant, selectSize }),
              className
            )}
            disabled={disabled}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={
              error
                ? `${selectId}-error`
                : hint
                ? `${selectId}-hint`
                : undefined
            }
            aria-required={required}
            {...props}
          >
            {/* Placeholder option */}
            {placeholder && (
              <option value="" disabled>
                {placeholder}
              </option>
            )}

            {/* Options */}
            {options.map((option) => (
              <option
                key={option.value}
                value={option.value}
                disabled={option.disabled}
              >
                {option.label}
              </option>
            ))}
          </select>

          {/* Chevron icon */}
          <div
            className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500"
            aria-hidden="true"
          >
            <ChevronDown className="h-4 w-4" />
          </div>
        </div>

        {/* Error message */}
        {error && (
          <p
            id={`${selectId}-error`}
            className="text-sm text-error-DEFAULT"
            role="alert"
          >
            {error}
          </p>
        )}

        {/* Hint text (only shown if no error) */}
        {!error && hint && (
          <p
            id={`${selectId}-hint`}
            className="text-sm text-neutral-600"
          >
            {hint}
          </p>
        )}
      </div>
    );
  }
);

Select.displayName = 'Select';
