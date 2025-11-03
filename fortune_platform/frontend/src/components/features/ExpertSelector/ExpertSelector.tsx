import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { useExpertSystems, useCalculatePrice } from '@/hooks/useOrders';
import type { ExpertSystem, ExpertSystemInfo } from '@/types/api';

export interface ExpertSelectorProps {
  selectedSystems: ExpertSystem[];
  onSelectionChange: (systems: ExpertSystem[]) => void;
  showPricing?: boolean;
}

const expertSystemLabels: Record<ExpertSystem, { name: string; description: string }> = {
  bazi: {
    name: '八字命理',
    description: '分析出生年月日時的天干地支，揭示命運軌跡',
  },
  ziwei: {
    name: '紫微斗數',
    description: '紫微星系統分析，解析人生格局與運勢',
  },
  astrology: {
    name: '心理占星',
    description: '西洋占星學分析，探索性格與人生方向',
  },
  numerology: {
    name: '生命靈數',
    description: '數字能量分析，了解生命密碼與潛能',
  },
  plum_blossom: {
    name: '梅花易數',
    description: '時間起卦，預測事件發展與趨勢',
  },
  qimen: {
    name: '奇門遁甲',
    description: '時空能量分析，找出最佳行動時機',
  },
  liuyao: {
    name: '六爻',
    description: '金錢卦占測，解答具體問題',
  },
  name_analysis: {
    name: '姓名學',
    description: '姓名筆劃五行分析，評估名字能量',
  },
};

export const ExpertSelector: React.FC<ExpertSelectorProps> = ({
  selectedSystems,
  onSelectionChange,
  showPricing = true,
}) => {
  const { data: systems, isLoading } = useExpertSystems();
  const calculatePrice = useCalculatePrice();
  const [priceInfo, setPriceInfo] = useState<{ total: number; discount: number; final: number } | null>(null);

  useEffect(() => {
    if (selectedSystems.length > 0 && showPricing) {
      calculatePrice.mutate(selectedSystems, {
        onSuccess: (data) => setPriceInfo(data),
      });
    } else {
      setPriceInfo(null);
    }
  }, [selectedSystems, showPricing]);

  const handleToggle = (systemId: ExpertSystem) => {
    if (selectedSystems.includes(systemId)) {
      onSelectionChange(selectedSystems.filter((id) => id !== systemId));
    } else {
      onSelectionChange([...selectedSystems, systemId]);
    }
  };

  const getSystemInfo = (systemId: ExpertSystem): ExpertSystemInfo | undefined => {
    return systems?.find((s) => s.id === systemId);
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('zh-TW', {
      style: 'currency',
      currency: 'TWD',
      minimumFractionDigits: 0,
    }).format(price);
  };

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="h-48 bg-neutral-200 rounded-lg animate-pulse" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Expert Systems Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {Object.entries(expertSystemLabels).map(([systemId, info]) => {
          const system = getSystemInfo(systemId as ExpertSystem);
          const isSelected = selectedSystems.includes(systemId as ExpertSystem);
          const isAvailable = system?.is_available ?? true;

          return (
            <Card
              key={systemId}
              variant={isSelected ? 'elevated' : 'bordered'}
              className={`cursor-pointer transition-all ${
                isSelected ? 'ring-2 ring-primary-500' : ''
              } ${!isAvailable ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-md'}`}
              onClick={() => isAvailable && handleToggle(systemId as ExpertSystem)}
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="text-base">{info.name}</CardTitle>
                  <div
                    className={`flex items-center justify-center h-6 w-6 rounded border-2 transition-colors ${
                      isSelected
                        ? 'bg-primary-500 border-primary-500'
                        : 'border-neutral-300'
                    }`}
                  >
                    {isSelected && (
                      <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </div>
                </div>
                <CardDescription className="text-xs line-clamp-2">
                  {info.description}
                </CardDescription>
              </CardHeader>

              <CardContent>
                <div className="space-y-2">
                  {system && (
                    <>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-neutral-600">價格</span>
                        <span className="font-semibold text-primary-600">
                          {formatPrice(system.price)}
                        </span>
                      </div>
                      {system.estimated_time && (
                        <div className="flex justify-between items-center text-xs text-neutral-500">
                          <span>預估時間</span>
                          <span>{system.estimated_time}</span>
                        </div>
                      )}
                    </>
                  )}
                  {!isAvailable && (
                    <div className="text-xs text-error-DEFAULT">暫時無法使用</div>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Pricing Summary */}
      {showPricing && selectedSystems.length > 0 && priceInfo && (
        <Card variant="elevated" className="bg-primary-50 border-primary-200">
          <CardContent className="p-6">
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-neutral-700">已選擇 {selectedSystems.length} 個系統</span>
                <span className="text-neutral-900 font-medium">{formatPrice(priceInfo.total)}</span>
              </div>
              {priceInfo.discount > 0 && (
                <div className="flex justify-between items-center text-success-DEFAULT">
                  <span>組合優惠折扣</span>
                  <span className="font-medium">-{formatPrice(priceInfo.discount)}</span>
                </div>
              )}
              <div className="flex justify-between items-center pt-3 border-t border-primary-300">
                <span className="text-lg font-semibold text-neutral-900">總計</span>
                <span className="text-2xl font-bold text-primary-600">
                  {formatPrice(priceInfo.final)}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Bundle Discount Info */}
      {selectedSystems.length >= 3 && (
        <div className="flex items-center gap-2 p-4 bg-success-50 border border-success-200 rounded-lg">
          <svg className="w-5 h-5 text-success-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-sm text-success-700">
            選擇 3 個或更多系統可享組合優惠！選擇越多，折扣越大。
          </p>
        </div>
      )}
    </div>
  );
};
