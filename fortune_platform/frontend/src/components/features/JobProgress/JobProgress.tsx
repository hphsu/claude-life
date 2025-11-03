import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { useJobStatus } from '@/hooks/useJobStatus';

export interface JobProgressProps {
  jobId: string;
  expertSystem: string;
  profileName?: string;
  showDetails?: boolean;
}

export const JobProgress: React.FC<JobProgressProps> = ({
  jobId,
  expertSystem,
  profileName,
  showDetails = true,
}) => {
  const { data: job, isLoading, error } = useJobStatus(jobId);

  const expertSystemLabels: Record<string, string> = {
    bazi: '八字命理',
    ziwei: '紫微斗數',
    astrology: '心理占星',
    numerology: '生命靈數',
    plum_blossom: '梅花易數',
    qimen: '奇門遁甲',
    liuyao: '六爻',
    name_analysis: '姓名學',
  };

  const getStatusInfo = (status: string) => {
    const statusMap = {
      queued: {
        label: '排隊中',
        color: 'bg-neutral-100 text-neutral-700',
        icon: (
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        ),
      },
      running: {
        label: '分析中',
        color: 'bg-primary-100 text-primary-700',
        icon: (
          <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        ),
      },
      completed: {
        label: '已完成',
        color: 'bg-success-100 text-success-700',
        icon: (
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        ),
      },
      failed: {
        label: '失敗',
        color: 'bg-error-100 text-error-700',
        icon: (
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        ),
      },
    };

    return statusMap[status as keyof typeof statusMap] || statusMap.queued;
  };

  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${seconds} 秒`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes} 分鐘`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours} 小時 ${mins} 分鐘`;
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString('zh-TW', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (isLoading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-neutral-100 animate-pulse" />
            <div className="flex-1">
              <div className="h-5 bg-neutral-100 rounded w-32 mb-2 animate-pulse" />
              <div className="h-4 bg-neutral-100 rounded w-48 animate-pulse" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card variant="elevated" className="border-error-200 bg-error-50">
        <CardContent className="p-6">
          <div className="flex items-start gap-3">
            <div className="flex items-center justify-center w-10 h-10 rounded-full bg-error-100 text-error-600">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h4 className="font-semibold text-error-900">無法載入工作狀態</h4>
              <p className="text-sm text-error-700 mt-1">請稍後重試或聯繫客服</p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!job) {
    return null;
  }

  const statusInfo = getStatusInfo(job.status);
  const progress = job.progress || 0;

  return (
    <Card variant="elevated">
      <CardContent className="p-6">
        <div className="space-y-4">
          {/* Header */}
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h3 className="font-semibold text-neutral-900">
                  {expertSystemLabels[expertSystem] || expertSystem}
                </h3>
                <span className={`px-2 py-1 rounded text-xs font-medium ${statusInfo.color}`}>
                  {statusInfo.label}
                </span>
              </div>
              {profileName && (
                <p className="text-sm text-neutral-600">檔案：{profileName}</p>
              )}
            </div>
            <div className={`flex items-center justify-center w-10 h-10 rounded-full ${statusInfo.color.replace('text-', 'bg-').replace('-700', '-50')}`}>
              {statusInfo.icon}
            </div>
          </div>

          {/* Progress Bar */}
          {job.status === 'running' || job.status === 'completed' ? (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-neutral-600">進度</span>
                <span className="font-medium text-neutral-900">{progress}%</span>
              </div>
              <div className="w-full bg-neutral-200 rounded-full h-2 overflow-hidden">
                <div
                  className={`h-full transition-all duration-300 ${
                    job.status === 'completed' ? 'bg-success-600' : 'bg-primary-600'
                  }`}
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          ) : null}

          {/* Details */}
          {showDetails && (
            <div className="grid grid-cols-2 gap-4 pt-4 border-t border-neutral-200">
              {job.started_at && (
                <div>
                  <p className="text-xs text-neutral-500">開始時間</p>
                  <p className="text-sm font-medium text-neutral-900 mt-1">
                    {formatTimestamp(job.started_at)}
                  </p>
                </div>
              )}
              {job.completed_at && (
                <div>
                  <p className="text-xs text-neutral-500">完成時間</p>
                  <p className="text-sm font-medium text-neutral-900 mt-1">
                    {formatTimestamp(job.completed_at)}
                  </p>
                </div>
              )}
              {job.duration && (
                <div>
                  <p className="text-xs text-neutral-500">處理時長</p>
                  <p className="text-sm font-medium text-neutral-900 mt-1">
                    {formatDuration(job.duration)}
                  </p>
                </div>
              )}
              {job.estimated_completion && job.status === 'running' && (
                <div>
                  <p className="text-xs text-neutral-500">預計完成</p>
                  <p className="text-sm font-medium text-neutral-900 mt-1">
                    {formatTimestamp(job.estimated_completion)}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Current Step */}
          {job.current_step && job.status === 'running' && (
            <div className="pt-4 border-t border-neutral-200">
              <p className="text-xs text-neutral-500 mb-1">當前步驟</p>
              <p className="text-sm text-neutral-900">{job.current_step}</p>
            </div>
          )}

          {/* Error Message */}
          {job.error_message && job.status === 'failed' && (
            <div className="pt-4 border-t border-neutral-200">
              <p className="text-xs text-error-600 mb-1">錯誤訊息</p>
              <p className="text-sm text-error-900">{job.error_message}</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
