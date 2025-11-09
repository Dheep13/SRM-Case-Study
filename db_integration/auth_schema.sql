-- Authentication Schema for User Login
-- Run this after schema.sql to add user authentication tables

-- Table: users
-- Stores user credentials for authentication
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(200),
    student_level VARCHAR(50) CHECK (student_level IN ('Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: user_sessions
-- Stores active user sessions
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_expires ON user_sessions(expires_at);

-- Note: Password hashing is handled in the backend (api.py)
-- In production, use bcrypt or similar for password hashing

-- Function: cleanup_expired_sessions
-- Remove expired sessions
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM user_sessions WHERE expires_at < NOW();
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Trigger: update_updated_at (if function exists)
-- Note: This function should be defined in schema.sql
-- If it doesn't exist, the trigger will be skipped
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'update_updated_at_column') THEN
        CREATE TRIGGER update_users_updated_at
        BEFORE UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    END IF;
END $$;

-- Insert default test user (password: 'password123')
-- In production, remove this and create users through registration
INSERT INTO users (username, password_hash, email, full_name, student_level) VALUES
('admin', 'password123', 'admin@evolveiq.com', 'Admin User', 'Graduate'),
('student', 'password123', 'student@evolveiq.com', 'Test Student', 'Junior')
ON CONFLICT (username) DO NOTHING;

COMMENT ON TABLE users IS 'User accounts for authentication';
COMMENT ON TABLE user_sessions IS 'Active user sessions with tokens';
COMMENT ON FUNCTION cleanup_expired_sessions IS 'Remove expired sessions periodically';

