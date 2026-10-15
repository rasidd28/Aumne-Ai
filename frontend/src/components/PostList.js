import { useState, useEffect, useCallback } from 'react';
import { fetchPosts } from '../api';
import PostCard from './PostCard';
import PostDetail from './PostDetail';

const FILTERS = [
  { label: 'All', value: null },
  { label: 'Draft', value: 'draft' },
  { label: 'Approved', value: 'approved' },
  { label: 'Flagged', value: 'flagged' },
  { label: 'Published', value: 'published' },
];

export default function PostList({ refreshTrigger }) {
  const [posts, setPosts] = useState([]);
  const [total, setTotal] = useState(0);
  const [filter, setFilter] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedPost, setSelectedPost] = useState(null);
  const [error, setError] = useState(null);

  const loadPosts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchPosts(filter);
      setPosts(data.posts || []);
      setTotal(data.total || 0);
    } catch (err) {
      setError(err.message || 'Unable to fetch posts.');
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => {
    loadPosts();
  }, [loadPosts, refreshTrigger]);

  useEffect(() => {
    const interval = setInterval(loadPosts, 15000);
    return () => clearInterval(interval);
  }, [loadPosts]);

  const handleUpdated = (updatedPost) => {
    setPosts((prev) =>
      prev.map((item) => (item.id === updatedPost.id ? updatedPost : item))
    );
    setSelectedPost(updatedPost);
  };

  return (
    <div>
      <div className="posts-header">
        <div>
          <h1 className="section-title">Articles</h1>
          <p className="section-subtitle">
            {total} article{total !== 1 ? 's' : ''} in pipeline · Synchronized every 15s
          </p>
        </div>

        <button
          id="btn-refresh-posts"
          className="btn btn-outline btn-sm"
          onClick={loadPosts}
          disabled={loading}
        >
          {loading ? (
            <span className="spinner" style={{ width: 14, height: 14 }} />
          ) : (
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
              <polyline points="23 4 23 10 17 10" />
              <polyline points="1 20 1 14 7 14" />
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
            </svg>
          )}
          <span>Refresh</span>
        </button>
      </div>

      <div className="filter-bar">
        {FILTERS.map((item) => (
          <button
            key={String(item.value)}
            id={`filter-${item.value ?? 'all'}`}
            className={`filter-chip ${filter === item.value ? 'active' : ''}`}
            onClick={() => setFilter(item.value)}
          >
            {item.label}
          </button>
        ))}
      </div>

      {error && (
        <div className="error-banner">
          <span>{error}</span>
        </div>
      )}

      {loading && posts.length === 0 && (
        <div className="posts-grid">
          {[1, 2, 3].map((placeholder) => (
            <div key={placeholder} className="card card-skeleton">
              <div className="skeleton-line skeleton-title" />
              <div className="skeleton-line skeleton-body" />
              <div className="skeleton-line skeleton-body-short" />
            </div>
          ))}
        </div>
      )}

      {!loading && posts.length === 0 && !error && (
        <div className="empty-state">
          <div className="empty-icon-wrap">
            <svg
              width="36"
              height="36"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <polyline points="22 12 16 12 14 15 10 15 8 12 2 12" />
              <path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" />
            </svg>
          </div>
          <p className="empty-text">
            No posts found {filter ? `matching filter "${filter}"` : 'in the database'}.
          </p>
        </div>
      )}

      {posts.length > 0 && (
        <div className="posts-grid">
          {posts.map((post) => (
            <PostCard
              key={post.id}
              post={post}
              onClick={() => setSelectedPost(post)}
            />
          ))}
        </div>
      )}

      {selectedPost && (
        <PostDetail
          post={selectedPost}
          onClose={() => setSelectedPost(null)}
          onUpdated={handleUpdated}
        />
      )}
    </div>
  );
}
