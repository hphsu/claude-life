import React from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { SteppedProgress } from '@/components/ui/Progress';
import { useCreateOrder } from '@/hooks/useOrders';
import type { Profile, ExpertSystem } from '@/types/api';

export interface OrderSummaryProps {
  profile: Profile;
  selectedSystems: ExpertSystem[];
  priceInfo: {
    total: number;
    discount: number;
    final: number;
  };
  onSuccess?: (orderId: string) => void;
  onCancel?: () => void;
}

const expertSystemLabels: Record<ExpertSystem, string> = {
  bazi: '八字命理',
  ziwei: '紫微斗數',
  astrology: '心理占星',
  numerology: '生命靈數',
  plum_blossom: '梅花易數',
  qimen: '奇門遁甲',
  liuyao: '六爻',
  name_analysis: '姓名學',
};

export const OrderSummary: React.FC<OrderSummaryProps> = ({
  profile,
  selectedSystems,
  priceInfo,
  onSuccess,
  onCancel,
}) => {
  const createOrder = useCreateOrder();

  const handleSubmit = async () => {
    try {
      const order = await createOrder.mutateAsync({
        profile_id: profile.id,
        expert_systems: selectedSystems,
      });
      onSuccess?.(order.id);
    } catch (error) {
      console.error('Failed to create order:', error);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('zh-TW', {
      style: 'currency',
      currency: 'TWD',
      minimumFractionDigits: 0,
    }).format(price);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const orderSteps = [
    { id: 'profile', label: '選擇檔案', description: '選擇要分析的檔案' },
    { id: 'systems', label: '選擇系統', description: '選擇命理分析系統' },
    { id: 'review', label: '確認訂單', description: '檢視並確認訂單內容' },
    { id: 'payment', label: '付款', description: '完成付款程序' },
  ];

  return (
    <div className="space-y-6">
      {/* Progress Indicator */}
      <Card>
        <CardContent className="pt-6">
          <SteppedProgress steps={orderSteps} currentStep={2} />
        </CardContent>
      </Card>

      {/* Profile Information */}
      <Card>
        <CardHeader>
          <CardTitle>檔案資訊</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <dt className="text-sm text-neutral-600 mb-1">姓名</dt>
              <dd className="font-medium text-neutral-900">{profile.name}</dd>
            </div>
            <div>
              <dt className="text-sm text-neutral-600 mb-1">性別</dt>
              <dd className="font-medium text-neutral-900">
                {{ M: '男', F: '女', O: '其他' }[profile.gender]}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-neutral-600 mb-1">出生日期</dt>
              <dd className="font-medium text-neutral-900">{formatDate(profile.birth_date)}</dd>
            </div>
            <div>
              <dt className="text-sm text-neutral-600 mb-1">出生時間</dt>
              <dd className="font-medium text-neutral-900">{profile.birth_time}</dd>
            </div>
            <div>
              <dt className="text-sm text-neutral-600 mb-1">出生地點</dt>
              <dd className="font-medium text-neutral-900">{profile.birth_location}</dd>
            </div>
            <div>
              <dt className="text-sm text-neutral-600 mb-1">時區</dt>
              <dd className="font-medium text-neutral-900">{profile.timezone}</dd>
            </div>
          </dl>
        </CardContent>
      </Card>

      {/* Selected Systems */}
      <Card>
        <CardHeader>
          <CardTitle>選擇的命理系統</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            {selectedSystems.map((systemId) => (
              <li
                key={systemId}
                className="flex items-center gap-3 p-3 bg-neutral-50 rounded-lg"
              >
                <svg
                  className="w-5 h-5 text-primary-600 flex-shrink-0"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span className="font-medium text-neutral-900">
                  {expertSystemLabels[systemId]}
                </span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* Price Breakdown */}
      <Card variant="elevated" className="bg-primary-50 border-primary-200">
        <CardHeader>
          <CardTitle>價格明細</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="space-y-3">
            <div className="flex justify-between">
              <dt className="text-neutral-700">小計</dt>
              <dd className="font-medium text-neutral-900">{formatPrice(priceInfo.total)}</dd>
            </div>
            {priceInfo.discount > 0 && (
              <div className="flex justify-between text-success-DEFAULT">
                <dt>組合優惠</dt>
                <dd className="font-medium">-{formatPrice(priceInfo.discount)}</dd>
              </div>
            )}
            <div className="flex justify-between pt-3 border-t border-primary-300">
              <dt className="text-lg font-semibold text-neutral-900">總計</dt>
              <dd className="text-2xl font-bold text-primary-600">
                {formatPrice(priceInfo.final)}
              </dd>
            </div>
          </dl>
        </CardContent>
        <CardFooter>
          <div className="w-full flex items-start gap-2 p-3 bg-primary-100 rounded-lg">
            <svg
              className="w-5 h-5 text-primary-600 flex-shrink-0 mt-0.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <p className="text-sm text-primary-800">
              分析報告將在 24-48 小時內完成。您可以在「報告」頁面查看進度。
            </p>
          </div>
        </CardFooter>
      </Card>

      {/* Action Buttons */}
      <div className="flex justify-end gap-3">
        {onCancel && (
          <Button variant="outline" onClick={onCancel} disabled={createOrder.isPending}>
            返回修改
          </Button>
        )}
        <Button onClick={handleSubmit} isLoading={createOrder.isPending} size="lg">
          確認下單
        </Button>
      </div>

      {createOrder.isError && (
        <Card variant="error">
          <CardContent className="p-4">
            <p className="text-sm text-error-DEFAULT">
              訂單建立失敗：{createOrder.error instanceof Error ? createOrder.error.message : '未知錯誤'}
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
