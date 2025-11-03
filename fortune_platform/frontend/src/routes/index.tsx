import React, { useState } from 'react';
import { createBrowserRouter, RouterProvider, Navigate, useParams } from 'react-router-dom';
import { AuthProvider } from '@/contexts/AuthContext';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { LoginForm } from '@/components/auth/LoginForm';
import { RegisterForm } from '@/components/auth/RegisterForm';
import { ProfileList } from '@/components/features/ProfileList';
import { ExpertSelector } from '@/components/features/ExpertSelector';
import { OrderSummary } from '@/components/features/OrderSummary';
import { DashboardStats } from '@/components/features/DashboardStats';
import { RecentActivity } from '@/components/features/RecentActivity';
import type { ActivityItem } from '@/components/features/RecentActivity';
import { JobProgress } from '@/components/features/JobProgress';
import { ReportViewer } from '@/components/features/ReportViewer';
import { Button } from '@/components/ui/Button';
import { SteppedProgress } from '@/components/ui/Progress';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import type { Profile, ExpertSystem } from '@/types/api';
import { useProfiles } from '@/hooks/useProfiles';
import { useOrders } from '@/hooks/useOrders';
import { useReports, useReport } from '@/hooks/useReports';

// Layouts
const MainLayout = React.lazy(() => import('@/layouts/MainLayout'));

