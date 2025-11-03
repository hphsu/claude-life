/**
 * SafeHTML Component
 *
 * SECURITY NOTE: This component uses dangerouslySetInnerHTML, which is safe in this context because:
 * 1. All HTML content is pre-sanitized at the API layer using DOMPurify
 * 2. The reportsApi.getContent() method calls sanitizeHTML() before returning content
 * 3. sanitizeHTML() strips all potentially dangerous elements (scripts, iframes, event handlers)
 * 4. Only semantic HTML tags are allowed (p, h1-h6, strong, em, tables, etc.)
 *
 * This component is a simple wrapper that renders already-sanitized HTML content.
 */

interface SafeHTMLProps {
  html: string;
  className?: string;
}

export function SafeHTML({ html, className = '' }: SafeHTMLProps) {
  return (
    <div
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
