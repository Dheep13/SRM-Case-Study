-- Vector Embeddings Extension for Chatbot Functionality
-- This enables semantic search and natural language queries

-- Enable pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Table: resource_embeddings
-- Stores vector embeddings of learning resources for semantic search
CREATE TABLE IF NOT EXISTS resource_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_id UUID REFERENCES learning_resources(id) ON DELETE CASCADE,
    embedding vector(1536), -- OpenAI ada-002 embedding dimension
    content_text TEXT, -- The text that was embedded
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(resource_id)
);

-- Table: skill_embeddings
-- Stores vector embeddings of skills for semantic matching
CREATE TABLE IF NOT EXISTS skill_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id UUID REFERENCES it_skills(id) ON DELETE CASCADE,
    embedding vector(1536),
    description_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(skill_id)
);

-- Table: chat_history
-- Stores conversation history for the chatbot
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    context_used JSONB, -- What data was used to generate response
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for vector similarity search (using cosine distance)
CREATE INDEX IF NOT EXISTS idx_resource_embeddings_vector 
ON resource_embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_skill_embeddings_vector 
ON skill_embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Index for chat history
CREATE INDEX IF NOT EXISTS idx_chat_history_session ON chat_history(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created ON chat_history(created_at DESC);

-- Function: search_similar_resources
-- Find resources similar to a query embedding
CREATE OR REPLACE FUNCTION search_similar_resources(
    query_embedding vector(1536),
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 5
)
RETURNS TABLE (
    resource_id UUID,
    title TEXT,
    url TEXT,
    description TEXT,
    category TEXT,
    similarity float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        lr.id,
        lr.title,
        lr.url,
        lr.description,
        lr.category,
        1 - (re.embedding <=> query_embedding) as similarity
    FROM resource_embeddings re
    JOIN learning_resources lr ON re.resource_id = lr.id
    WHERE 1 - (re.embedding <=> query_embedding) > match_threshold
    ORDER BY re.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- Function: search_similar_skills
-- Find skills similar to a query embedding
CREATE OR REPLACE FUNCTION search_similar_skills(
    query_embedding vector(1536),
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 10
)
RETURNS TABLE (
    skill_id UUID,
    skill_name TEXT,
    category TEXT,
    difficulty_level TEXT,
    demand_score INT,
    similarity float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id,
        s.skill_name,
        s.category,
        s.difficulty_level,
        s.demand_score,
        1 - (se.embedding <=> query_embedding) as similarity
    FROM skill_embeddings se
    JOIN it_skills s ON se.skill_id = s.id
    WHERE 1 - (se.embedding <=> query_embedding) > match_threshold
    ORDER BY se.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- Function: get_skill_with_resources
-- Get a skill and its related learning resources
CREATE OR REPLACE FUNCTION get_skill_with_resources(skill_name_param TEXT)
RETURNS TABLE (
    skill_name TEXT,
    category TEXT,
    demand_score INT,
    resource_title TEXT,
    resource_url TEXT,
    resource_category TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.skill_name,
        s.category,
        s.demand_score,
        lr.title,
        lr.url,
        lr.category
    FROM it_skills s
    LEFT JOIN resource_skills rs ON s.id = rs.skill_id
    LEFT JOIN learning_resources lr ON rs.resource_id = lr.id
    WHERE s.skill_name ILIKE '%' || skill_name_param || '%'
    ORDER BY s.demand_score DESC, lr.relevance_score DESC;
END;
$$ LANGUAGE plpgsql;

-- Function: get_recommended_skills_for_query
-- Get skill recommendations based on natural language query
CREATE OR REPLACE FUNCTION get_recommended_skills_for_query(
    student_level_param TEXT,
    focus_area_param TEXT DEFAULT NULL
)
RETURNS TABLE (
    skill_name TEXT,
    category TEXT,
    difficulty_level TEXT,
    demand_score INT,
    resource_count BIGINT,
    avg_relevance NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.skill_name,
        s.category,
        s.difficulty_level,
        s.demand_score,
        COUNT(DISTINCT rs.resource_id) as resource_count,
        ROUND(AVG(lr.relevance_score)::numeric, 2) as avg_relevance
    FROM it_skills s
    LEFT JOIN resource_skills rs ON s.id = rs.skill_id
    LEFT JOIN learning_resources lr ON rs.resource_id = lr.id
    WHERE 
        (focus_area_param IS NULL OR s.category = focus_area_param)
        AND (
            (student_level_param IN ('Freshman', 'Sophomore') AND s.difficulty_level = 'Beginner')
            OR (student_level_param = 'Junior' AND s.difficulty_level IN ('Beginner', 'Intermediate'))
            OR (student_level_param IN ('Senior', 'Graduate') AND s.difficulty_level IN ('Intermediate', 'Advanced'))
        )
    GROUP BY s.id, s.skill_name, s.category, s.difficulty_level, s.demand_score
    ORDER BY s.demand_score DESC, resource_count DESC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- Function: search_resources_by_text
-- Full text search for resources
CREATE OR REPLACE FUNCTION search_resources_by_text(search_query TEXT)
RETURNS TABLE (
    resource_id UUID,
    title TEXT,
    url TEXT,
    description TEXT,
    category TEXT,
    relevance_score NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        lr.id,
        lr.title,
        lr.url,
        lr.description,
        lr.category,
        lr.relevance_score
    FROM learning_resources lr
    WHERE 
        lr.title ILIKE '%' || search_query || '%'
        OR lr.description ILIKE '%' || search_query || '%'
    ORDER BY lr.relevance_score DESC
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;

-- View: chatbot_context
-- Pre-aggregated data for chatbot context
CREATE OR REPLACE VIEW chatbot_context AS
SELECT 
    s.skill_name,
    s.category,
    s.difficulty_level,
    s.demand_score,
    s.description as skill_description,
    COUNT(DISTINCT rs.resource_id) as resource_count,
    COUNT(DISTINCT st.id) as trend_data_points,
    AVG(st.trend_score) as avg_trend_score,
    ARRAY_AGG(DISTINCT lr.title) FILTER (WHERE lr.title IS NOT NULL) as sample_resources
FROM it_skills s
LEFT JOIN resource_skills rs ON s.id = rs.skill_id
LEFT JOIN learning_resources lr ON rs.resource_id = lr.id
LEFT JOIN skill_trends st ON s.id = st.skill_id
GROUP BY s.id, s.skill_name, s.category, s.difficulty_level, s.demand_score, s.description
ORDER BY s.demand_score DESC;

-- Comments
COMMENT ON TABLE resource_embeddings IS 'Vector embeddings of learning resources for semantic search';
COMMENT ON TABLE skill_embeddings IS 'Vector embeddings of skills for semantic matching';
COMMENT ON TABLE chat_history IS 'Conversation history for the chatbot';
COMMENT ON FUNCTION search_similar_resources IS 'Semantic search for similar resources using vector embeddings';
COMMENT ON FUNCTION search_similar_skills IS 'Find similar skills using vector embeddings';
COMMENT ON FUNCTION get_skill_with_resources IS 'Get a skill and all its related learning resources';
COMMENT ON VIEW chatbot_context IS 'Pre-aggregated context for chatbot responses';



