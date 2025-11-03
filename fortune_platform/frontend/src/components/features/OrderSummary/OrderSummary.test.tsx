import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/tests/utils';
import userEvent from '@testing-library/user-event';
import { OrderSummary } from './OrderSummary';

describe('OrderSummary', () => {
  const mockProfile = {
    id: '123',
    name: 'John Doe',
    gender: 'male' as const,
    birth_date: '1990-01-15',
    birth_time: '14:30:00',
    birth_location: 'Taipei, Taiwan',
    timezone: 'Asia/Taipei',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  };

  const mockSystems = ['bazi', 'ziwei', 'astrology'];

  it('renders profile information', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText(/1990-01-15/)).toBeInTheDocument();
    expect(screen.getByText('Taipei, Taiwan')).toBeInTheDocument();
  });

  it('displays selected expert systems', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    expect(screen.getByText('八字命理分析')).toBeInTheDocument();
    expect(screen.getByText('紫微斗數分析')).toBeInTheDocument();
    expect(screen.getByText('心理占星分析')).toBeInTheDocument();
  });

  it('shows individual system prices', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    const prices = screen.getAllByText('NT$299');
    expect(prices.length).toBe(3);
  });

  it('displays total price', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    expect(screen.getByText(/NT\$897/)).toBeInTheDocument();
  });

  it('shows bundle information when bundle is selected', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={799}
        bundleName="三方法綜合分析"
        originalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    expect(screen.getByText('三方法綜合分析')).toBeInTheDocument();
    expect(screen.getByText(/NT\$897/)).toBeInTheDocument(); // Original price
    expect(screen.getByText(/NT\$799/)).toBeInTheDocument(); // Bundle price
  });

  it('calculates and displays savings', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={799}
        bundleName="三方法綜合分析"
        originalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    // Savings: 897 - 799 = 98
    expect(screen.getByText(/省下.*NT\$98/)).toBeInTheDocument();
  });

  it('calls onConfirm when confirm button is clicked', async () => {
    const user = userEvent.setup();
    const handleConfirm = vi.fn();
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={handleConfirm}
        onCancel={vi.fn()}
      />
    );

    const confirmButton = screen.getByRole('button', { name: /確認下單|確認/i });
    await user.click(confirmButton);

    expect(handleConfirm).toHaveBeenCalledTimes(1);
  });

  it('calls onCancel when cancel button is clicked', async () => {
    const user = userEvent.setup();
    const handleCancel = vi.fn();
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={handleCancel}
      />
    );

    const cancelButton = screen.getByRole('button', { name: /取消|返回/i });
    await user.click(cancelButton);

    expect(handleCancel).toHaveBeenCalledTimes(1);
  });

  it('shows loading state during submission', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
        isSubmitting={true}
      />
    );

    const confirmButton = screen.getByRole('button', { name: /確認下單|確認/i });
    expect(confirmButton).toBeDisabled();
    expect(confirmButton.querySelector('.animate-spin')).toBeInTheDocument();
  });

  it('disables buttons during submission', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
        isSubmitting={true}
      />
    );

    const confirmButton = screen.getByRole('button', { name: /確認下單|確認/i });
    const cancelButton = screen.getByRole('button', { name: /取消|返回/i });

    expect(confirmButton).toBeDisabled();
    expect(cancelButton).toBeDisabled();
  });

  it('displays estimated delivery time', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    expect(screen.getByText(/預計.*分鐘/)).toBeInTheDocument();
  });

  it('shows terms and conditions checkbox', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    expect(screen.getByRole('checkbox')).toBeInTheDocument();
    expect(screen.getByText(/同意.*條款/)).toBeInTheDocument();
  });

  it('disables confirm button when terms not accepted', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
        termsAccepted={false}
      />
    );

    const confirmButton = screen.getByRole('button', { name: /確認下單|確認/i });
    expect(confirmButton).toBeDisabled();
  });

  it('renders gender in Chinese', () => {
    render(
      <OrderSummary
        profile={{ ...mockProfile, gender: 'female' }}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    expect(screen.getByText('女性')).toBeInTheDocument();
  });

  it('handles missing birth time gracefully', () => {
    const profileWithoutTime = {
      ...mockProfile,
      birth_time: undefined,
    };

    render(
      <OrderSummary
        profile={profileWithoutTime}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.queryByText(/14:30/)).not.toBeInTheDocument();
  });

  it('displays warning for systems without birth time', () => {
    const profileWithoutTime = {
      ...mockProfile,
      birth_time: undefined,
    };

    render(
      <OrderSummary
        profile={profileWithoutTime}
        selectedSystems={['bazi', 'ziwei']}
        totalPrice={598}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    expect(screen.getByText(/需要出生時間/)).toBeInTheDocument();
  });

  it('shows section headers', () => {
    render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );

    expect(screen.getByText('命盤資料')).toBeInTheDocument();
    expect(screen.getByText('選擇的分析項目')).toBeInTheDocument();
    expect(screen.getByText('費用明細')).toBeInTheDocument();
  });

  it('applies compact mode when specified', () => {
    const { container } = render(
      <OrderSummary
        profile={mockProfile}
        selectedSystems={mockSystems}
        totalPrice={897}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
        compact={true}
      />
    );

    expect(container.querySelector('.p-4')).toBeInTheDocument();
  });
});
