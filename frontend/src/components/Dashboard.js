import { useState, useEffect } from 'react';
import { fetchPosts } from '../api';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
} from 'recharts';

const STATUS_COLORS = {
  draft: '#6b7280',
  approved: '#10b981',
  flagged: '#ef4444',
  published: '#7c3aed',
};

const RADIAN = Math.PI / 180;
const renderSliceLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, value }) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);
  return value > 0 ? (
    <text
      x={x}
      y={y}
      fill="#ffffff"
      textAnchor="middle"
      dominantBaseline="central"
      fontSize={12}
      fontWeight={600}
    >
      {value}
    </text>
  ) : null;
};

export default function Dashboard({ refreshTrigger }) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    fetchPosts()
      .then((data) => {
        if (isMounted) setPosts(data.posts || []);
      })
      .catch(() => {})
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [refreshTrigger]);

  const counts = posts.reduce(
    (acc, post) => {
      acc[post.status] = (acc[post.status] || 0) + 1;
      return acc;
    },
    { draft: 0, approved: 0, flagged: 0, published: 0 }
  );

  const pieData = Object.entries(counts).map(([name, value]) => ({ name, value }));

  const timelineMap = {};
  posts.forEach((post) => {
    const day = post.created_at ? post.created_at.slice(0, 10) : 'Unknown';
    if (!timelineMap[day]) {
      timelineMap[day] = { date: day, draft: 0, approved: 0, flagged: 0, published: 0 };
    }
    timelineMap[day][post.status] = (timelineMap[day][post.status] || 0) + 1;
  });

  const barData = Object.values(timelineMap)
    .sort((a, b) => a.date.localeCompare(b.date))
    .slice(-7);

  const approvalRate =
    posts.length > 0
      ? Math.round(((counts.approved + counts.published) / posts.length) * 100)
      : 0;

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner" style={{ width: 28, height: 28, margin: '0 auto 12px' }} />
        <span>Loading analytics...</span>
      </div>
    );
  }

  return (
    <div>
      <h1 className="section-title">Overview</h1>
      <p className="section-subtitle">
        Operational metrics and throughput across your editorial pipeline.
      </p>

      <div className="stats-grid">
        {[
          { label: 'Total Articles', value: posts.length, cls: '' },
          { label: 'Draft', value: counts.draft, cls: 'draft' },
          { label: 'Approved', value: counts.approved, cls: 'approved' },
          { label: 'Flagged', value: counts.flagged, cls: 'flagged' },
          { label: 'Published', value: counts.published, cls: 'published' },
          { label: 'Approval Rate', value: `${approvalRate}%`, cls: 'approved' },
        ].map((stat) => (
          <div key={stat.label} className={`stat-card ${stat.cls}`}>
            <div className="stat-label">{stat.label}</div>
            <div className="stat-value">{stat.value}</div>
          </div>
        ))}
      </div>

      {posts.length === 0 ? (
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
              <line x1="18" y1="20" x2="18" y2="10" />
              <line x1="12" y1="20" x2="12" y2="4" />
              <line x1="6" y1="20" x2="6" y2="14" />
            </svg>
          </div>
          <p className="empty-text">No data recorded yet. Create posts to populate analytics.</p>
        </div>
      ) : (
        <>
          <div className="chart-section">
            <div className="chart-title">Status Distribution</div>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  outerRadius={105}
                  labelLine={false}
                  label={renderSliceLabel}
                  dataKey="value"
                >
                  {pieData.map((entry) => (
                    <Cell key={entry.name} fill={STATUS_COLORS[entry.name] || '#6b7280'} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: 'var(--bg-elevated)',
                    border: '1px solid var(--border)',
                    borderRadius: 8,
                    color: 'var(--text-primary)',
                  }}
                  formatter={(val, name) => [`${val} articles`, name]}
                />
              </PieChart>
            </ResponsiveContainer>

            <div className="chart-legend-row">
              {pieData.map((entry) => (
                <span key={entry.name} className="chart-legend-item">
                  <span
                    className="legend-dot"
                    style={{ background: STATUS_COLORS[entry.name] }}
                  />
                  <span>
                    {entry.name} ({entry.value})
                  </span>
                </span>
              ))}
            </div>
          </div>

          {barData.length > 0 && (
            <div className="chart-section">
              <div className="chart-title">Publication Velocity (Last 7 Days)</div>
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={barData} margin={{ top: 8, right: 16, left: 0, bottom: 4 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" />
                  <XAxis dataKey="date" stroke="var(--text-muted)" tick={{ fontSize: 11 }} />
                  <YAxis stroke="var(--text-muted)" tick={{ fontSize: 11 }} allowDecimals={false} />
                  <Tooltip
                    contentStyle={{
                      background: 'var(--bg-elevated)',
                      border: '1px solid var(--border)',
                      borderRadius: 8,
                      color: 'var(--text-primary)',
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }} />
                  {Object.entries(STATUS_COLORS).map(([status, color]) => (
                    <Bar
                      key={status}
                      dataKey={status}
                      fill={color}
                      radius={[3, 3, 0, 0]}
                      maxBarSize={28}
                    />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </>
      )}
    </div>
  );
}
