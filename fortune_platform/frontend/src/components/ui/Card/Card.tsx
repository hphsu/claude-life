import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/utils/cn';

const cardVariants = cva('rounded-lg transition-all duration-200', {
  variants: {
    variant: {
      default: 'bg-white border border-neutral-200',
      elevated: 'bg-white shadow-lg hover:shadow-xl',
      bordered: 'bg-white border-2 border-primary-200',
      interactive:
        'bg-white border border-neutral-200 cursor-pointer hover:border-primary-400 hover:shadow-md',
    },
    padding: {
      compact: 'p-4',
      default: 'p-6',
      spacious: 'p-8',
    },
  },
  defaultVariants: {
    variant: 'default',
    padding: 'default',
  },
});

export interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {
  header?: React.ReactNode;
  footer?: React.ReactNode;
  hoverable?: boolean;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  (
    {
      className,
      variant,
      padding,
      header,
      footer,
      hoverable = false,
      children,
      onClick,
      ...props
    },
    ref
  ) => {
    const isInteractive = variant === 'interactive' || onClick || hoverable;

    return (
      <div
        ref={ref}
        className={cn(
          cardVariants({ variant, padding }),
          isInteractive && 'transition-transform hover:scale-[1.02]',
          className
        )}
        onClick={onClick}
        role={isInteractive ? 'button' : undefined}
        tabIndex={isInteractive ? 0 : undefined}
        onKeyDown={
          isInteractive
            ? (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  onClick?.(e as any);
                }
              }
            : undefined
        }
        {...props}
      >
        {header && (
          <div className="mb-4 border-b border-neutral-200 pb-4">{header}</div>
        )}
        <div>{children}</div>
        {footer && (
          <div className="mt-4 border-t border-neutral-200 pt-4">{footer}</div>
        )}
      </div>
    );
  }
);

Card.displayName = 'Card';

// Sub-components for better composition
export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className,
  ...props
}) => <div className={cn('flex flex-col space-y-1.5', className)} {...props} />;

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({
  className,
  ...props
}) => (
  <h3
    className={cn(
      'text-2xl font-semibold leading-none tracking-tight',
      className
    )}
    {...props}
  />
);

export const CardDescription: React.FC<
  React.HTMLAttributes<HTMLParagraphElement>
> = ({ className, ...props }) => (
  <p className={cn('text-sm text-neutral-600', className)} {...props} />
);

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className,
  ...props
}) => <div className={cn('pt-0', className)} {...props} />;

export const CardFooter: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className,
  ...props
}) => <div className={cn('flex items-center', className)} {...props} />;
