import { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import PostList from './components/PostList';
import CreatePostForm from './components/CreatePostForm';

export default function App() {
  const [view, setView] = useState('dashboard');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handlePostCreated = () => {
    setRefreshTrigger((prev) => prev + 1);
    setView('posts');
  };

  return (
    <div className="app-wrapper">
      <Navbar activeView={view} onChangeView={setView} />

      <main className="main-content">
        {view === 'dashboard' && <Dashboard refreshTrigger={refreshTrigger} />}
        {view === 'posts' && <PostList refreshTrigger={refreshTrigger} />}
        {view === 'create' && <CreatePostForm onCreated={handlePostCreated} />}
      </main>

      <Toaster
        position="bottom-right"
        toastOptions={{
          style: {
            background: 'var(--bg-elevated)',
            color: 'var(--text-primary)',
            border: '1px solid var(--border)',
            borderRadius: 8,
            fontFamily: 'Inter, sans-serif',
            fontSize: '0.875rem',
            boxShadow: '0 10px 25px rgba(0, 0, 0, 0.3)',
          },
          success: {
            iconTheme: { primary: '#10b981', secondary: '#ffffff' },
          },
          error: {
            iconTheme: { primary: '#ef4444', secondary: '#ffffff' },
          },
        }}
      />
    </div>
  );
}
