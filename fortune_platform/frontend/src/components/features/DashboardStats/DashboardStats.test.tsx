import { describe, it, expect } from 'vitest';
import { render, screen } from '@/tests/utils';
import { DashboardStats } from './DashboardStats';

describe('DashboardStats', () => {
  const mockStats = {
    total_profiles: 5,
    total_reports: 12,
    pending_reports: 3,
    completed_reports: 9,
  };

  it('renders all stat cards', () => {
    render(<DashboardStats stats={mockStats} />);

    expect(screen.getByText('命盤總數')).toBeInTheDocument();
    expect(screen.getByText('報告總數')).toBeInTheDocument();
    expect(screen.getByText('處理中')).toBeInTheDocument();
    expect(screen.getByText('已完成')).toBeInTheDocument();
  });

  it('displays correct stat values', () => {
    render(<DashboardStats stats={mockStats} />);

    expect(screen.getByText('5')).toBeInTheDocument(); // total_profiles
    expect(screen.getByText('12')).toBeInTheDocument(); // total_reports
    expect(screen.getByText('3')).toBeInTheDocument(); // pending_reports
    expect(screen.getByText('9')).toBeInTheDocument(); // completed_reports
  });

  it('renders stat icons', () => {
    const { container } = render(<DashboardStats stats={mockStats} />);

    // Check for SVG icons
    const icons = container.querySelectorAll('svg');
    expect(icons.length).toBeGreaterThanOrEqual(4);
  });

  it('shows loading state', () => {
    render(<DashboardStats stats={mockStats} isLoading={true} />);

    const loadingElements = screen.getAllByRole('status');
    expect(loadingElements.length).toBeGreaterThan(0);
  });

  it('shows error state', () => {
    render(<DashboardStats stats={mockStats} error="Failed to load stats" />);

    expect(screen.getByText(/載入失敗|錯誤/i)).toBeInTheDocument();
  });

  it('displays zero values correctly', () => {
    const emptyStats = {
      total_profiles: 0,
      total_reports: 0,
      pending_reports: 0,
      completed_reports: 0,
    };

    render(<DashboardStats stats={emptyStats} />);

    const zeroElements = screen.getAllByText('0');
    expect(zeroElements.length).toBe(4);
  });

  it('shows trend indicators when provided', () => {
    const statsWithTrends = {
      ...mockStats,
      trends: {
        total_profiles: { value: 2, direction: 'up' as const },
        total_reports: { value: 5, direction: 'up' as const },
        pending_reports: { value: 1, direction: 'down' as const },
        completed_reports: { value: 4, direction: 'up' as const },
      },
    };

    const { container } = render(<DashboardStats stats={statsWithTrends} />);

    // Check for trend arrows
    const upArrows = container.querySelectorAll('.text-success-600');
    const downArrows = container.querySelectorAll('.text-error-600');

    expect(upArrows.length + downArrows.length).toBeGreaterThan(0);
  });

  it('displays trend percentages', () => {
    const statsWithTrends = {
      ...mockStats,
      trends: {
        total_profiles: { value: 2, direction: 'up' as const },
      },
    };

    render(<DashboardStats stats={statsWithTrends} />);

    expect(screen.getByText(/\+2/)).toBeInTheDocument();
  });

  it('renders in grid layout', () => {
    const { container } = render(<DashboardStats stats={mockStats} />);

    const grid = container.querySelector('.grid');
    expect(grid).toBeInTheDocument();
    expect(grid).toHaveClass('grid-cols-1');
  });

  it('applies responsive grid classes', () => {
    const { container } = render(<DashboardStats stats={mockStats} />);

    const grid = container.querySelector('.grid');
    expect(grid).toHaveClass('sm:grid-cols-2');
    expect(grid).toHaveClass('lg:grid-cols-4');
  });

  it('shows stat card with primary color for total profiles', () => {
    const { container } = render(<DashboardStats stats={mockStats} />);

    const cards = container.querySelectorAll('.bg-primary-50');
    expect(cards.length).toBeGreaterThan(0);
  });

  it('shows stat card with secondary color for total reports', () => {
    const { container } = render(<DashboardStats stats={mockStats} />);

    const cards = container.querySelectorAll('.bg-secondary-50');
    expect(cards.length).toBeGreaterThan(0);
  });

  it('shows stat card with warning color for pending reports', () => {
    const { container } = render(<DashboardStats stats={mockStats} />);

    const cards = container.querySelectorAll('.bg-warning-50');
    expect(cards.length).toBeGreaterThan(0);
  });

  it('shows stat card with success color for completed reports', () => {
    const { container } = render(<DashboardStats stats={mockStats} />);

    const cards = container.querySelectorAll('.bg-success-50');
    expect(cards.length).toBeGreaterThan(0);
  });

  it('handles large numbers correctly', () => {
    const largeStats = {
      total_profiles: 1234,
      total_reports: 5678,
      pending_reports: 999,
      completed_reports: 4679,
    };

    render(<DashboardStats stats={largeStats} />);

    expect(screen.getByText('1,234')).toBeInTheDocument();
    expect(screen.getByText('5,678')).toBeInTheDocument();
  });

  it('shows hover effects on stat cards', () => {
    const { container } = render(<DashboardStats stats={mockStats} />);

    const cards = container.querySelectorAll('.hover\\:shadow-md');
    expect(cards.length).toBe(4);
  });

  it('renders stat descriptions', () => {
    render(<DashboardStats stats={mockStats} />);

    expect(screen.getByText(/您建立的命盤數量/)).toBeInTheDocument();
    expect(screen.getByText(/生成的報告總數/)).toBeInTheDocument();
  });

  it('shows loading skeleton with correct structure', () => {
    render(<DashboardStats stats={mockStats} isLoading={true} />);

    const skeletons = screen.getAllByRole('status');
    expect(skeletons.length).toBe(4);
  });

  it('displays refresh timestamp when provided', () => {
    const now = new Date();
    render(<DashboardStats stats={mockStats} lastUpdated={now} />);

    expect(screen.getByText(/最後更新/)).toBeInTheDocument();
  });

  it('handles missing trend data gracefully', () => {
    const statsWithPartialTrends = {
      ...mockStats,
      trends: {
        total_profiles: { value: 2, direction: 'up' as const },
        // Other trends missing
      },
    };

    render(<DashboardStats stats={statsWithPartialTrends} />);

    // Should render without errors
    expect(screen.getByText('命盤總數')).toBeInTheDocument();
  });

  it('applies custom className when provided', () => {
    const { container } = render(
      <DashboardStats stats={mockStats} className="custom-stats" />
    );

    expect(container.firstChild).toHaveClass('custom-stats');
  });

  it('renders clickable stat cards when onClick provided', () => {
    const handleClick = vi.fn();
    render(<DashboardStats stats={mockStats} onStatClick={handleClick} />);

    const cards = screen.getAllByRole('button');
    expect(cards.length).toBe(4);
  });
});
