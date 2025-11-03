import React, { useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Progress } from '@/components/ui/Progress';
import { SafeHTML } from '@/components/common/SafeHTML';
import { useReportContent, useDownloadPdf, useDownloadHtml } from '@/hooks/useReports';
import type { ExpertSystem } from '@/types/api';

export interface ReportViewerProps {
  reportId: string;
  expertSystem?: ExpertSystem;
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

export const ReportViewer: React.FC<ReportViewerProps> = ({
  reportId,
  expertSystem,
}) => {
  const { data: report, isLoading, error } = useReportContent(reportId);
  const downloadPdf = useDownloadPdf();
  const downloadHtml = useDownloadHtml();

  const [showFullReport, setShowFullReport] = useState(false);

  if (isLoading) {
    return (
      <Card>
        <div className="p-6 space-y-4">
          <div className="h-6 bg-neutral-200 rounded animate-pulse" />
          <div className="h-4 bg-neutral-100 rounded animate-pulse" />
          <div className="h-4 bg-neutral-100 rounded animate-pulse w-3/4" />
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card variant="error">
        <div className="p-6">
          <h3 className="text-lg font-semibold text-error-DEFAULT mb-2">
            Failed to Load Report
          </h3>
          <p className="text-sm text-neutral-600">
            {error instanceof Error ? error.message : 'Unknown error occurred'}
          </p>
        </div>
      </Card>
    );
  }

  if (!report) {
    return (
      <Card>
        <div className="p-6">
          <p className="text-neutral-600">No report data available</p>
        </div>
      </Card>
    );
  }

  const expertLabel = expertSystemLabels[report.expert_system] || report.expert_system;

  return (
    <div className="space-y-4">
      {/* Report Header */}
      <Card>
        <div className="p-6">
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <h2 className="text-2xl font-bold text-primary-600">
                {expertLabel}
              </h2>
              <p className="text-sm text-neutral-600">
                Generated on {new Date(report.metadata.generated_at).toLocaleString('zh-TW')}
              </p>
              <p className="text-xs text-neutral-500">
                Version {report.metadata.version}
              </p>
            </div>

            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => downloadPdf.mutate(reportId)}
                isLoading={downloadPdf.isPending}
              >
                Download PDF
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => downloadHtml.mutate(reportId)}
                isLoading={downloadHtml.isPending}
              >
                Download HTML
              </Button>
            </div>
          </div>
        </div>
      </Card>

      {/* Report Content */}
      <Card>
        <div className="p-6">
          {/* Content preview or full view toggle */}
          {!showFullReport && report.html_content.length > 10000 && (
            <div className="mb-4 p-4 bg-primary-50 border border-primary-200 rounded-lg">
              <p className="text-sm text-primary-700 mb-2">
                This is a comprehensive report. Would you like to view it all at once?
              </p>
              <Button
                size="sm"
                onClick={() => setShowFullReport(true)}
              >
                Show Full Report
              </Button>
            </div>
          )}

          {/* Render sanitized HTML content */}
          <div className="prose prose-neutral max-w-none">
            <SafeHTML
              html={
                showFullReport || report.html_content.length <= 10000
                  ? report.html_content
                  : report.html_content.slice(0, 10000) + '...'
              }
            />
          </div>

          {/* Load more button if content is truncated */}
          {!showFullReport && report.html_content.length > 10000 && (
            <div className="mt-6 text-center">
              <Button
                variant="outline"
                onClick={() => setShowFullReport(true)}
              >
                Load Full Report
              </Button>
            </div>
          )}
        </div>
      </Card>

      {/* Additional metadata */}
      {report.metadata && Object.keys(report.metadata).length > 2 && (
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold text-neutral-800 mb-4">
              Report Metadata
            </h3>
            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
              {Object.entries(report.metadata)
                .filter(([key]) => key !== 'generated_at' && key !== 'version')
                .map(([key, value]) => (
                  <div key={key}>
                    <dt className="font-medium text-neutral-600">
                      {key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                    </dt>
                    <dd className="mt-1 text-neutral-800">
                      {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                    </dd>
                  </div>
                ))}
            </dl>
          </div>
        </Card>
      )}
    </div>
  );
};
