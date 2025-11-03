import { describe, it, expect } from 'vitest';
import { render, screen } from '@/tests/utils';
import { RecentActivity } from './RecentActivity';

describe('RecentActivity', () => {
  const mockActivities = [
    {
      id: '1',
      type: 'report_created',
      title: '八字命理報告生成',
      description: 'John Doe 的八字命理分析報告已完成',
      timestamp: new Date('2024-01-15T10:30:00Z'),
      status: 'completed' as const,
      profile_name: 'John Doe',
    },
    {
      id: '2',
      type: 'profile_created',
      title: '新增命盤',
      description: '成功建立 Jane Smith 的命盤資料',
      timestamp: new Date('2024-01-15T09:15:00Z'),
      status: 'completed' as const,
      profile_name: 'Jane Smith',
    },
    {
      id: '3',
      type: 'report_pending',
      title: '紫微斗數分析中',
      description: '正在為 John Doe 生成紫微斗數報告',
      timestamp: new Date('2024-01-15T08:00:00Z'),
      status: 'pending' as const,
      profile_name: 'John Doe',
    },
  ];

  it('renders all activity items', () => {
    render(<RecentActivity activities={mockActivities} />);

    expect(screen.getByText('八字命理報告生成')).toBeInTheDocument();
    expect(screen.getByText('新增命盤')).toBeInTheDocument();
    expect(screen.getByText('紫微斗數分析中')).toBeInTheDocument();
  });

  it('displays activity descriptions', () => {
    render(<RecentActivity activities={mockActivities} />);

    expect(screen.getByText(/John Doe 的八字命理分析報告已完成/)).toBeInTheDocument();
    expect(screen.getByText(/成功建立 Jane Smith 的命盤資料/)).toBeInTheDocument();
  });

  it('shows timestamps', () => {
    render(<RecentActivity activities={mockActivities} />);

    // Should show relative time like "2 hours ago"
    const timestamps = screen.getAllByText(/前|ago/);
    expect(timestamps.length).toBeGreaterThan(0);
  });

  it('displays status badges', () => {
    const { container } = render(<RecentActivity activities={mockActivities} />);

    // Check for status badge elements
    const completedBadges = container.querySelectorAll('.bg-success-100');
    const pendingBadges = container.querySelectorAll('.bg-warning-100');

    expect(completedBadges.length).toBeGreaterThan(0);
    expect(pendingBadges.length).toBeGreaterThan(0);
  });

  it('shows different icons for different activity types', () => {
    const { container } = render(<RecentActivity activities={mockActivities} />);

    const icons = container.querySelectorAll('svg');
    expect(icons.length).toBeGreaterThanOrEqual(3);
  });

  it('shows loading state', () => {
    render(<RecentActivity activities={[]} isLoading={true} />);

    const loadingElements = screen.getAllByRole('status');
    expect(loadingElements.length).toBeGreaterThan(0);
  });

  it('shows error state', () => {
    render(<RecentActivity activities={[]} error="Failed to load activities" />);

    expect(screen.getByText(/載入失敗|錯誤/i)).toBeInTheDocument();
  });

  it('shows empty state when no activities', () => {
    render(<RecentActivity activities={[]} />);

    expect(screen.getByText(/暫無活動記錄|沒有活動/i)).toBeInTheDocument();
  });

  it('formats timestamps as relative time', () => {
    render(<RecentActivity activities={mockActivities} />);

    // Should show relative time formats
    const relativeTimePatterns = [/小時前/, /分鐘前/, /天前/, /剛剛/];
    const hasRelativeTime = relativeTimePatterns.some(pattern =>
      screen.queryByText(pattern) !== null
    );

    expect(hasRelativeTime).toBe(true);
  });

  it('shows status text for completed activities', () => {
    render(<RecentActivity activities={mockActivities} />);

    expect(screen.getByText('已完成')).toBeInTheDocument();
  });

  it('shows status text for pending activities', () => {
    render(<RecentActivity activities={mockActivities} />);

    expect(screen.getByText('處理中')).toBeInTheDocument();
  });

  it('renders activities in reverse chronological order', () => {
    render(<RecentActivity activities={mockActivities} />);

    const titles = screen.getAllByRole('heading', { level: 4 });
    expect(titles[0]).toHaveTextContent('八字命理報告生成'); // Most recent
    expect(titles[2]).toHaveTextContent('紫微斗數分析中'); // Oldest
  });

  it('limits displayed activities when maxItems specified', () => {
    render(<RecentActivity activities={mockActivities} maxItems={2} />);

    expect(screen.getByText('八字命理報告生成')).toBeInTheDocument();
    expect(screen.getByText('新增命盤')).toBeInTheDocument();
    expect(screen.queryByText('紫微斗數分析中')).not.toBeInTheDocument();
  });

  it('shows "View All" link when activities exceed maxItems', () => {
    render(<RecentActivity activities={mockActivities} maxItems={2} />);

    expect(screen.getByText(/查看全部|更多/i)).toBeInTheDocument();
  });

  it('handles click on activity item', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();
    render(<RecentActivity activities={mockActivities} onActivityClick={handleClick} />);

    const firstActivity = screen.getByText('八字命理報告生成').closest('div[role="button"]');
    await user.click(firstActivity!);

    expect(handleClick).toHaveBeenCalledWith(mockActivities[0]);
  });

  it('shows profile avatar when available', () => {
    const activitiesWithAvatars = mockActivities.map(activity => ({
      ...activity,
      profile_avatar: '/avatar.jpg',
    }));

    const { container } = render(<RecentActivity activities={activitiesWithAvatars} />);

    const avatars = container.querySelectorAll('img[alt*="avatar"]');
    expect(avatars.length).toBe(3);
  });

  it('shows initials when no avatar available', () => {
    render(<RecentActivity activities={mockActivities} />);

    // Should show first letter of profile name
    expect(screen.getByText('J')).toBeInTheDocument(); // John
  });

  it('handles different activity types with appropriate icons', () => {
    const differentTypes = [
      { ...mockActivities[0], type: 'report_created' },
      { ...mockActivities[1], type: 'profile_created' },
      { ...mockActivities[2], type: 'order_placed' },
      { id: '4', type: 'report_failed', title: '失敗', description: '分析失敗', timestamp: new Date(), status: 'failed' as const },
    ];

    const { container } = render(<RecentActivity activities={differentTypes} />);

    const icons = container.querySelectorAll('svg');
    expect(icons.length).toBeGreaterThanOrEqual(4);
  });

  it('shows failed status with error styling', () => {
    const failedActivity = [{
      id: '1',
      type: 'report_failed',
      title: '報告生成失敗',
      description: '系統錯誤',
      timestamp: new Date(),
      status: 'failed' as const,
    }];

    const { container } = render(<RecentActivity activities={failedActivity} />);

    const errorBadges = container.querySelectorAll('.bg-error-100');
    expect(errorBadges.length).toBeGreaterThan(0);
  });

  it('applies custom className when provided', () => {
    const { container } = render(
      <RecentActivity activities={mockActivities} className="custom-activity" />
    );

    expect(container.firstChild).toHaveClass('custom-activity');
  });

  it('renders in compact mode when specified', () => {
    const { container } = render(
      <RecentActivity activities={mockActivities} compact={true} />
    );

    const compactItems = container.querySelectorAll('.p-3');
    expect(compactItems.length).toBeGreaterThan(0);
  });

  it('shows refresh button when onRefresh provided', () => {
    const handleRefresh = vi.fn();
    render(<RecentActivity activities={mockActivities} onRefresh={handleRefresh} />);

    expect(screen.getByRole('button', { name: /重新整理|刷新/i })).toBeInTheDocument();
  });

  it('calls onRefresh when refresh button clicked', async () => {
    const user = userEvent.setup();
    const handleRefresh = vi.fn();
    render(<RecentActivity activities={mockActivities} onRefresh={handleRefresh} />);

    const refreshButton = screen.getByRole('button', { name: /重新整理|刷新/i });
    await user.click(refreshButton);

    expect(handleRefresh).toHaveBeenCalledTimes(1);
  });

  it('handles very long descriptions with ellipsis', () => {
    const longDescription = 'A'.repeat(200);
    const activityWithLongDesc = [{
      ...mockActivities[0],
      description: longDescription,
    }];

    const { container } = render(<RecentActivity activities={activityWithLongDesc} />);

    const descElement = container.querySelector('.line-clamp-2');
    expect(descElement).toBeInTheDocument();
  });

  it('shows loading skeleton with correct structure', () => {
    render(<RecentActivity activities={[]} isLoading={true} />);

    const skeletons = screen.getAllByRole('status');
    expect(skeletons.length).toBeGreaterThan(0);
  });
});
