-- Migration: Add course_id to content and learning_paths tables
ALTER TABLE content ADD COLUMN course_id VARCHAR REFERENCES courses(id);
ALTER TABLE learning_paths ADD COLUMN course_id VARCHAR REFERENCES courses(id);
