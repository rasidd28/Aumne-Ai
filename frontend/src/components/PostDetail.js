import { useState } from 'react';
import toast from 'react-hot-toast';
import { submitPost, publishPost } from '../api';
import StatusBadge from './StatusBadge';

function formatDateTime(isoString) {
  if (!isoString) return '—';
  return new Date(isoString).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export default function PostDetail({ post, onClose, onUpdated }) {
  const [currentPost, setCurrentPost] = useState(post);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isPublishing, setIsPublishing] = useState(false);

  const handleSubmitForReview = async () => {
    setIsSubmitting(true);
    try {
      const result = await submitPost(currentPost.id);
      const updated = {
        ...currentPost,
        status: result.status,
        flagged_reasons: result.flagged_reasons,
      };
      setCurrentPost(updated);
      onUpdated?.(updated);

      if (result.status === 'approved') {
        toast.success('Post approved and ready for publishing');
      } else {
        toast.error('Post flagged during review. Revisions needed.');
      }
    } catch (err) {
      toast.error(err.message || 'Review request failed.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handlePublish = async () => {
    setIsPublishing(true);
    try {
      const result = await publishPost(currentPost.id);
      const updated = { ...currentPost, status: result.status };
      setCurrentPost(updated);
      onUpdated?.(updated);
      toast.success('Post published successfully');
    } catch (err) {
      toast.error(err.message || 'Publishing failed.');
    } finally {
      setIsPublishing(false);
    }
  };

  const reasons = currentPost.flagged_reasons
    ? currentPost.flagged_reasons.split(' | ')
    : [];

  return (
    <div
      className="modal-overlay"
      onClick={(e) => e.target === e.currentTarget && onClose()}
      role="presentation"
    >
      <div className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div className="modal-header">
          <h2 className="modal-title" id="modal-title">
            {currentPost.title}
          </h2>
          <button
            className="modal-close"
            onClick={onClose}
            aria-label="Close dialog"
          >
            ✕
          </button>
        </div>

        <div className="modal-meta-bar">
          <div>
            <div className="meta-label">Status</div>
            <StatusBadge status={currentPost.status} />
          </div>
          <div style={{ textAlign: 'right' }}>
            <div className="meta-label">Metadata</div>
            <span className="meta-id-date">
              #{currentPost.id} · {formatDateTime(currentPost.created_at)}
            </span>
          </div>
        </div>

        {currentPost.status === 'published' && (
          <div className="published-notice">
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
            <span>This post is published and read-only. Content cannot be edited.</span>
          </div>
        )}

        <div className="modal-body-section">
          <div className="meta-label">Content</div>
          <div className="modal-content-text">{currentPost.content}</div>
        </div>

        {currentPost.status === 'flagged' && reasons.length > 0 && (
          <div className="flag-alert">
            <div className="flag-alert-title">
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                <line x1="12" y1="9" x2="12" y2="13" />
                <line x1="12" y1="17" x2="12.01" y2="17" />
              </svg>
              <span>Moderation Feedback:</span>
            </div>
            {reasons.map((reason, index) => (
              <div key={index} className="flag-reason">
                {reason}
              </div>
            ))}
          </div>
        )}

        <div className="modal-actions">
          {currentPost.status === 'draft' && (
            <button
              id={`btn-submit-${currentPost.id}`}
              className="btn btn-primary"
              onClick={handleSubmitForReview}
              disabled={isSubmitting}
            >
              {isSubmitting ? <span className="spinner" /> : null}
              {isSubmitting ? 'Evaluating...' : 'Submit for Review'}
            </button>
          )}

          {currentPost.status === 'approved' && (
            <button
              id={`btn-publish-${currentPost.id}`}
              className="btn btn-accent"
              onClick={handlePublish}
              disabled={isPublishing}
            >
              {isPublishing ? <span className="spinner" /> : null}
              {isPublishing ? 'Publishing...' : 'Publish Post'}
            </button>
          )}

          <button className="btn btn-outline" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
