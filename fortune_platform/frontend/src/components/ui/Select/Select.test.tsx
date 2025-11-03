import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/tests/utils';
import userEvent from '@testing-library/user-event';
import { Select } from './Select';

describe('Select', () => {
  const options = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' },
  ];

  it('renders with options', () => {
    render(<Select options={options} />);
    const select = screen.getByRole('combobox');
    expect(select).toBeInTheDocument();
  });

  it('renders with label', () => {
    render(<Select label="Choose option" options={options} />);
    expect(screen.getByLabelText('Choose option')).toBeInTheDocument();
  });

  it('renders with placeholder', () => {
    render(<Select placeholder="Select an option" options={options} />);
    expect(screen.getByText('Select an option')).toBeInTheDocument();
  });

  it('renders all options', () => {
    render(<Select options={options} />);
    expect(screen.getByText('Option 1')).toBeInTheDocument();
    expect(screen.getByText('Option 2')).toBeInTheDocument();
    expect(screen.getByText('Option 3')).toBeInTheDocument();
  });

  it('handles selection', async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(<Select options={options} onChange={handleChange} />);

    const select = screen.getByRole('combobox');
    await user.selectOptions(select, 'option2');

    expect(handleChange).toHaveBeenCalled();
    expect(select).toHaveValue('option2');
  });

  it('renders with default value', () => {
    render(<Select options={options} value="option2" />);
    const select = screen.getByRole('combobox') as HTMLSelectElement;
    expect(select.value).toBe('option2');
  });

  it('can be disabled', () => {
    render(<Select options={options} disabled />);
    const select = screen.getByRole('combobox');
    expect(select).toBeDisabled();
  });

  it('can be required', () => {
    render(<Select options={options} required />);
    const select = screen.getByRole('combobox');
    expect(select).toBeRequired();
  });

  it('renders with error state', () => {
    render(<Select options={options} error="This field is required" />);
    const errorText = screen.getByText('This field is required');
    expect(errorText).toBeInTheDocument();
    expect(errorText).toHaveClass('text-error-600');
  });

  it('renders with helper text', () => {
    render(<Select options={options} helperText="Choose your preferred option" />);
    expect(screen.getByText('Choose your preferred option')).toBeInTheDocument();
  });

  it('applies different sizes', () => {
    const { rerender } = render(<Select options={options} size="sm" />);
    expect(screen.getByRole('combobox')).toHaveClass('px-3 py-1.5 text-sm');

    rerender(<Select options={options} size="md" />);
    expect(screen.getByRole('combobox')).toHaveClass('px-4 py-2 text-base');

    rerender(<Select options={options} size="lg" />);
    expect(screen.getByRole('combobox')).toHaveClass('px-4 py-3 text-lg');
  });

  it('applies full width when specified', () => {
    const { container } = render(<Select options={options} fullWidth />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper).toHaveClass('w-full');
  });

  it('forwards ref correctly', () => {
    const ref = vi.fn();
    render(<Select options={options} ref={ref} />);
    expect(ref).toHaveBeenCalled();
  });

  it('shows required asterisk when required', () => {
    render(<Select label="Choose option" options={options} required />);
    expect(screen.getByText('*')).toBeInTheDocument();
  });

  it('applies error styling to select', () => {
    render(<Select options={options} error="Error message" />);
    const select = screen.getByRole('combobox');
    expect(select).toHaveClass('border-error-600');
  });

  it('renders option groups', () => {
    const groupedOptions = [
      {
        label: 'Group 1',
        options: [
          { value: 'g1o1', label: 'Group 1 Option 1' },
          { value: 'g1o2', label: 'Group 1 Option 2' },
        ],
      },
      {
        label: 'Group 2',
        options: [
          { value: 'g2o1', label: 'Group 2 Option 1' },
        ],
      },
    ];

    render(<Select options={groupedOptions} />);
    expect(screen.getByText('Group 1')).toBeInTheDocument();
    expect(screen.getByText('Group 2')).toBeInTheDocument();
    expect(screen.getByText('Group 1 Option 1')).toBeInTheDocument();
  });
});
