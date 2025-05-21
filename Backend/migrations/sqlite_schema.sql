-- Create content_type enum table
CREATE TABLE IF NOT EXISTS content_type (
    value TEXT PRIMARY KEY
);
INSERT INTO content_type (value) VALUES ('text'), ('video'), ('quiz'), ('exercise');

-- Create progress_status enum table
CREATE TABLE IF NOT EXISTS progress_status (
    value TEXT PRIMARY KEY
);
INSERT INTO progress_status (value) VALUES ('not_started'), ('in_progress'), ('completed');

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT,
    is_active BOOLEAN DEFAULT 1,
    is_superuser BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create learning_paths table
CREATE TABLE IF NOT EXISTS learning_paths (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT 0,
    difficulty_level TEXT,
    estimated_duration INTEGER,
    tags TEXT DEFAULT '[]',
    created_by TEXT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create learning_path_steps table
CREATE TABLE IF NOT EXISTS learning_path_steps (
    id TEXT PRIMARY KEY,
    learning_path_id TEXT REFERENCES learning_paths(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    step_order INTEGER NOT NULL,
    content_type TEXT REFERENCES content_type(value),
    content_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create content table
CREATE TABLE IF NOT EXISTS content (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content_type TEXT REFERENCES content_type(value),
    content TEXT NOT NULL,
    meta TEXT DEFAULT '{}',
    created_by TEXT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create user_progress table
CREATE TABLE IF NOT EXISTS user_progress (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    learning_path_id TEXT REFERENCES learning_paths(id) ON DELETE CASCADE,
    step_id TEXT REFERENCES learning_path_steps(id) ON DELETE CASCADE,
    status TEXT REFERENCES progress_status(value) DEFAULT 'not_started',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_learning_paths_created_by ON learning_paths(created_by);
CREATE INDEX IF NOT EXISTS idx_learning_path_steps_learning_path_id ON learning_path_steps(learning_path_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_learning_path_id ON user_progress(learning_path_id);
CREATE INDEX IF NOT EXISTS idx_content_created_by ON content(created_by); 