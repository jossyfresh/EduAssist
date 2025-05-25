-- Migration: Create courses table for SQLite
CREATE TABLE IF NOT EXISTS courses (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    sub_title TEXT,
    description TEXT,
    created_by TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- Add foreign key constraint for created_by
-- (Assumes users table exists and uses id as TEXT/UUID)
-- SQLite does not enforce foreign keys by default unless PRAGMA foreign_keys=ON
