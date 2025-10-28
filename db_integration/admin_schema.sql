-- Admin Configuration System Database Schema for Supabase
-- Run this after schema.sql to add admin configuration tables

-- Table: system_settings
-- Stores runtime configuration overrides
CREATE TABLE IF NOT EXISTS system_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category VARCHAR(50) NOT NULL,
    key VARCHAR(100) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    data_type VARCHAR(20),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_by VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: admin_users
-- Stores admin authentication information
CREATE TABLE IF NOT EXISTS admin_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'admin',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Table: config_audit_log
-- Tracks all configuration changes for accountability
CREATE TABLE IF NOT EXISTS config_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    setting_key VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    old_value JSONB,
    new_value JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    change_reason TEXT
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_system_settings_category ON system_settings(category);
CREATE INDEX IF NOT EXISTS idx_system_settings_key ON system_settings(key);
CREATE INDEX IF NOT EXISTS idx_audit_log_setting_key ON config_audit_log(setting_key);
CREATE INDEX IF NOT EXISTS idx_audit_log_changed_at ON config_audit_log(changed_at DESC);

-- Function: log_config_change
-- Automatically logs configuration changes
CREATE OR REPLACE FUNCTION log_config_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO config_audit_log (
        setting_key,
        category,
        old_value,
        new_value,
        changed_by
    ) VALUES (
        COALESCE(NEW.key, OLD.key),
        COALESCE(NEW.category, OLD.category),
        OLD.value,
        NEW.value,
        NEW.updated_by
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: log changes to system_settings
CREATE TRIGGER log_system_settings_changes
AFTER INSERT OR UPDATE ON system_settings
FOR EACH ROW
EXECUTE FUNCTION log_config_change();

-- Function: update_updated_at
-- Automatically updates updated_at timestamp
CREATE OR REPLACE FUNCTION update_admin_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: update system_settings.updated_at
CREATE TRIGGER update_system_settings_updated_at
BEFORE UPDATE ON system_settings
FOR EACH ROW
EXECUTE FUNCTION update_admin_updated_at();

-- View: current_settings_by_category
-- Shows all current settings grouped by category
CREATE OR REPLACE VIEW current_settings_by_category AS
SELECT 
    category,
    COUNT(*) as setting_count,
    MAX(updated_at) as last_updated
FROM system_settings
GROUP BY category
ORDER BY category;

-- View: recent_config_changes
-- Shows recent configuration changes
CREATE OR REPLACE VIEW recent_config_changes AS
SELECT 
    setting_key,
    category,
    changed_at,
    changed_by,
    old_value,
    new_value
FROM config_audit_log
ORDER BY changed_at DESC
LIMIT 50;

COMMENT ON TABLE system_settings IS 'Runtime configuration overrides that take precedence over config files';
COMMENT ON TABLE admin_users IS 'Administrative users with configuration access';
COMMENT ON TABLE config_audit_log IS 'Complete audit trail of all configuration changes';

