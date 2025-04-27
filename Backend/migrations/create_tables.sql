-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE content_type AS ENUM ('text', 'video', 'quiz', 'exercise');
CREATE TYPE progress_status AS ENUM ('not_started', 'in_progress', 'completed');

-- Create learning_paths table
CREATE TABLE IF NOT EXISTS public.learning_paths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    difficulty_level TEXT,
    estimated_duration INTEGER,
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    created_by UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create learning_path_steps table
CREATE TABLE IF NOT EXISTS public.learning_path_steps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    learning_path_id UUID REFERENCES public.learning_paths(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    step_order INTEGER NOT NULL,
    content_type content_type NOT NULL,
    content_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create content_items table
CREATE TABLE IF NOT EXISTS public.content_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_type content_type NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::JSONB,
    created_by UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create user_progress table
CREATE TABLE IF NOT EXISTS public.user_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    learning_path_id UUID REFERENCES public.learning_paths(id) ON DELETE CASCADE,
    step_id UUID REFERENCES public.learning_path_steps(id) ON DELETE CASCADE,
    status progress_status DEFAULT 'not_started',
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_learning_paths_created_by ON public.learning_paths(created_by);
CREATE INDEX IF NOT EXISTS idx_learning_path_steps_learning_path_id ON public.learning_path_steps(learning_path_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON public.user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_learning_path_id ON public.user_progress(learning_path_id);

-- Create trigger function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for all tables
CREATE TRIGGER update_learning_paths_updated_at
    BEFORE UPDATE ON public.learning_paths
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_learning_path_steps_updated_at
    BEFORE UPDATE ON public.learning_path_steps
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_content_items_updated_at
    BEFORE UPDATE ON public.content_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_progress_updated_at
    BEFORE UPDATE ON public.user_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Set up RLS (Row Level Security) policies
ALTER TABLE public.learning_paths ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.learning_path_steps ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.content_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_progress ENABLE ROW LEVEL SECURITY;

-- Learning paths policies
CREATE POLICY "Public learning paths are viewable by everyone"
    ON public.learning_paths FOR SELECT
    USING (is_public = true);

CREATE POLICY "Users can view their own learning paths"
    ON public.learning_paths FOR SELECT
    USING (auth.uid() = created_by);

CREATE POLICY "Users can create their own learning paths"
    ON public.learning_paths FOR INSERT
    WITH CHECK (auth.uid() = created_by);

CREATE POLICY "Users can update their own learning paths"
    ON public.learning_paths FOR UPDATE
    USING (auth.uid() = created_by);

CREATE POLICY "Users can delete their own learning paths"
    ON public.learning_paths FOR DELETE
    USING (auth.uid() = created_by);

-- Learning path steps policies
CREATE POLICY "Users can view steps of public learning paths"
    ON public.learning_path_steps FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.learning_paths
        WHERE id = learning_path_id AND is_public = true
    ));

CREATE POLICY "Users can view steps of their own learning paths"
    ON public.learning_path_steps FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.learning_paths
        WHERE id = learning_path_id AND created_by = auth.uid()
    ));

CREATE POLICY "Users can modify steps of their own learning paths"
    ON public.learning_path_steps FOR ALL
    USING (EXISTS (
        SELECT 1 FROM public.learning_paths
        WHERE id = learning_path_id AND created_by = auth.uid()
    ));

-- Content items policies
CREATE POLICY "Users can view all content items"
    ON public.content_items FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Users can create their own content items"
    ON public.content_items FOR INSERT
    WITH CHECK (auth.uid() = created_by);

CREATE POLICY "Users can update their own content items"
    ON public.content_items FOR UPDATE
    USING (auth.uid() = created_by);

CREATE POLICY "Users can delete their own content items"
    ON public.content_items FOR DELETE
    USING (auth.uid() = created_by);

-- User progress policies
CREATE POLICY "Users can view their own progress"
    ON public.user_progress FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own progress"
    ON public.user_progress FOR ALL
    USING (auth.uid() = user_id); 