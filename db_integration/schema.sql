-- GenAI Learning Resources and Trends Database Schema for Supabase

-- Table: learning_resources
-- Stores all discovered learning resources
CREATE TABLE IF NOT EXISTS learning_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    description TEXT,
    category TEXT CHECK (category IN ('tutorial', 'course', 'article', 'video', 'documentation')),
    source TEXT,
    relevance_score DECIMAL(3,2) CHECK (relevance_score >= 0 AND relevance_score <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: trending_topics
-- Stores trending topics from GitHub, LinkedIn, etc.
CREATE TABLE IF NOT EXISTS trending_topics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    source TEXT CHECK (source IN ('GitHub', 'LinkedIn', 'Twitter', 'Other')),
    topic_type TEXT,
    overall_score DECIMAL(5,2),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: it_skills
-- Categorizes and tracks IT skills mentioned in resources
CREATE TABLE IF NOT EXISTS it_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_name TEXT NOT NULL UNIQUE,
    category TEXT CHECK (category IN ('AI/ML', 'Programming', 'Cloud', 'Database', 'DevOps', 'Web Development', 'Mobile', 'Data Science', 'Other')),
    description TEXT,
    difficulty_level TEXT CHECK (difficulty_level IN ('Beginner', 'Intermediate', 'Advanced')),
    demand_score INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: resource_skills
-- Many-to-many relationship between resources and skills
CREATE TABLE IF NOT EXISTS resource_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_id UUID REFERENCES learning_resources(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES it_skills(id) ON DELETE CASCADE,
    relevance INTEGER CHECK (relevance >= 1 AND relevance <= 10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(resource_id, skill_id)
);

-- Table: skill_trends
-- Tracks skill popularity over time
CREATE TABLE IF NOT EXISTS skill_trends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id UUID REFERENCES it_skills(id) ON DELETE CASCADE,
    trend_date DATE NOT NULL,
    mention_count INTEGER DEFAULT 0,
    resource_count INTEGER DEFAULT 0,
    github_stars INTEGER DEFAULT 0,
    linkedin_posts INTEGER DEFAULT 0,
    trend_score DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(skill_id, trend_date)
);

-- Table: student_recommendations
-- Personalized skill recommendations for IT students
CREATE TABLE IF NOT EXISTS student_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_level TEXT CHECK (student_level IN ('Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate')),
    skill_id UUID REFERENCES it_skills(id) ON DELETE CASCADE,
    priority INTEGER CHECK (priority >= 1 AND priority <= 5),
    reason TEXT,
    learning_path JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_learning_resources_category ON learning_resources(category);
CREATE INDEX IF NOT EXISTS idx_learning_resources_created_at ON learning_resources(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_trending_topics_source ON trending_topics(source);
CREATE INDEX IF NOT EXISTS idx_trending_topics_score ON trending_topics(overall_score DESC);
CREATE INDEX IF NOT EXISTS idx_it_skills_category ON it_skills(category);
CREATE INDEX IF NOT EXISTS idx_it_skills_demand ON it_skills(demand_score DESC);
CREATE INDEX IF NOT EXISTS idx_skill_trends_date ON skill_trends(trend_date DESC);
CREATE INDEX IF NOT EXISTS idx_skill_trends_score ON skill_trends(trend_score DESC);

-- Create views for common queries

-- View: top_skills_for_students
-- Shows most in-demand skills for IT students
CREATE OR REPLACE VIEW top_skills_for_students AS
SELECT 
    s.skill_name,
    s.category,
    s.difficulty_level,
    s.demand_score,
    COUNT(DISTINCT rs.resource_id) as resource_count,
    AVG(lr.relevance_score) as avg_relevance,
    MAX(st.trend_score) as latest_trend_score
FROM it_skills s
LEFT JOIN resource_skills rs ON s.id = rs.skill_id
LEFT JOIN learning_resources lr ON rs.resource_id = lr.id
LEFT JOIN skill_trends st ON s.id = st.skill_id
GROUP BY s.id, s.skill_name, s.category, s.difficulty_level, s.demand_score
ORDER BY s.demand_score DESC, resource_count DESC;

-- View: skill_trend_summary
-- Summarizes skill trends over the last 30 days
CREATE OR REPLACE VIEW skill_trend_summary AS
SELECT 
    s.skill_name,
    s.category,
    COUNT(st.id) as data_points,
    AVG(st.trend_score) as avg_trend_score,
    SUM(st.mention_count) as total_mentions,
    SUM(st.resource_count) as total_resources,
    MAX(st.trend_date) as latest_date
FROM it_skills s
LEFT JOIN skill_trends st ON s.id = st.skill_id
WHERE st.trend_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY s.id, s.skill_name, s.category
ORDER BY avg_trend_score DESC;

-- View: recommended_learning_path
-- Shows recommended learning paths for students by level
CREATE OR REPLACE VIEW recommended_learning_path AS
SELECT 
    sr.student_level,
    s.skill_name,
    s.category,
    s.difficulty_level,
    sr.priority,
    sr.reason,
    COUNT(DISTINCT lr.id) as available_resources
FROM student_recommendations sr
JOIN it_skills s ON sr.skill_id = s.id
LEFT JOIN resource_skills rs ON s.id = rs.skill_id
LEFT JOIN learning_resources lr ON rs.resource_id = lr.id
GROUP BY sr.student_level, s.skill_name, s.category, s.difficulty_level, sr.priority, sr.reason
ORDER BY sr.student_level, sr.priority;

-- Function: update_skill_demand_score
-- Automatically updates demand score based on trends
CREATE OR REPLACE FUNCTION update_skill_demand_score()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE it_skills
    SET demand_score = (
        SELECT COALESCE(ROUND(AVG(trend_score)), 0)
        FROM skill_trends
        WHERE skill_id = NEW.skill_id
        AND trend_date >= CURRENT_DATE - INTERVAL '7 days'
    )
    WHERE id = NEW.skill_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: update_demand_on_trend_insert
CREATE TRIGGER update_demand_on_trend_insert
AFTER INSERT ON skill_trends
FOR EACH ROW
EXECUTE FUNCTION update_skill_demand_score();

-- Function: update_updated_at
-- Automatically updates updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update_updated_at trigger to relevant tables
CREATE TRIGGER update_learning_resources_updated_at
BEFORE UPDATE ON learning_resources
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_trending_topics_updated_at
BEFORE UPDATE ON trending_topics
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_it_skills_updated_at
BEFORE UPDATE ON it_skills
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_student_recommendations_updated_at
BEFORE UPDATE ON student_recommendations
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Insert initial IT skills relevant for students
INSERT INTO it_skills (skill_name, category, difficulty_level, demand_score, description) VALUES
-- AI/ML Skills
('Generative AI', 'AI/ML', 'Intermediate', 95, 'Building applications with LLMs and generative models'),
('LangChain', 'AI/ML', 'Intermediate', 90, 'Framework for developing LLM-powered applications'),
('Prompt Engineering', 'AI/ML', 'Beginner', 85, 'Crafting effective prompts for AI models'),
('RAG', 'AI/ML', 'Advanced', 88, 'Retrieval Augmented Generation for enhanced AI responses'),
('Fine-tuning', 'AI/ML', 'Advanced', 82, 'Customizing AI models for specific tasks'),
('Vector Databases', 'AI/ML', 'Intermediate', 80, 'Database systems for AI embeddings and semantic search'),

-- Programming Skills
('Python', 'Programming', 'Beginner', 95, 'Essential programming language for AI and data science'),
('JavaScript', 'Programming', 'Beginner', 90, 'Core language for web development'),
('TypeScript', 'Programming', 'Intermediate', 85, 'Typed superset of JavaScript'),
('APIs', 'Programming', 'Intermediate', 88, 'Building and consuming web APIs'),

-- Cloud Skills
('AWS', 'Cloud', 'Intermediate', 85, 'Amazon Web Services cloud platform'),
('Azure', 'Cloud', 'Intermediate', 82, 'Microsoft Azure cloud services'),
('Docker', 'Cloud', 'Intermediate', 90, 'Containerization platform'),
('Kubernetes', 'Cloud', 'Advanced', 78, 'Container orchestration system'),

-- Web Development
('React', 'Web Development', 'Intermediate', 88, 'Popular JavaScript library for UIs'),
('Node.js', 'Web Development', 'Intermediate', 85, 'JavaScript runtime for backend'),
('REST APIs', 'Web Development', 'Intermediate', 90, 'RESTful API design and implementation'),

-- Data Science
('Data Analysis', 'Data Science', 'Beginner', 85, 'Analyzing and interpreting data'),
('Machine Learning', 'Data Science', 'Intermediate', 92, 'Building predictive models'),
('SQL', 'Database', 'Beginner', 90, 'Database query language'),

-- DevOps
('Git', 'DevOps', 'Beginner', 95, 'Version control system'),
('CI/CD', 'DevOps', 'Intermediate', 82, 'Continuous Integration and Deployment')
ON CONFLICT (skill_name) DO NOTHING;

COMMENT ON TABLE learning_resources IS 'Stores GenAI learning resources discovered by agents';
COMMENT ON TABLE trending_topics IS 'Tracks trending topics from various platforms';
COMMENT ON TABLE it_skills IS 'Master list of IT skills relevant for students';
COMMENT ON TABLE resource_skills IS 'Links resources to the skills they teach';
COMMENT ON TABLE skill_trends IS 'Time-series data of skill popularity';
COMMENT ON TABLE student_recommendations IS 'Curated skill recommendations by student level';

