import { useState } from 'react';
import toast from 'react-hot-toast';
import { createPost, submitPost } from '../api';

const MIN_LENGTH = 50;
const MAX_LENGTH = 2000;
const MAX_TITLE_LENGTH = 200;

export default function CreatePostForm({ onCreated }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSavingDraft, setIsSavingDraft] = useState(false);

  const contentLength = content.length;
  const isTooShort = contentLength > 0 && contentLength < MIN_LENGTH;
  const isTooLong = contentLength > MAX_LENGTH;

  const validate = () => {
    if (!title.trim()) {
      toast.error('Please enter a post title.');
      return false;
    }
    if (!content.trim()) {
      toast.error('Post content cannot be empty.');
      return false;
    }
    return true;
  };

  const handleSaveDraft = async () => {
    if (!validate()) return;

    setIsSavingDraft(true);
    try {
      const post = await createPost(title.trim(), content.trim());
      toast.success(`Draft saved (Post #${post.id})`);
      setTitle('');
      setContent('');
      onCreated?.(post);
    } catch (err) {
      toast.error(err.message || 'Failed to save draft.');
    } finally {
      setIsSavingDraft(false);
    }
  };

  const handleSaveAndSubmit = async () => {
    if (!validate()) return;

    setIsSubmitting(true);
    try {
      const post = await createPost(title.trim(), content.trim());
      const review = await submitPost(post.id);
      const updatedPost = {
        ...post,
        status: review.status,
        flagged_reasons: review.flagged_reasons,
      };

      if (review.status === 'approved') {
        toast.success(`Post #${post.id} submitted and approved`);
      } else {
        toast.error(`Post #${post.id} flagged for revisions`);
      }

      setTitle('');
      setContent('');
      onCreated?.(updatedPost);
    } catch (err) {
      toast.error(err.message || 'Submission failed.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const isBusy = isSubmitting || isSavingDraft;

  return (
    <div>
      <h1 className="section-title">New Post</h1>
      <p className="section-subtitle">
        Draft an article and send it through automated moderation checks before publishing.
      </p>

      <div className="card" style={{ maxWidth: 760 }}>
        <div className="form-group">
          <label className="form-label" htmlFor="post-title">
            Title
          </label>
          <input
            id="post-title"
            className="form-input"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter article title..."
            maxLength={MAX_TITLE_LENGTH}
            disabled={isBusy}
          />
          <div className="char-count">
            {title.length} / {MAX_TITLE_LENGTH}
          </div>
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="post-content">
            Article Content
          </label>
          <textarea
            id="post-content"
            className="form-textarea"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write your article content here (50 - 2,000 characters)..."
            rows={9}
            disabled={isBusy}
          />
          <div
            className={`char-count ${
              isTooLong ? 'error' : isTooShort ? 'warn' : ''
            }`}
          >
            {isTooShort
              ? `${MIN_LENGTH - contentLength} more character${
                  MIN_LENGTH - contentLength !== 1 ? 's' : ''
                } needed · `
              : ''}
            {contentLength} / {MAX_LENGTH}
          </div>
        </div>

        <div className="guidelines-card">
          <div className="guidelines-title">
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
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="16" x2="12" y2="12" />
              <line x1="12" y1="8" x2="12.01" y2="8" />
            </svg>
            <span>Content Quality Rules</span>
          </div>
          <p className="guidelines-text">
            Posts are reviewed against quality standards: length between 50 and 2,000 characters,
            natural sentence casing, respectful language, and no repetitive text.
          </p>
        </div>

        <div className="form-actions">
          <button
            id="btn-save-and-submit"
            type="button"
            className="btn btn-primary"
            onClick={handleSaveAndSubmit}
            disabled={isBusy}
          >
            {isSubmitting ? <span className="spinner" /> : null}
            {isSubmitting ? 'Submitting...' : 'Submit for Review'}
          </button>

          <button
            id="btn-create-post"
            type="button"
            className="btn btn-outline"
            onClick={handleSaveDraft}
            disabled={isBusy}
          >
            {isSavingDraft ? <span className="spinner" /> : null}
            {isSavingDraft ? 'Saving...' : 'Save Draft'}
          </button>
        </div>
      </div>
    </div>
  );
}
