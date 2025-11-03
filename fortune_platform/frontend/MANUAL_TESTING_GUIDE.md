# Manual Testing Guide - Fortune Platform Frontend

## Prerequisites

### 1. Environment Setup
```bash
# Navigate to frontend directory
cd /Users/frank/src/life/fortune_platform/frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev
```

The application will be available at: **http://localhost:3000**

### 2. Backend Requirements
Ensure the backend API is running for full functionality testing. The frontend expects API endpoints at the configured base URL.

## Testing Workflows

### Workflow 1: Profile Management

#### Test Case 1.1: Create New Profile
1. **Navigate** to http://localhost:3000/profiles
2. **Click** "新增命盤" or "建立命盤" button
3. **Fill in the form**:
   - 姓名 (Name): Enter "測試用戶"
   - 性別 (Gender): Select "男性" or "女性"
   - 出生日期 (Birth Date): Select "1990-05-15"
   - 出生時間 (Birth Time): Enter "14:30" (optional)
   - 出生地點 (Birth Location): Enter "台北市"
   - 時區 (Timezone): Select "Asia/Taipei"
4. **Click** "確認" or "送出" button
5. **Verify**:
   - ✅ Profile appears in the list
   - ✅ Name "測試用戶" is displayed
   - ✅ Birth date "1990-05-15" is shown
   - ✅ Success message appears (if implemented)

#### Test Case 1.2: Validation Errors
1. **Click** "新增命盤" button
2. **Leave all required fields empty**
3. **Click** "確認" button
4. **Verify**:
   - ✅ Validation errors appear for required fields
   - ✅ Form is not submitted
   - ✅ Error messages in Traditional Chinese

#### Test Case 1.3: Edit Existing Profile
1. **Find a profile** in the list
2. **Click** "編輯" button
3. **Modify** the name to "更新用戶"
4. **Click** "確認" button
5. **Verify**:
   - ✅ Profile name updated to "更新用戶"
   - ✅ Other information remains unchanged
   - ✅ Update confirmation appears

#### Test Case 1.4: Delete Profile
1. **Find a profile** to delete
2. **Click** "刪除" button
3. **Confirm** deletion in dialog
4. **Verify**:
   - ✅ Profile removed from list
   - ✅ Profile count decreased by 1
   - ✅ Deletion confirmation appears

#### Test Case 1.5: Profile List Pagination
1. **Create 15+ profiles** (if pagination threshold is 12)
2. **Verify**:
   - ✅ Pagination controls appear
   - ✅ Maximum 12 profiles per page
3. **Click** "下一頁" or "Next"
4. **Verify**:
   - ✅ URL changes to include `?page=2`
   - ✅ Next page of profiles loads
5. **Click** "上一頁" or "Previous"
6. **Verify**:
   - ✅ Returns to page 1
   - ✅ URL updates accordingly

### Workflow 2: Order Placement

#### Test Case 2.1: Complete Order Flow
1. **Navigate** to profiles page
2. **Select a profile** or create new one
3. **Click** "訂購分析" or similar action button
4. **Expert System Selection**:
   - ✅ Verify all 8 systems displayed:
     - 八字命理分析 (NT$299)
     - 紫微斗數分析 (NT$299)
     - 心理占星分析 (NT$299)
     - 姓名學分析 (NT$199)
     - 六爻占卜 (NT$199)
     - 梅花易數 (NT$199)
     - 生命靈數分析 (NT$199)
     - 奇門遁甲分析 (NT$299)
5. **Select 2-3 individual systems**
6. **Verify**:
   - ✅ Selected systems highlighted
   - ✅ Total price calculated correctly
   - ✅ Price displayed as "總計: NT$XXX"

#### Test Case 2.2: Bundle Selection
1. **In expert selection screen**
2. **Click** bundle option (if available)
3. **Verify**:
   - ✅ All systems selected
   - ✅ Bundle discount applied
   - ✅ Savings amount displayed
   - ✅ Bundle price lower than individual sum

