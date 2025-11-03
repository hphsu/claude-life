import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@/tests/utils';
import { JobProgress } from './JobProgress';
import * as hooks from '@/hooks/useJobStatus';

// Mock the useJobStatus hook
vi.mock('@/hooks/useJobStatus', () => ({
  useJobStatus: vi.fn(),
}));

describe('JobProgress', () => {
  const mockUseJobStatus = hooks.useJobStatus as ReturnType<typeof vi.fn>;

  beforeEach(() => {
    vi.clearAllMocks();
  });

  const mockJob = {
    id: 'job-123',
    profile_id: 'profile-123',
    expert_system: 'bazi',
    status: 'running' as const,
    progress: 45,
    started_at: new Date('2024-01-15T10:00:00Z'),
    current_step: '分析命盤格局',
    estimated_completion: new Date('2024-01-15T10:10:00Z'),
  };

  it('renders loading state initially', () => {
    mockUseJobStatus.mockReturnValue({
      data: undefined,
      isLoading: true,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        profileName="John Doe"
      />
    );

    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders error state when hook returns error', () => {
    mockUseJobStatus.mockReturnValue({
      data: undefined,
      isLoading: false,
      error: new Error('Failed to fetch job status'),
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        profileName="John Doe"
      />
    );

    expect(screen.getByText(/載入失敗|錯誤/i)).toBeInTheDocument();
  });

  it('displays job information when loaded', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        profileName="John Doe"
      />
    );

    expect(screen.getByText('八字命理')).toBeInTheDocument();
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  it('shows correct status for queued jobs', () => {
    mockUseJobStatus.mockReturnValue({
      data: { ...mockJob, status: 'queued', progress: 0 },
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    expect(screen.getByText('排隊中')).toBeInTheDocument();
  });

  it('shows correct status for running jobs', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    expect(screen.getByText('分析中')).toBeInTheDocument();
  });

  it('shows correct status for completed jobs', () => {
    mockUseJobStatus.mockReturnValue({
      data: { ...mockJob, status: 'completed', progress: 100 },
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    expect(screen.getByText('已完成')).toBeInTheDocument();
  });

  it('shows correct status for failed jobs', () => {
    mockUseJobStatus.mockReturnValue({
      data: { ...mockJob, status: 'failed', error_message: '系統錯誤' },
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    expect(screen.getByText('失敗')).toBeInTheDocument();
  });

  it('displays progress bar with correct percentage', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    const { container } = render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    const progressBar = container.querySelector('[style*="width: 45%"]');
    expect(progressBar).toBeInTheDocument();
    expect(screen.getByText('45%')).toBeInTheDocument();
  });

  it('shows current step for running jobs', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        showDetails={true}
      />
    );

    expect(screen.getByText('分析命盤格局')).toBeInTheDocument();
  });

  it('displays started time', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        showDetails={true}
      />
    );

    expect(screen.getByText(/開始時間/i)).toBeInTheDocument();
  });

  it('displays estimated completion time', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        showDetails={true}
      />
    );

    expect(screen.getByText(/預計完成/i)).toBeInTheDocument();
  });

  it('hides details when showDetails is false', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        showDetails={false}
      />
    );

    expect(screen.queryByText(/開始時間/i)).not.toBeInTheDocument();
    expect(screen.queryByText('分析命盤格局')).not.toBeInTheDocument();
  });

  it('shows error message for failed jobs', () => {
    const errorMessage = '系統錯誤：無法連接到分析服務器';
    mockUseJobStatus.mockReturnValue({
      data: { ...mockJob, status: 'failed', error_message: errorMessage },
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  it('shows completion time for completed jobs', () => {
    mockUseJobStatus.mockReturnValue({
      data: {
        ...mockJob,
        status: 'completed',
        progress: 100,
        completed_at: new Date('2024-01-15T10:08:00Z'),
      },
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        showDetails={true}
      />
    );

    expect(screen.getByText(/完成時間/i)).toBeInTheDocument();
  });

  it('calculates and displays duration', () => {
    mockUseJobStatus.mockReturnValue({
      data: {
        ...mockJob,
        status: 'completed',
        progress: 100,
        started_at: new Date('2024-01-15T10:00:00Z'),
        completed_at: new Date('2024-01-15T10:08:00Z'),
      },
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        showDetails={true}
      />
    );

    expect(screen.getByText(/8.*分鐘/i)).toBeInTheDocument();
  });

  it('shows animated spinner for running status', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    const { container } = render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    const spinner = container.querySelector('.animate-spin');
    expect(spinner).toBeInTheDocument();
  });

  it('shows checkmark icon for completed status', () => {
    mockUseJobStatus.mockReturnValue({
      data: { ...mockJob, status: 'completed', progress: 100 },
      isLoading: false,
      error: null,
    });

    const { container } = render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    // Check for checkmark SVG path
    const checkmark = container.querySelector('svg[viewBox*="24"]');
    expect(checkmark).toBeInTheDocument();
  });

  it('shows X icon for failed status', () => {
    mockUseJobStatus.mockReturnValue({
      data: { ...mockJob, status: 'failed' },
      isLoading: false,
      error: null,
    });

    const { container } = render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    // Check for X mark SVG
    const xMark = container.querySelector('svg[viewBox*="24"]');
    expect(xMark).toBeInTheDocument();
  });

  it('applies correct color classes for different statuses', () => {
    const statuses = ['queued', 'running', 'completed', 'failed'] as const;

    statuses.forEach((status) => {
      const { container } = render(
        <JobProgress
          jobId="job-123"
          expertSystem="八字命理"
        />
      );

      mockUseJobStatus.mockReturnValue({
        data: { ...mockJob, status },
        isLoading: false,
        error: null,
      });
    });
  });

  it('handles missing profile name gracefully', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    expect(screen.getByText('八字命理')).toBeInTheDocument();
  });

  it('polls for updates at regular intervals', async () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
      />
    );

    // Verify hook was called with correct jobId
    expect(mockUseJobStatus).toHaveBeenCalledWith('job-123');
  });

  it('renders compact mode when specified', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    const { container } = render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        compact={true}
      />
    );

    const compactCard = container.querySelector('.p-3');
    expect(compactCard).toBeInTheDocument();
  });

  it('applies custom className when provided', () => {
    mockUseJobStatus.mockReturnValue({
      data: mockJob,
      isLoading: false,
      error: null,
    });

    const { container } = render(
      <JobProgress
        jobId="job-123"
        expertSystem="八字命理"
        className="custom-job-progress"
      />
    );

    expect(container.firstChild).toHaveClass('custom-job-progress');
  });
});
