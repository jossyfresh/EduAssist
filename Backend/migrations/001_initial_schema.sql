-- Create learning_paths table
CREATE TABLE learning_paths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_by UUID NOT NULL REFERENCES auth.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_public BOOLEAN DEFAULT false,
    difficulty_level VARCHAR(50),
    estimated_duration INTEGER, -- in minutes
    tags TEXT[] DEFAULT '{}'
);

-- Create learning_path_steps table
CREATE TABLE learning_path_steps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    learning_path_id UUID NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    step_order INTEGER NOT NULL,
    content_type VARCHAR(50) NOT NULL, -- 'text', 'video', 'quiz', etc.
    content_id UUID, -- References specific content based on content_type
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create content_items table
CREATE TABLE content_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    metadata JSONB DEFAULT '{}',
    created_by UUID NOT NULL REFERENCES auth.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user_progress table
CREATE TABLE user_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    learning_path_id UUID NOT NULL REFERENCES learning_paths(id),
    step_id UUID NOT NULL REFERENCES learning_path_steps(id),
    status VARCHAR(50) NOT NULL, -- 'not_started', 'in_progress', 'completed'
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, step_id)
);

-- Create indexes for better performance
CREATE INDEX idx_learning_paths_created_by ON learning_paths(created_by);
CREATE INDEX idx_learning_path_steps_path_id ON learning_path_steps(learning_path_id);
CREATE INDEX idx_content_items_created_by ON content_items(created_by);
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_progress_path_id ON user_progress(learning_path_id);

-- Enable Row Level Security
ALTER TABLE learning_paths ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_path_steps ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view public learning paths"
    ON learning_paths FOR SELECT
    USING (is_public = true);

CREATE POLICY "Users can view their own learning paths"
    ON learning_paths FOR SELECT
    USING (auth.uid() = created_by);

CREATE POLICY "Users can create learning paths"
    ON learning_paths FOR INSERT
    WITH CHECK (auth.uid() = created_by);

CREATE POLICY "Users can update their own learning paths"
    ON learning_paths FOR UPDATE
    USING (auth.uid() = created_by);

CREATE POLICY "Users can delete their own learning paths"
    ON learning_paths FOR DELETE
    USING (auth.uid() = created_by);

-- Similar policies for other tables... 