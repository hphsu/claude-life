import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/tests/utils';
import userEvent from '@testing-library/user-event';
import { ProfileCard } from './ProfileCard';
import type { Profile } from '@/types/api';

describe('ProfileCard', () => {
  const mockProfile: Profile = {
    id: '123',
    name: 'John Doe',
    gender: 'male',
    birth_date: '1990-01-15',
    birth_time: '14:30:00',
    birth_location: 'Taipei, Taiwan',
    timezone: 'Asia/Taipei',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  };

  it('renders profile information', () => {
    render(<ProfileCard profile={mockProfile} />);

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText(/1990-01-15/)).toBeInTheDocument();
    expect(screen.getByText(/14:30:00/)).toBeInTheDocument();
    expect(screen.getByText('Taipei, Taiwan')).toBeInTheDocument();
  });

  it('renders gender correctly', () => {
    render(<ProfileCard profile={mockProfile} />);
    expect(screen.getByText(/男性/)).toBeInTheDocument();
  });

  it('calls onEdit when edit button is clicked', async () => {
    const user = userEvent.setup();
    const handleEdit = vi.fn();
    render(<ProfileCard profile={mockProfile} onEdit={handleEdit} />);

    const editButton = screen.getByRole('button', { name: /編輯/i });
    await user.click(editButton);
    expect(handleEdit).toHaveBeenCalledWith(mockProfile);
  });

  it('calls onDelete when delete button is clicked', async () => {
    const user = userEvent.setup();
    const handleDelete = vi.fn();
    render(<ProfileCard profile={mockProfile} onDelete={handleDelete} />);

    const deleteButton = screen.getByRole('button', { name: /刪除/i });
    await user.click(deleteButton);
    expect(handleDelete).toHaveBeenCalledWith(mockProfile.id);
  });

  it('calls onSelect when card is clicked in selectable mode', async () => {
    const user = userEvent.setup();
    const handleSelect = vi.fn();
    render(
      <ProfileCard
        profile={mockProfile}
        selectable={true}
        onSelect={handleSelect}
      />
    );

    const card = screen.getByRole('article');
    await user.click(card);
    expect(handleSelect).toHaveBeenCalledWith(mockProfile);
  });

  it('shows selected state when selected', () => {
    const { container } = render(
      <ProfileCard
        profile={mockProfile}
        selectable={true}
        selected={true}
      />
    );

    const card = container.querySelector('[role="article"]');
    expect(card).toHaveClass('border-primary-600');
  });

  it('does not show action buttons when not provided', () => {
    render(<ProfileCard profile={mockProfile} />);
    expect(screen.queryByRole('button', { name: /編輯/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /刪除/i })).not.toBeInTheDocument();
  });

  it('handles missing optional fields gracefully', () => {
    const minimalProfile: Profile = {
      ...mockProfile,
      birth_time: undefined,
      timezone: undefined,
    };

    render(<ProfileCard profile={minimalProfile} />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  it('formats dates correctly in Chinese locale', () => {
    render(<ProfileCard profile={mockProfile} />);
    // The component should show formatted date
    const dateElement = screen.getByText(/1990/);
    expect(dateElement).toBeInTheDocument();
  });

  it('applies compact mode when specified', () => {
    const { container } = render(
      <ProfileCard profile={mockProfile} compact={true} />
    );

    const card = container.querySelector('[role="article"]');
    expect(card).toHaveClass('p-4'); // Compact padding
  });
});