#### Test Case 2.3: Order Summary Review
1. **After selecting systems**
2. **Click** "下一步" or "Continue"
3. **Verify Order Summary displays**:
   - ✅ Profile name and details
   - ✅ Selected expert systems list
   - ✅ Individual system prices
   - ✅ Total price with/without discount
   - ✅ Terms and conditions checkbox
4. **Check** terms and conditions
5. **Click** "確認下單" button
6. **Verify**:
   - ✅ Order submitted successfully
   - ✅ Redirect to success page or dashboard
   - ✅ Order appears in orders list

#### Test Case 2.4: Order Cancellation
1. **During order flow**
2. **Click** "取消" or "Cancel" button
3. **Verify**:
   - ✅ Returns to previous page
   - ✅ No order created
   - ✅ Selected systems cleared

### Workflow 3: Dashboard & Reports

#### Test Case 3.1: Dashboard Statistics
1. **Navigate** to http://localhost:3000 or /dashboard
2. **Verify Dashboard Stats display**:
   - ✅ 命盤總數 (Total Profiles) with count
   - ✅ 報告總數 (Total Reports) with count
   - ✅ 處理中 (Pending) with count
   - ✅ 已完成 (Completed) with count
3. **Verify each stat card has**:
   - ✅ Icon (different for each type)
   - ✅ Correct color coding
   - ✅ Numeric value
   - ✅ Hover effect

#### Test Case 3.2: Recent Activity Timeline
1. **On dashboard page**
2. **Verify Recent Activity section shows**:
   - ✅ Latest activities in reverse chronological order
   - ✅ Activity titles in Traditional Chinese
   - ✅ Activity descriptions
   - ✅ Relative timestamps (e.g., "2小時前")
   - ✅ Status badges (completed, pending, failed)
   - ✅ Activity type icons
3. **Click** an activity item
4. **Verify**:
   - ✅ Navigates to relevant detail page (if implemented)

#### Test Case 3.3: View Reports List
1. **Navigate** to reports page
2. **Verify reports list displays**:
   - ✅ Profile name for each report
   - ✅ Expert system type
   - ✅ Status (pending/completed)
   - ✅ Creation date
   - ✅ Action buttons (view/download)

#### Test Case 3.4: Report Filtering
1. **On reports page**
2. **Use filter controls** to filter by:
   - Status (All/Pending/Completed)
   - Expert system type
   - Date range
3. **Verify**:
   - ✅ Filtered results update immediately
   - ✅ URL parameters updated
   - ✅ Filter selections persist on refresh

#### Test Case 3.5: View Completed Report
1. **Find a completed report**
2. **Click** "查看" or "View" button
3. **Verify report page displays**:
   - ✅ Profile information
   - ✅ Expert system sections
   - ✅ Analysis content
   - ✅ Traditional Chinese text
   - ✅ Proper formatting

### Workflow 4: Real-Time Job Progress

#### Test Case 4.1: Job Progress Display
1. **Create a new order** that triggers analysis
2. **Navigate** to job progress page or dashboard
3. **Verify JobProgress component shows**:
   - ✅ Job status (排隊中/分析中/已完成/失敗)
   - ✅ Progress percentage (0-100%)
   - ✅ Progress bar visual
   - ✅ Current step description (for running jobs)
   - ✅ Expert system name
   - ✅ Profile name

#### Test Case 4.2: Progress States
1. **Observe different job states**:

   **Queued State**:
   - ✅ Status: "排隊中"
   - ✅ Progress: 0%
   - ✅ No current step

   **Running State**:
   - ✅ Status: "分析中"
   - ✅ Progress: 1-99%
   - ✅ Current step displayed
   - ✅ Animated spinner icon
   - ✅ Estimated completion time

   **Completed State**:
   - ✅ Status: "已完成"
   - ✅ Progress: 100%
   - ✅ Checkmark icon
   - ✅ Completion time displayed

   **Failed State**:
   - ✅ Status: "失敗"
   - ✅ X icon
   - ✅ Error message displayed

