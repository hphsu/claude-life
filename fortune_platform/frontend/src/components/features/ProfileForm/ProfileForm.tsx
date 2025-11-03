import React from 'react';
import { useForm } from 'react-hook-form';
import { Form, FormField, FormSection, FormActions } from '@/components/ui/Form';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Button } from '@/components/ui/Button';
import { useCreateProfile, useUpdateProfile } from '@/hooks/useProfiles';
import type { Profile, CreateProfileInput, UpdateProfileInput } from '@/types/api';

export interface ProfileFormProps {
  profile?: Profile;
  onSuccess?: (profile: Profile) => void;
  onCancel?: () => void;
}

type ProfileFormData = {
  name: string;
  birth_date: string;
  birth_time: string;
  birth_location: string;
  gender: 'M' | 'F' | 'O';
  timezone: string;
};

export const ProfileForm: React.FC<ProfileFormProps> = ({
  profile,
  onSuccess,
  onCancel,
}) => {
  const isEdit = !!profile;

  const form = useForm<ProfileFormData>({
    defaultValues: {
      name: profile?.name || '',
      birth_date: profile?.birth_date || '',
      birth_time: profile?.birth_time || '',
      birth_location: profile?.birth_location || '',
      gender: profile?.gender || 'O',
      timezone: profile?.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone,
    },
  });

  const createMutation = useCreateProfile();
  const updateMutation = useUpdateProfile();

  const onSubmit = async (data: ProfileFormData) => {
    try {
      if (isEdit) {
        const updateData: UpdateProfileInput = {
          id: profile.id,
          ...data,
        };
        const updated = await updateMutation.mutateAsync(updateData);
        onSuccess?.(updated);
      } else {
        const createData: CreateProfileInput = data;
        const created = await createMutation.mutateAsync(createData);
        onSuccess?.(created);
      }
    } catch (error) {
      console.error('Failed to save profile:', error);
    }
  };

  const isLoading = createMutation.isPending || updateMutation.isPending;

  return (
    <Form form={form} onSubmit={onSubmit}>
      <FormSection
        title="Personal Information"
        description="Basic information about the person"
      >
        <FormField
          name="name"
          label="Full Name"
          required
        >
          {(field) => (
            <Input
              {...form.register('name', {
                required: 'Name is required',
                minLength: { value: 2, message: 'Name must be at least 2 characters' },
              })}
              placeholder="Enter full name"
              error={field.error}
              disabled={isLoading}
            />
          )}
        </FormField>

        <FormField
          name="gender"
          label="Gender"
          required
        >
          {(field) => (
            <Select
              {...form.register('gender', { required: 'Gender is required' })}
              error={field.error}
              disabled={isLoading}
            >
              <option value="">Select gender</option>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
            </Select>
          )}
        </FormField>
      </FormSection>

      <FormSection
        title="Birth Information"
        description="Birth date, time, and location are essential for accurate fortune-telling analysis"
      >
        <FormField
          name="birth_date"
          label="Birth Date"
          hint="Format: YYYY-MM-DD"
          required
        >
          {(field) => (
            <Input
              {...form.register('birth_date', {
                required: 'Birth date is required',
                pattern: {
                  value: /^\d{4}-\d{2}-\d{2}$/,
                  message: 'Invalid date format (use YYYY-MM-DD)',
                },
              })}
              type="date"
              error={field.error}
              disabled={isLoading}
            />
          )}
        </FormField>

        <FormField
          name="birth_time"
          label="Birth Time"
          hint="Format: HH:MM (24-hour)"
          required
        >
          {(field) => (
            <Input
              {...form.register('birth_time', {
                required: 'Birth time is required',
                pattern: {
                  value: /^([01]\d|2[0-3]):([0-5]\d)$/,
                  message: 'Invalid time format (use HH:MM)',
                },
              })}
              type="time"
              error={field.error}
              disabled={isLoading}
            />
          )}
        </FormField>

        <FormField
          name="birth_location"
          label="Birth Location"
          hint="City, Country"
          required
        >
          {(field) => (
            <Input
              {...form.register('birth_location', {
                required: 'Birth location is required',
                minLength: { value: 3, message: 'Location must be at least 3 characters' },
              })}
              placeholder="e.g., Taipei, Taiwan"
              error={field.error}
              disabled={isLoading}
            />
          )}
        </FormField>

        <FormField
          name="timezone"
          label="Timezone"
          hint="For accurate time-based calculations"
          required
        >
          {(field) => (
            <Select
              {...form.register('timezone', { required: 'Timezone is required' })}
              error={field.error}
              disabled={isLoading}
            >
              <option value="Asia/Taipei">Asia/Taipei (GMT+8)</option>
              <option value="Asia/Shanghai">Asia/Shanghai (GMT+8)</option>
              <option value="Asia/Hong_Kong">Asia/Hong Kong (GMT+8)</option>
              <option value="America/New_York">America/New York (GMT-5)</option>
              <option value="America/Los_Angeles">America/Los Angeles (GMT-8)</option>
              <option value="Europe/London">Europe/London (GMT+0)</option>
              <option value="UTC">UTC (GMT+0)</option>
            </Select>
          )}
        </FormField>
      </FormSection>

      <FormActions>
        {onCancel && (
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            disabled={isLoading}
          >
            Cancel
          </Button>
        )}
        <Button type="submit" isLoading={isLoading}>
          {isEdit ? 'Update Profile' : 'Create Profile'}
        </Button>
      </FormActions>
    </Form>
  );
};
