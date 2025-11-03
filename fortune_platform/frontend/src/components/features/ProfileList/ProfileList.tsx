import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { ProfileCard } from '@/components/features/ProfileCard';
import { ProfileForm } from '@/components/features/ProfileForm';
import { useProfiles } from '@/hooks/useProfiles';
import type { Profile } from '@/types/api';

export interface ProfileListProps {
  onSelect?: (profile: Profile) => void;
  selectedProfileId?: string;
  showCreateButton?: boolean;
}

export const ProfileList: React.FC<ProfileListProps> = ({
  onSelect,
  selectedProfileId,
  showCreateButton = true,
}) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingProfile, setEditingProfile] = useState<Profile | null>(null);

  const { data, isLoading, error } = useProfiles(currentPage, 12);

  const handleCreateSuccess = (profile: Profile) => {
    setShowCreateModal(false);
    onSelect?.(profile);
  };

  const handleEditSuccess = (profile: Profile) => {
    setEditingProfile(null);
    onSelect?.(profile);
  };

  const handleEdit = (profile: Profile) => {
    setEditingProfile(profile);
  };

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
        <p className="text-neutral-600 mb-4">
          {error instanceof Error ? error.message : '無法載入檔案列表'}
        </p>
        <Button onClick={() => window.location.reload()}>重新載入</Button>
      </div>
    );
  }

  if (!data || data.results.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-50 text-primary-600 mb-4">
          <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-neutral-800 mb-2">尚無檔案</h3>
        <p className="text-neutral-600 mb-4">建立第一個檔案以開始命理分析</p>
        {showCreateButton && (
          <Button onClick={() => setShowCreateModal(true)}>建立檔案</Button>
        )}
      </div>
    );
  }

  return (
    <>
      <div className="space-y-6">
        {/* Header with Create Button */}
        {showCreateButton && (
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-bold text-neutral-800">檔案列表</h2>
              <p className="text-neutral-600 mt-1">共 {data.count} 個檔案</p>
            </div>
            <Button onClick={() => setShowCreateModal(true)}>
              <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              建立新檔案
            </Button>
          </div>
        )}

        {/* Profile Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.results.map((profile) => (
            <ProfileCard
              key={profile.id}
              profile={profile}
              onEdit={handleEdit}
              onSelect={onSelect}
              isSelected={selectedProfileId === profile.id}
            />
          ))}
        </div>

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

      {/* Create Profile Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="建立新檔案"
        size="lg"
      >
        <ProfileForm
          onSuccess={handleCreateSuccess}
          onCancel={() => setShowCreateModal(false)}
        />
      </Modal>

      {/* Edit Profile Modal */}
      <Modal
        isOpen={!!editingProfile}
        onClose={() => setEditingProfile(null)}
        title="編輯檔案"
        size="lg"
      >
        {editingProfile && (
          <ProfileForm
            profile={editingProfile}
            onSuccess={handleEditSuccess}
            onCancel={() => setEditingProfile(null)}
          />
        )}
      </Modal>
    </>
  );
};
