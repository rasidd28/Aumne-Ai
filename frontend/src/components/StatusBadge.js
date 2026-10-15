const STATUS_CONFIG = {
  draft: { label: 'Draft', cls: 'badge-draft' },
  approved: { label: 'Approved', cls: 'badge-approved' },
  flagged: { label: 'Flagged', cls: 'badge-flagged' },
  published: { label: 'Published', cls: 'badge-published' },
};

export default function StatusBadge({ status }) {
  const config = STATUS_CONFIG[status] || { label: status || 'Unknown', cls: 'badge-draft' };

  return (
    <span className={`badge ${config.cls}`}>
      <span className="badge-dot" aria-hidden="true" />
      <span>{config.label}</span>
    </span>
  );
}
