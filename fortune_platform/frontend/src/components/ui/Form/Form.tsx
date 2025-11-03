import React from 'react';
import {
  useForm,
  FormProvider,
  useFormContext,
  FieldValues,
  UseFormReturn,
  FieldPath,
  UseFormProps,
} from 'react-hook-form';
import { cn } from '@/utils/cn';

// Form component - wraps react-hook-form FormProvider
export interface FormProps<TFieldValues extends FieldValues = FieldValues>
  extends Omit<React.FormHTMLAttributes<HTMLFormElement>, 'onSubmit'> {
  form: UseFormReturn<TFieldValues>;
  onSubmit: (data: TFieldValues) => void | Promise<void>;
}

export function Form<TFieldValues extends FieldValues = FieldValues>({
  form,
  onSubmit,
  children,
  className,
  ...props
}: FormProps<TFieldValues>) {
  return (
    <FormProvider {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className={cn('space-y-6', className)}
        {...props}
      >
        {children}
      </form>
    </FormProvider>
  );
}

Form.displayName = 'Form';

// FormField component - wraps individual form fields
export interface FormFieldProps<TFieldValues extends FieldValues = FieldValues> {
  name: FieldPath<TFieldValues>;
  label?: string;
  hint?: string;
  required?: boolean;
  children: (field: {
    value: any;
    onChange: (value: any) => void;
    onBlur: () => void;
    error?: string;
  }) => React.ReactNode;
}

export function FormField<TFieldValues extends FieldValues = FieldValues>({
  name,
  label,
  hint,
  required,
  children,
}: FormFieldProps<TFieldValues>) {
  const {
    register,
    formState: { errors },
    setValue,
    watch,
    trigger,
  } = useFormContext<TFieldValues>();

  const value = watch(name);
  const error = errors[name]?.message as string | undefined;

  const field = {
    value,
    onChange: (newValue: any) => {
      setValue(name, newValue);
      trigger(name);
    },
    onBlur: () => {
      trigger(name);
    },
    error,
  };

  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-sm font-medium text-neutral-700">
          {label}
          {required && (
            <span className="ml-1 text-error-DEFAULT" aria-label="required">
              *
            </span>
          )}
        </label>
      )}
      {children(field)}
      {error && (
        <p className="text-sm text-error-DEFAULT" role="alert">
          {error}
        </p>
      )}
      {!error && hint && (
        <p className="text-sm text-neutral-600">{hint}</p>
      )}
    </div>
  );
}

FormField.displayName = 'FormField';

// FormLabel component
export interface FormLabelProps
  extends React.LabelHTMLAttributes<HTMLLabelElement> {
  required?: boolean;
}

export const FormLabel: React.FC<FormLabelProps> = ({
  children,
  required,
  className,
  ...props
}) => (
  <label
    className={cn('text-sm font-medium text-neutral-700', className)}
    {...props}
  >
    {children}
    {required && (
      <span className="ml-1 text-error-DEFAULT" aria-label="required">
        *
      </span>
    )}
  </label>
);

FormLabel.displayName = 'FormLabel';

// FormDescription component
export const FormDescription: React.FC<
  React.HTMLAttributes<HTMLParagraphElement>
> = ({ className, ...props }) => (
  <p className={cn('text-sm text-neutral-600', className)} {...props} />
);

FormDescription.displayName = 'FormDescription';

// FormMessage component - for error messages
export const FormMessage: React.FC<
  React.HTMLAttributes<HTMLParagraphElement>
> = ({ className, ...props }) => (
  <p
    className={cn('text-sm text-error-DEFAULT', className)}
    role="alert"
    {...props}
  />
);

FormMessage.displayName = 'FormMessage';

// FormSection component - for grouping related fields
export interface FormSectionProps
  extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  description?: string;
}

export const FormSection: React.FC<FormSectionProps> = ({
  title,
  description,
  children,
  className,
  ...props
}) => (
  <div className={cn('space-y-4', className)} {...props}>
    {(title || description) && (
      <div className="space-y-1">
        {title && (
          <h3 className="text-lg font-semibold text-neutral-900">{title}</h3>
        )}
        {description && (
          <p className="text-sm text-neutral-600">{description}</p>
        )}
      </div>
    )}
    {children}
  </div>
);

FormSection.displayName = 'FormSection';

// FormActions component - for submit/cancel buttons
export const FormActions: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className,
  ...props
}) => (
  <div
    className={cn(
      'flex items-center justify-end gap-3 border-t border-neutral-200 pt-6',
      className
    )}
    {...props}
  />
);

FormActions.displayName = 'FormActions';

// Hook for creating forms with validation
export function useFormWithValidation<TFieldValues extends FieldValues>(
  options?: UseFormProps<TFieldValues>
) {
  return useForm<TFieldValues>({
    mode: 'onBlur', // Validate on blur by default
    ...options,
  });
}