#### Test Case 4.3: Auto-Refresh
1. **Watch a running job**
2. **Wait without refreshing page**
3. **Verify**:
   - ✅ Progress updates automatically
   - ✅ Current step changes
   - ✅ Percentage increases
   - ✅ No manual refresh needed

## UI Component Testing

### Test Case 5.1: Button Component
1. **Navigate through the app**
2. **Test different button variants**:
   - ✅ Primary buttons (solid background)
   - ✅ Secondary buttons (outlined)
   - ✅ Ghost buttons (transparent)
   - ✅ Danger buttons (red for delete actions)
3. **Test button sizes**:
   - ✅ Small (sm)
   - ✅ Medium (md) - default
   - ✅ Large (lg)
4. **Test button states**:
   - ✅ Hover effect
   - ✅ Disabled state (grayed out, no interaction)
   - ✅ Loading state (spinner icon)

### Test Case 5.2: Input Component
1. **Test text inputs**:
   - ✅ Label displays correctly
   - ✅ Placeholder text visible
   - ✅ Text entry works
   - ✅ Required field indicator (asterisk)
2. **Test validation states**:
   - ✅ Error state (red border, error message)
   - ✅ Success state (green border)
   - ✅ Focus state (highlighted border)
3. **Test disabled state**:
   - ✅ Grayed out appearance
   - ✅ Cannot enter text
   - ✅ No focus on click

### Test Case 5.3: Select Component
1. **Test dropdown select**:
   - ✅ Click opens dropdown
   - ✅ Options list displays
   - ✅ Select option updates value
   - ✅ Dropdown closes on selection
2. **Test search functionality** (if implemented):
   - ✅ Type to filter options
   - ✅ Filtered list updates
   - ✅ No results message

### Test Case 5.4: Modal Component
1. **Trigger modal** (e.g., delete confirmation)
2. **Verify modal behavior**:
   - ✅ Modal opens with backdrop
   - ✅ Background content darkened
   - ✅ Modal title displays
   - ✅ Modal content visible
   - ✅ Action buttons present
3. **Test closing**:
   - ✅ Click X button closes modal
   - ✅ Click backdrop closes modal
   - ✅ Press ESC key closes modal
   - ✅ Click cancel button closes modal

### Test Case 5.5: Card Component
1. **View profile cards or stat cards**
2. **Verify card displays**:
   - ✅ Rounded corners
   - ✅ Shadow effect
   - ✅ Proper padding
   - ✅ Content organized
3. **Test interactive cards**:
   - ✅ Hover effect (if clickable)
   - ✅ Click navigation (if applicable)

## Responsive Design Testing

### Test Case 6.1: Mobile View (375px width)
1. **Resize browser** to 375px width or use mobile device
2. **Verify**:
   - ✅ Navigation menu collapses to hamburger
   - ✅ Cards stack vertically
   - ✅ Form inputs full width
   - ✅ Text remains readable
   - ✅ No horizontal scroll
   - ✅ Touch targets adequate size (44x44px minimum)

### Test Case 6.2: Tablet View (768px width)
1. **Resize browser** to 768px width
2. **Verify**:
   - ✅ 2-column grid layouts
   - ✅ Navigation partially expanded
   - ✅ Proper spacing maintained
   - ✅ Touch-friendly interface

### Test Case 6.3: Desktop View (1024px+ width)
1. **Full desktop browser**
2. **Verify**:
   - ✅ 3-4 column grid layouts
   - ✅ Sidebar navigation visible
   - ✅ Optimal use of space
   - ✅ No excessive white space

## Error State Testing

### Test Case 7.1: Network Error
1. **Disable network** or block API requests
2. **Try to load data**
3. **Verify**:
   - ✅ Error message displays
   - ✅ Retry button available
   - ✅ No application crash
   - ✅ Traditional Chinese error text

### Test Case 7.2: Loading State
1. **Trigger data fetch** (e.g., load reports)
2. **Verify during loading**:
   - ✅ Loading spinner or skeleton
   - ✅ User cannot interact with loading content
   - ✅ Loading message displayed