// Pages
const Dashboard = () => {
  const { data: profilesData } = useProfiles(1, 100);
  const { data: ordersData } = useOrders(1, 100);
  const { data: reportsData } = useReports(1, 100);

  // Calculate statistics
  const totalProfiles = profilesData?.count || 0;
  const totalOrders = ordersData?.count || 0;
  const completedReports = reportsData?.results.filter(r => r.status === 'completed').length || 0;
  const pendingJobs = reportsData?.results.filter(r => r.status === 'pending').length || 0;

  // Generate recent activities from orders and reports
  const recentActivities: ActivityItem[] = React.useMemo(() => {
    const activities: ActivityItem[] = [];

    // Add recent orders
    if (ordersData?.results) {
      ordersData.results.slice(0, 3).forEach(order => {
        activities.push({
          id: `order-${order.id}`,
          type: 'order',
          title: '建立新訂單',
          description: `選擇了 ${order.expert_systems.length} 個命理系統`,
          timestamp: order.created_at,
          status: order.status === 'completed' ? 'completed' : 'pending',
          actionLabel: '查看訂單',
          actionHref: `/orders/${order.id}`,
        });
      });
    }

    // Add recent reports
    if (reportsData?.results) {
      reportsData.results.slice(0, 3).forEach(report => {
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

        activities.push({
          id: `report-${report.id}`,
          type: 'report',
          title: `${expertSystemLabels[report.expert_system]} 分析報告`,
          description: report.status === 'completed' ? '分析已完成' : '分析處理中',
          timestamp: report.created_at,
          status: report.status,
          actionLabel: report.status === 'completed' ? '查看報告' : '查看進度',
          actionHref: report.status === 'completed' ? `/reports/${report.id}` : `/orders`,
        });
      });
    }

    // Sort by timestamp
    return activities.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  }, [ordersData, reportsData]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-primary-600">控制台</h1>
        <p className="mt-2 text-neutral-600">歡迎回到命理分析平台</p>
      </div>

      <DashboardStats
        totalProfiles={totalProfiles}
        totalOrders={totalOrders}
        completedReports={completedReports}
        pendingJobs={pendingJobs}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentActivity activities={recentActivities} maxItems={5} />

        <Card>
          <CardHeader>
            <CardTitle>快速操作</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <Button
                onClick={() => window.location.href = '/profiles'}
                className="w-full justify-start"
                variant="outline"
              >
                <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                管理檔案
              </Button>
              <Button
                onClick={() => window.location.href = '/orders'}
                className="w-full justify-start"
                variant="outline"
              >
                <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                建立新訂單
              </Button>
              <Button
                onClick={() => window.location.href = '/reports'}
                className="w-full justify-start"
                variant="outline"
              >
                <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                查看報告
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {pendingJobs > 0 && (
        <Card variant="elevated" className="bg-primary-50 border-primary-200">
          <CardContent className="p-6">
            <div className="flex items-start gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary-100 text-primary-600 flex-shrink-0">
                <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-primary-900">正在分析中</h3>
                <p className="text-sm text-primary-800 mt-1">
                  您有 {pendingJobs} 個命理系統正在處理中，預計在 24-48 小時內完成。
                </p>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => window.location.href = '/reports'}
                  className="mt-2 text-primary-700 hover:text-primary-900"
                >
                  查看進度 →
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

const ProfilesPage = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-primary-600">檔案管理</h1>
      </div>
      <ProfileList showCreateButton={true} />
    </div>
  );
};

const OrdersPage = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedProfile, setSelectedProfile] = useState<Profile | null>(null);
  const [selectedSystems, setSelectedSystems] = useState<ExpertSystem[]>([]);
  const [priceInfo, setPriceInfo] = useState<{ total: number; discount: number; final: number } | null>(null);

  const orderSteps = [
    { id: 'profile', label: '選擇檔案', description: '選擇要分析的檔案' },
    { id: 'systems', label: '選擇系統', description: '選擇命理分析系統' },
    { id: 'review', label: '確認訂單', description: '檢視並確認訂單內容' },
    { id: 'payment', label: '完成', description: '訂單已建立' },
  ];

  const handleProfileSelect = (profile: Profile) => {
    setSelectedProfile(profile);
    setCurrentStep(1);
  };

  const handleSystemsConfirm = () => {
    if (selectedSystems.length > 0) {
      setCurrentStep(2);
    }
  };

  const handleOrderSuccess = (orderId: string) => {
    setCurrentStep(3);
    // Could redirect to orders list or show success message
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-primary-600">建立訂單</h1>
      </div>

      {/* Progress Indicator */}
      <Card>
        <CardContent className="pt-6">
          <SteppedProgress steps={orderSteps} currentStep={currentStep} />
        </CardContent>
      </Card>

      {/* Step Content */}
      {currentStep === 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-neutral-800">選擇檔案</h2>
          <ProfileList onSelect={handleProfileSelect} selectedProfileId={selectedProfile?.id} showCreateButton={true} />
        </div>
      )}

      {currentStep === 1 && selectedProfile && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-neutral-800">選擇命理系統</h2>
            <Button variant="outline" onClick={handleBack}>返回選擇檔案</Button>
          </div>
          <ExpertSelector
            selectedSystems={selectedSystems}
            onSelectionChange={setSelectedSystems}
            showPricing={true}
          />
          <div className="flex justify-end">
            <Button onClick={handleSystemsConfirm} disabled={selectedSystems.length === 0} size="lg">
              下一步：確認訂單
            </Button>
          </div>
        </div>
      )}

      {currentStep === 2 && selectedProfile && selectedSystems.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-neutral-800">確認訂單</h2>
          <OrderSummary
            profile={selectedProfile}
            selectedSystems={selectedSystems}
            priceInfo={priceInfo || { total: 0, discount: 0, final: 0 }}
            onSuccess={handleOrderSuccess}
            onCancel={handleBack}
          />
        </div>
      )}

      {currentStep === 3 && (
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-success-50 text-success-600 mb-4">
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-neutral-800 mb-2">訂單已建立</h3>
          <p className="text-neutral-600 mb-6">您的命理分析訂單已成功建立，分析結果將在 24-48 小時內完成。</p>
          <div className="flex justify-center gap-4">
            <Button variant="outline" onClick={() => window.location.href = '/reports'}>查看報告</Button>
            <Button onClick={() => { setCurrentStep(0); setSelectedProfile(null); setSelectedSystems([]); }}>
              建立新訂單
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

const ReportsPage = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedTab, setSelectedTab] = useState<'all' | 'pending' | 'completed'>('all');
  const { data, isLoading, error } = useReports(currentPage, 12);

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="h-64 bg-neutral-200 rounded-lg animate-pulse" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-error-50 text-error-DEFAULT mb-4">
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-neutral-800 mb-2">載入失敗</h3>
        <p className="text-neutral-600">{error instanceof Error ? error.message : '無法載入報告列表'}</p>
      </div>
    );
  }

  if (!data || data.results.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-50 text-primary-600 mb-4">
          <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-neutral-800 mb-2">尚無報告</h3>
        <p className="text-neutral-600 mb-4">建立訂單後，您的命理分析報告將在這裡顯示</p>
        <Button onClick={() => window.location.href = '/orders'}>建立訂單</Button>
      </div>
    );
  }

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

  // Filter reports based on selected tab
  const filteredReports = data.results.filter((report) => {
    if (selectedTab === 'pending') return report.status === 'pending';
    if (selectedTab === 'completed') return report.status === 'completed';
    return true;
  });

  const pendingReports = data.results.filter(r => r.status === 'pending');
  const completedReports = data.results.filter(r => r.status === 'completed');

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-primary-600">分析報告</h1>
        <p className="text-neutral-600">共 {data.count} 份報告</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-neutral-200">
        <button
          onClick={() => setSelectedTab('all')}
          className={`px-4 py-2 font-medium transition-colors ${
            selectedTab === 'all'
              ? 'text-primary-600 border-b-2 border-primary-600'
              : 'text-neutral-600 hover:text-neutral-800'
          }`}
        >
          全部 ({data.count})
        </button>
        <button
          onClick={() => setSelectedTab('pending')}
          className={`px-4 py-2 font-medium transition-colors ${
            selectedTab === 'pending'
              ? 'text-primary-600 border-b-2 border-primary-600'
              : 'text-neutral-600 hover:text-neutral-800'
          }`}
        >
          處理中 ({pendingReports.length})
        </button>
        <button
          onClick={() => setSelectedTab('completed')}
          className={`px-4 py-2 font-medium transition-colors ${
            selectedTab === 'completed'
              ? 'text-primary-600 border-b-2 border-primary-600'
              : 'text-neutral-600 hover:text-neutral-800'
          }`}
        >
          已完成 ({completedReports.length})
        </button>
      </div>

      {/* Pending Jobs Progress */}
      {selectedTab !== 'completed' && pendingReports.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-neutral-800">處理中的分析</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {pendingReports.map((report) => (
              <JobProgress
                key={report.id}
                jobId={report.job_id}
                expertSystem={report.expert_system}
                profileName={report.profile_name}
                showDetails={true}
              />
            ))}
          </div>
        </div>
      )}

      {/* Completed Reports Grid */}
      {selectedTab !== 'pending' && completedReports.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-neutral-800">已完成的報告</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {completedReports.map((report) => (
              <Card key={report.id} className="cursor-pointer hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="space-y-4">
                    <div className="flex items-start justify-between">
                      <h3 className="text-lg font-semibold text-neutral-800">
                        {expertSystemLabels[report.expert_system] || report.expert_system}
                      </h3>
                      <span className="px-2 py-1 rounded text-xs font-medium bg-success-50 text-success-700">
                        已完成
                      </span>
                    </div>
                    <div className="text-sm text-neutral-600">
                      <p>檔案：{report.profile_name}</p>
                      <p>訂單：{report.order_id.slice(0, 8)}...</p>
                      <p>建立時間：{new Date(report.created_at).toLocaleDateString('zh-TW')}</p>
                    </div>
                    <Button
                      onClick={() => window.location.href = `/reports/${report.id}`}
                      className="w-full"
                    >
                      查看報告
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Empty State for Filtered View */}
      {filteredReports.length === 0 && (
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-neutral-100 text-neutral-400 mb-4">
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-neutral-800 mb-2">無符合條件的報告</h3>
          <p className="text-neutral-600">
            {selectedTab === 'pending' ? '目前沒有處理中的分析' : '目前沒有已完成的報告'}
          </p>
        </div>
      )}

      {/* Pagination */}
      {data.count > 12 && (
        <div className="flex justify-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={!data.previous || currentPage === 1}
          >
            上一頁
          </Button>
          <div className="flex items-center px-4 text-sm text-neutral-600">
            第 {currentPage} 頁 / 共 {Math.ceil(data.count / 12)} 頁
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentPage((p) => p + 1)}
            disabled={!data.next}
          >
            下一頁
          </Button>
        </div>
      )}
    </div>
  );
};

