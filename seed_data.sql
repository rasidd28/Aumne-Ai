-- Sample data for local development

INSERT INTO posts (title, content, status, flagged_reasons, created_at) VALUES
(
    'Reflections on Modern Software Architecture',
    'Modern software architecture is fundamentally about managing complexity and change. While microservices offer organizational boundaries, modular monoliths often provide the sweet spot for early-stage products. Striking the right balance depends on domain cohesion, team topology, and communication latency across services.',
    'approved',
    NULL,
    '2026-10-10 08:00:00'
);

INSERT INTO posts (title, content, status, flagged_reasons, created_at) VALUES
(
    'Designing Predictable REST APIs with FastAPI',
    'FastAPI pairs standard Python type hints with Pydantic schemas, enabling concise endpoints with automatic validation and interactive OpenAPI documentation. By adopting explicit request models and disciplined status codes, engineering teams can build reliable APIs that integrate smoothly with frontend clients.',
    'published',
    NULL,
    '2026-10-11 09:30:00'
);

INSERT INTO posts (title, content, status, flagged_reasons, created_at) VALUES
(
    'Pragmatic Notes on Team Code Reviews',
    'Code reviews are as much about shared context and team empathy as they are about catching bugs. Small, incremental pull requests reduce review fatigue, improve comprehension, and allow faster iteration cycles without compromising code quality.',
    'draft',
    NULL,
    '2026-10-12 10:15:00'
);

INSERT INTO posts (title, content, status, flagged_reasons, created_at) VALUES
(
    'Brief update',
    'Just testing out the draft composer quickly.',
    'flagged',
    'Content is too short. Minimum required length: 50 characters.',
    '2026-10-13 11:00:00'
);

INSERT INTO posts (title, content, status, flagged_reasons, created_at) VALUES
(
    'Unmoderated Community Rant',
    'I hate this product and consider it completely worthless garbage designed by idiots who have no idea how software should work.',
    'flagged',
    'Banned word(s) detected: worthless, garbage. Please remove inappropriate language.',
    '2026-10-13 12:00:00'
);

INSERT INTO posts (title, content, status, flagged_reasons, created_at) VALUES
(
    'ALL-CAPS NOTICE',
    'THIS IS AN IMPORTANT SYSTEM NOTIFICATION THAT REQUIRES YOUR IMMEDIATE ATTENTION WITHOUT DELAY PLEASE READ CAREFULLY.',
    'flagged',
    'Content sounds aggressive (all-caps, 95% uppercase). Please write in normal sentence case.',
    '2026-10-14 13:00:00'
);