### Test Case 7.3: Empty State
1. **Navigate to page with no data** (e.g., new user, no profiles)
2. **Verify**:
   - ✅ Empty state message in Traditional Chinese
   - ✅ Helpful illustration or icon
   - ✅ Call-to-action button (e.g., "建立第一個命盤")
   - ✅ Proper vertical centering

## Accessibility Testing

### Test Case 8.1: Keyboard Navigation
1. **Use only keyboard** (Tab, Enter, Escape, Arrow keys)
2. **Verify**:
   - ✅ Can tab through all interactive elements
   - ✅ Focus indicator visible on all elements
   - ✅ Enter key activates buttons
   - ✅ Escape closes modals
   - ✅ Arrow keys navigate menus (if applicable)
   - ✅ Skip to main content link available

### Test Case 8.2: Screen Reader (Optional)
1. **Enable screen reader** (VoiceOver on Mac, NVDA on Windows)
2. **Navigate through app**
3. **Verify**:
   - ✅ All content announced
   - ✅ Form labels read correctly
   - ✅ Button purposes clear
   - ✅ Landmark regions identified
   - ✅ Status changes announced

### Test Case 8.3: Color Contrast
1. **Check text readability**
2. **Verify**:
   - ✅ Text has sufficient contrast with background
   - ✅ Links distinguishable from text
   - ✅ Disabled states visually clear
   - ✅ Status colors distinguishable (not relying on color alone)

## Performance Testing

### Test Case 9.1: Page Load Time
1. **Open browser DevTools** (F12)
2. **Go to Network tab**
3. **Reload page**
4. **Verify**:
   - ✅ Initial load < 3 seconds on 3G
   - ✅ First Contentful Paint < 1.8s
   - ✅ Time to Interactive < 3.8s
   - ✅ Bundle size reasonable

### Test Case 9.2: Large Data Sets
1. **Create 50+ profiles**
2. **Load profiles page**
3. **Verify**:
   - ✅ Page remains responsive
   - ✅ No significant lag
   - ✅ Scrolling smooth
   - ✅ Pagination helps performance

## Browser Compatibility

### Test on Multiple Browsers:
- ✅ **Chrome** (latest version)
- ✅ **Firefox** (latest version)
- ✅ **Safari** (latest version)
- ✅ **Edge** (latest version)
- ✅ **Mobile Chrome** (Android)
- ✅ **Mobile Safari** (iOS)

### Verify in each browser:
- ✅ Layout renders correctly
- ✅ Interactions work as expected
- ✅ No console errors
- ✅ Fonts and styles correct

## Test Checklist Summary

### Critical Path (Must Pass)
- [ ] Create profile successfully
- [ ] Place order successfully
- [ ] View completed report
- [ ] Dashboard displays correctly
- [ ] No critical console errors

### Important Features
- [ ] Form validation works
- [ ] Real-time job progress updates
- [ ] Profile editing works
- [ ] Report filtering works
- [ ] Responsive design works

### Nice to Have
- [ ] Accessibility fully compliant
- [ ] Performance metrics met
- [ ] All browser compatibility
- [ ] Advanced animations work

## Reporting Issues

When you find an issue, document:
1. **Steps to reproduce**
2. **Expected behavior**
3. **Actual behavior**
4. **Browser and version**
5. **Screenshots** (if applicable)
6. **Console errors** (if any)

## Quick Start for Testing

```bash
# Start the app
cd /Users/frank/src/life/fortune_platform/frontend
npm run dev

# Open in browser
open http://localhost:3000

# Test critical path:
1. Create a profile → Should succeed
2. Order analysis → Should succeed
3. View dashboard → Should show stats
4. Check console → Should have no errors

# All working? ✅ Basic functionality confirmed
```

## Notes

- Most features require backend API to be running
- Some features may not be implemented yet
- Focus on critical user workflows first
- Test in production-like environment when available
- Use realistic test data (Traditional Chinese names and locations)