const ReportDetailPage = () => {
  const { reportId } = useParams<{ reportId: string }>();
  const { data: report, isLoading, error } = useReport(reportId || '');

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-neutral-600">載入報告中...</p>
        </div>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="text-center py-12">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-error-50 text-error-DEFAULT mb-4">
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-neutral-800 mb-2">找不到報告</h3>
        <p className="text-neutral-600 mb-4">
          {error instanceof Error ? error.message : '報告不存在或已被刪除'}
        </p>
        <Button onClick={() => window.location.href = '/reports'}>返回報告列表</Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          onClick={() => window.location.href = '/reports'}
          className="flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          返回列表
        </Button>
      </div>

      <ReportViewer reportId={reportId || ''} />
    </div>
  );
};

// Login and Register pages
const LoginPage = () => <LoginForm />;
const RegisterPage = () => <RegisterForm />;

// Router configuration
export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/register',
    element: <RegisterPage />,
  },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <React.Suspense fallback={<div className="p-8">Loading...</div>}>
          <MainLayout />
        </React.Suspense>
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: 'dashboard',
        element: <Dashboard />,
      },
      {
        path: 'profiles',
        element: <ProfilesPage />,
      },
      {
        path: 'orders',
        element: <OrdersPage />,
      },
      {
        path: 'reports',
        element: <ReportsPage />,
      },
      {
        path: 'reports/:reportId',
        element: <ReportDetailPage />,
      },
    ],
  },
  {
    path: '*',
    element: <Navigate to="/dashboard" replace />,
  },
]);

// Router component for App wrapped with AuthProvider
export const AppRouter: React.FC = () => {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
};
