import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { Check } from 'lucide-react';
import { cn } from '@/utils/cn';

// Linear Progress
const progressVariants = cva(
  'relative h-2 w-full overflow-hidden rounded-full bg-neutral-200',
  {
    variants: {
      size: {
        sm: 'h-1',
        md: 'h-2',
        lg: 'h-3',
      },
    },
    defaultVariants: {
      size: 'md',
    },
  }
);

export interface ProgressProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof progressVariants> {
  value: number; // 0-100
  showLabel?: boolean;
  label?: string;
}

export const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value, size, showLabel = false, label, ...props }, ref) => {
    // Clamp value between 0 and 100
    const clampedValue = Math.min(100, Math.max(0, value));

    return (
      <div className="flex w-full flex-col gap-2">
        {/* Label */}
        {(showLabel || label) && (
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium text-neutral-700">
              {label || 'Progress'}
            </span>
            <span className="text-neutral-600">{clampedValue}%</span>
          </div>
        )}

        {/* Progress bar */}
        <div
          ref={ref}
          className={cn(progressVariants({ size }), className)}
          role="progressbar"
          aria-valuenow={clampedValue}
          aria-valuemin={0}
          aria-valuemax={100}
          {...props}
        >
          <div
            className="h-full bg-primary-600 transition-all duration-300 ease-in-out"
            style={{ width: `${clampedValue}%` }}
          />
        </div>
      </div>
    );
  }
);

Progress.displayName = 'Progress';

// Stepped Progress
export interface Step {
  id: string;
  label: string;
  description?: string;
}

export interface SteppedProgressProps {
  steps: Step[];
  currentStep: number; // 0-indexed
  onStepClick?: (stepIndex: number) => void;
  className?: string;
}

export const SteppedProgress: React.FC<SteppedProgressProps> = ({
  steps,
  currentStep,
  onStepClick,
  className,
}) => {
  return (
    <div className={cn('w-full', className)}>
      <nav aria-label="Progress">
        <ol className="flex items-center">
          {steps.map((step, index) => {
            const isCompleted = index < currentStep;
            const isCurrent = index === currentStep;
            const isClickable = onStepClick && (isCompleted || isCurrent);

            return (
              <li
                key={step.id}
                className={cn(
                  'relative flex-1',
                  index !== steps.length - 1 && 'pr-8 sm:pr-20'
                )}
              >
                {/* Connector line */}
                {index !== steps.length - 1 && (
                  <div
                    className="absolute left-4 top-4 -ml-px mt-0.5 h-0.5 w-full"
                    aria-hidden="true"
                  >
                    <div
                      className={cn(
                        'h-full transition-all duration-300',
                        isCompleted ? 'bg-primary-600' : 'bg-neutral-200'
                      )}
                    />
                  </div>
                )}

                {/* Step button/indicator */}
                <button
                  type="button"
                  onClick={
                    isClickable ? () => onStepClick?.(index) : undefined
                  }
                  disabled={!isClickable}
                  className={cn(
                    'group relative flex w-full flex-col',
                    isClickable && 'cursor-pointer hover:opacity-80',
                    !isClickable && 'cursor-default'
                  )}
                  aria-current={isCurrent ? 'step' : undefined}
                >
                  <span className="flex items-start">
                    {/* Step circle */}
                    <span className="relative flex h-9 w-9 flex-shrink-0 items-center justify-center">
                      {isCompleted ? (
                        // Completed step
                        <span className="flex h-9 w-9 items-center justify-center rounded-full bg-primary-600 transition-all duration-300">
                          <Check className="h-5 w-5 text-white" aria-hidden="true" />
                        </span>
                      ) : isCurrent ? (
                        // Current step
                        <>
                          <span
                            className="absolute h-9 w-9 rounded-full bg-primary-200"
                            aria-hidden="true"
                          />
                          <span
                            className="relative flex h-7 w-7 items-center justify-center rounded-full border-2 border-primary-600 bg-white"
                            aria-hidden="true"
                          >
                            <span className="h-3 w-3 rounded-full bg-primary-600" />
                          </span>
                        </>
                      ) : (
                        // Future step
                        <span
                          className="flex h-9 w-9 items-center justify-center rounded-full border-2 border-neutral-300 bg-white transition-all duration-300"
                          aria-hidden="true"
                        >
                          <span className="h-3 w-3 rounded-full bg-transparent" />
                        </span>
                      )}
                    </span>

                    {/* Step label */}
                    <span className="ml-4 mt-0.5 flex min-w-0 flex-col">
                      <span
                        className={cn(
                          'text-sm font-medium transition-all duration-300',
                          isCurrent
                            ? 'text-primary-600'
                            : isCompleted
                            ? 'text-neutral-900'
                            : 'text-neutral-500'
                        )}
                      >
                        {step.label}
                      </span>
                      {step.description && (
                        <span className="text-sm text-neutral-500">
                          {step.description}
                        </span>
                      )}
                    </span>
                  </span>
                </button>
              </li>
            );
          })}
        </ol>
      </nav>
    </div>
  );
};

SteppedProgress.displayName = 'SteppedProgress';

// Circular Progress (optional, for completeness)
export interface CircularProgressProps {
  value: number; // 0-100
  size?: number; // diameter in pixels
  strokeWidth?: number;
  showLabel?: boolean;
  className?: string;
}

export const CircularProgress: React.FC<CircularProgressProps> = ({
  value,
  size = 120,
  strokeWidth = 8,
  showLabel = true,
  className,
}) => {
  const clampedValue = Math.min(100, Math.max(0, value));
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (clampedValue / 100) * circumference;

  return (
    <div className={cn('relative inline-flex items-center justify-center', className)}>
      <svg
        width={size}
        height={size}
        className="transform -rotate-90"
        role="progressbar"
        aria-valuenow={clampedValue}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-neutral-200"
        />
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="text-primary-600 transition-all duration-300 ease-in-out"
        />
      </svg>
      {/* Center label */}
      {showLabel && (
        <span className="absolute text-xl font-semibold text-neutral-900">
          {clampedValue}%
        </span>
      )}
    </div>
  );
};

CircularProgress.displayName = 'CircularProgress';
