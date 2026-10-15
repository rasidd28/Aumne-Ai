import StatusBadge from './StatusBadge';

function truncate(text, maxLength = 120) {
  if (!text) return '';
  return text.length > maxLength ? `${text.slice(0, maxLength).trim()}...` : text;
}

function formatDate(isoString) {
  if (!isoString) return '—';
  return new Date(isoString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

export default function PostCard({ post, onClick }) {
  const flaggedReasons = post.flagged_reasons ? post.flagged_reasons.split(' | ') : [];

  return (
    <article
      id={`post-card-${post.id}`}
      className={`post-card ${post.status}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick?.();
        }
      }}
      aria-label={`View post: ${post.title}`}
    >
      <div className="post-card-header">
        <h3 className="post-card-title">{post.title}</h3>
        <StatusBadge status={post.status} />
      </div>

      <p className="post-card-content">{truncate(post.content)}</p>

      <div className="post-card-footer">
        <span className="post-card-date">
          #{post.id} · {formatDate(post.created_at)}
        </span>
        <span className="post-card-stats">
          {post.content ? `${post.content.length} chars` : '0 chars'}
        </span>
      </div>

      {post.status === 'flagged' && flaggedReasons.length > 0 && (
        <div className="post-card-flag-preview">
          <span className="flag-dot" aria-hidden="true" />
          <span className="flag-preview-text">
            {flaggedReasons[0]}
            {flaggedReasons.length > 1 && ` (+${flaggedReasons.length - 1} more)`}
          </span>
        </div>
      )}
    </article>
  );
}
