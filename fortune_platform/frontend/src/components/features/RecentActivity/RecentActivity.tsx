import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import type { Order, Report } from '@/types/api';

export interface ActivityItem {
  id: string;
  type: 'order' | 'report' | 'profile';
  title: string;
  description: string;
  timestamp: string;
  status?: 'completed' | 'pending' | 'failed';
  actionLabel?: string;
  actionHref?: string;
}

export interface RecentActivityProps {
  activities: ActivityItem[];
  maxItems?: number;
}

export const RecentActivity: React.FC<RecentActivityProps> = ({ activities, maxItems = 5 }) => {
  const displayActivities = activities.slice(0, maxItems);

  const getActivityIcon = (type: ActivityItem['type']) => {
    switch (type) {
      case 'order':
        return (
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        );
      case 'report':
        return (
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        );
      case 'profile':
        return (
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        );
    }
  };

  const getStatusBadge = (status?: ActivityItem['status']) => {
    if (!status) return null;

    const badgeClasses = {
      completed: 'bg-success-50 text-success-700',
      pending: 'bg-warning-50 text-warning-700',
      failed: 'bg-error-50 text-error-700',
    };

    const badgeLabels = {
      completed: '已完成',
      pending: '處理中',
      failed: '失敗',
    };

    return (
      <span className={`px-2 py-1 rounded text-xs font-medium ${badgeClasses[status]}`}>
        {badgeLabels[status]}
      </span>
    );
  };

  const formatRelativeTime = (timestamp: string) => {
    const now = new Date();
    const past = new Date(timestamp);
    const diffMs = now.getTime() - past.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return '剛剛';
    if (diffMins < 60) return `${diffMins} 分鐘前`;
    if (diffHours < 24) return `${diffHours} 小時前`;
    if (diffDays < 7) return `${diffDays} 天前`;
    return past.toLocaleDateString('zh-TW');
  };

  if (displayActivities.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>最近活動</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-neutral-100 text-neutral-400 mb-3">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-sm text-neutral-600">尚無活動記錄</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>最近活動</CardTitle>
          <Button variant="ghost" size="sm" onClick={() => window.location.href = '/orders'}>
            查看全部
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {displayActivities.map((activity) => (
            <div key={activity.id} className="flex items-start gap-4 pb-4 border-b border-neutral-200 last:border-0 last:pb-0">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary-50 text-primary-600 flex-shrink-0">
                {getActivityIcon(activity.type)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-neutral-900">{activity.title}</p>
                    <p className="text-sm text-neutral-600 mt-1">{activity.description}</p>
                  </div>
                  {getStatusBadge(activity.status)}
                </div>
                <div className="flex items-center gap-3 mt-2">
                  <span className="text-xs text-neutral-500">{formatRelativeTime(activity.timestamp)}</span>
                  {activity.actionLabel && activity.actionHref && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => window.location.href = activity.actionHref!}
                      className="text-xs"
                    >
                      {activity.actionLabel}
                    </Button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};
