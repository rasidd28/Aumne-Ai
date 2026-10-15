export default function Navbar({ activeView, onChangeView }) {
  const links = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'posts', label: 'Posts' },
    { id: 'create', label: 'New Post' },
  ];

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <div className="navbar-brand" onClick={() => onChangeView('dashboard')} role="button" tabIndex={0}>
          <div className="navbar-logo">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" y1="13" x2="8" y2="13" />
              <line x1="16" y1="17" x2="8" y2="17" />
              <polyline points="10 9 9 9 8 9" />
            </svg>
          </div>
          <span className="navbar-title">ContentMod</span>
        </div>

        <div className="navbar-nav">
          {links.map((link) => (
            <button
              key={link.id}
              id={`nav-${link.id}`}
              className={`nav-btn ${activeView === link.id ? 'active' : ''}`}
              onClick={() => onChangeView(link.id)}
            >
              {link.label}
            </button>
          ))}
        </div>

        <div className="navbar-status" title="Real-time synchronization active">
          <span className="live-dot" />
          <span className="live-label">Synced</span>
        </div>
      </div>
    </nav>
  );
}
