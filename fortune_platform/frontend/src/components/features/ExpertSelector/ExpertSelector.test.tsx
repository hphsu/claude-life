import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/tests/utils';
import userEvent from '@testing-library/user-event';
import { ExpertSelector } from './ExpertSelector';

describe('ExpertSelector', () => {
  const mockOnChange = vi.fn();
  const mockOnBundleSelect = vi.fn();

  it('renders all expert systems', () => {
    render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
      />
    );

    expect(screen.getByText('八字命理分析')).toBeInTheDocument();
    expect(screen.getByText('紫微斗數分析')).toBeInTheDocument();
    expect(screen.getByText('心理占星分析')).toBeInTheDocument();
    expect(screen.getByText('姓名學分析')).toBeInTheDocument();
    expect(screen.getByText('梅花易數分析')).toBeInTheDocument();
    expect(screen.getByText('生命靈數分析')).toBeInTheDocument();
    expect(screen.getByText('奇門遁甲分析')).toBeInTheDocument();
    expect(screen.getByText('六爻占卜')).toBeInTheDocument();
  });

  it('shows individual prices when no bundle selected', () => {
    render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
      />
    );

    // Check for individual prices (NT$299 each)
    const priceElements = screen.getAllByText('NT$299');
    expect(priceElements.length).toBeGreaterThan(0);
  });

  it('calls onChange when system is selected', async () => {
    const user = userEvent.setup();
    render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
      />
    );

    const baziCard = screen.getByText('八字命理分析').closest('div[role="button"]');
    await user.click(baziCard!);

    expect(mockOnChange).toHaveBeenCalledWith(['bazi']);
  });

  it('shows selected state for systems', () => {
    const { container } = render(
      <ExpertSelector
        selectedSystems={['bazi', 'ziwei']}
        onChange={mockOnChange}
      />
    );

    const selectedCards = container.querySelectorAll('.border-primary-600');
    expect(selectedCards.length).toBe(2);
  });

  it('displays bundle options', () => {
    render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
      />
    );

    expect(screen.getByText('三方法綜合分析')).toBeInTheDocument();
    expect(screen.getByText('八方法完整解析')).toBeInTheDocument();
  });

  it('shows bundle pricing and discounts', () => {
    render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
      />
    );

    // Check for bundle prices
    expect(screen.getByText('NT$799')).toBeInTheDocument(); // 3-system bundle
    expect(screen.getByText('NT$1,999')).toBeInTheDocument(); // 8-system bundle

    // Check for savings indicators
    expect(screen.getByText(/省下/)).toBeInTheDocument();
  });

  it('calls onBundleSelect when bundle is clicked', async () => {
    const user = userEvent.setup();
    render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
        onBundleSelect={mockOnBundleSelect}
      />
    );

    const threeSystemBundle = screen.getByText('三方法綜合分析').closest('div[role="button"]');
    await user.click(threeSystemBundle!);

    expect(mockOnBundleSelect).toHaveBeenCalledWith('three_system');
  });

  it('highlights selected bundle', () => {
    const { container } = render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
        selectedBundle="eight_system"
      />
    );

    const bundleCards = container.querySelectorAll('.border-primary-600');
    expect(bundleCards.length).toBeGreaterThan(0);
  });

  it('disables individual selection when bundle is selected', () => {
    render(
      <ExpertSelector
        selectedSystems={['bazi', 'ziwei', 'astrology']}
        onChange={mockOnChange}
        selectedBundle="three_system"
      />
    );

    const systemCards = screen.getAllByRole('button');
    const individualCards = systemCards.filter(card =>
      card.textContent?.includes('八字') ||
      card.textContent?.includes('紫微') ||
      card.textContent?.includes('心理占星')
    );

    individualCards.forEach(card => {
      expect(card).toHaveClass('opacity-50');
    });
  });

  it('shows system descriptions', () => {
    render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
      />
    );

    expect(screen.getByText(/分析命盤格局/)).toBeInTheDocument();
    expect(screen.getByText(/揭示人生藍圖/)).toBeInTheDocument();
  });

  it('displays checkmarks for selected systems', () => {
    const { container } = render(
      <ExpertSelector
        selectedSystems={['bazi', 'ziwei']}
        onChange={mockOnChange}
      />
    );

    // Check for checkmark SVG elements
    const checkmarks = container.querySelectorAll('svg.text-primary-600');
    expect(checkmarks.length).toBeGreaterThan(0);
  });

  it('calculates total price correctly for individual selections', () => {
    render(
      <ExpertSelector
        selectedSystems={['bazi', 'ziwei', 'astrology']}
        onChange={mockOnChange}
      />
    );

    // 3 systems × NT$299 = NT$897
    expect(screen.getByText(/總計.*NT\$897/)).toBeInTheDocument();
  });

  it('shows bundle descriptions', () => {
    render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
      />
    );

    expect(screen.getByText(/八字、紫微、心理占星/)).toBeInTheDocument();
    expect(screen.getByText(/所有八種命理系統/)).toBeInTheDocument();
  });

  it('allows deselecting individual systems', async () => {
    const user = userEvent.setup();
    const { rerender } = render(
      <ExpertSelector
        selectedSystems={['bazi']}
        onChange={mockOnChange}
      />
    );

    const baziCard = screen.getByText('八字命理分析').closest('div[role="button"]');
    await user.click(baziCard!);

    expect(mockOnChange).toHaveBeenCalledWith([]);
  });

  it('shows popular badge on recommended bundle', () => {
    render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
      />
    );

    expect(screen.getByText('最受歡迎')).toBeInTheDocument();
  });

  it('renders in compact mode when specified', () => {
    const { container } = render(
      <ExpertSelector
        selectedSystems={[]}
        onChange={mockOnChange}
        compact={true}
      />
    );

    const cards = container.querySelectorAll('.p-3');
    expect(cards.length).toBeGreaterThan(0);
  });
});
