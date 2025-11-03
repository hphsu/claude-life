import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { useDeleteProfile } from '@/hooks/useProfiles';
import type { Profile } from '@/types/api';

export interface ProfileCardProps {
  profile: Profile;
  onEdit?: (profile: Profile) => void;
  onSelect?: (profile: Profile) => void;
  isSelected?: boolean;
}

export const ProfileCard: React.FC<ProfileCardProps> = ({
  profile,
  onEdit,
  onSelect,
  isSelected = false,
}) => {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const deleteMutation = useDeleteProfile();

  const handleDelete = async () => {
    try {
      await deleteMutation.mutateAsync(profile.id);
      setShowDeleteModal(false);
    } catch (error) {
      console.error('Failed to delete profile:', error);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const genderLabels: Record<string, string> = {
    M: '男',
    F: '女',
    O: '其他',
  };

  return (
    <>
      <Card
        variant={isSelected ? 'elevated' : 'default'}
        className={isSelected ? 'ring-2 ring-primary-500' : ''}
      >
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle>{profile.name}</CardTitle>
              <CardDescription>
                {genderLabels[profile.gender]} • {profile.birth_location}
              </CardDescription>
            </div>
            {isSelected && (
              <div className="flex items-center justify-center h-6 w-6 rounded-full bg-primary-500 text-white text-xs font-medium">
                ✓
              </div>
            )}
          </div>
        </CardHeader>

        <CardContent>
          <dl className="space-y-2 text-sm">
            <div className="flex justify-between">
              <dt className="text-neutral-600">出生日期</dt>
              <dd className="font-medium text-neutral-900">{formatDate(profile.birth_date)}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-neutral-600">出生時間</dt>
              <dd className="font-medium text-neutral-900">{profile.birth_time}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-neutral-600">時區</dt>
              <dd className="font-medium text-neutral-900">{profile.timezone}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-neutral-600">建立日期</dt>
              <dd className="text-neutral-700">{formatDate(profile.created_at)}</dd>
            </div>
          </dl>
        </CardContent>

        <CardFooter className="flex gap-2">
          {onSelect && (
            <Button
              variant={isSelected ? 'primary' : 'outline'}
              size="sm"
              onClick={() => onSelect(profile)}
              className="flex-1"
            >
              {isSelected ? '已選擇' : '選擇此檔案'}
            </Button>
          )}
          {onEdit && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => onEdit(profile)}
            >
              編輯
            </Button>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowDeleteModal(true)}
            className="text-error-DEFAULT hover:text-error-dark hover:bg-error-50"
          >
            刪除
          </Button>
        </CardFooter>
      </Card>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="確認刪除"
        size="sm"
      >
        <div className="space-y-4">
          <p className="text-neutral-600">
            確定要刪除 <strong>{profile.name}</strong> 的檔案嗎？此操作無法復原。
          </p>
          <div className="flex justify-end gap-2">
            <Button
              variant="outline"
              onClick={() => setShowDeleteModal(false)}
              disabled={deleteMutation.isPending}
            >
              取消
            </Button>
            <Button
              variant="danger"
              onClick={handleDelete}
              isLoading={deleteMutation.isPending}
            >
              確認刪除
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
};
