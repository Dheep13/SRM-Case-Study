# IT Skills Chatbot - Setup Guide

## Overview

An AI-powered chatbot that lets students query the IT skills database using natural language. The chatbot uses:
- **Vector embeddings** for semantic search
- **PostgreSQL pgvector** for similarity matching
- **LangChain** for conversation management
- **OpenAI GPT** for natural language responses

## Features

✅ Ask questions in plain English
✅ Get personalized skill recommendations
✅ Find learning resources instantly
✅ Semantic search (understands meaning, not just keywords)
✅ Context-aware conversations
✅ Student-level tailored responses

## Setup (5 minutes)

### Step 1: Run Vector Embeddings SQL

1. Go to Supabase dashboard → SQL Editor
2. Copy contents of `db_integration/vector_embeddings.sql`
3. Paste and **Run**
4. Wait for "Success" message

This creates:
- `resource_embeddings` table
- `skill_embeddings` table  
- `chat_history` table
- Vector search functions
- Semantic search capabilities

### Step 2: Generate Embeddings

After loading data to Supabase, generate vector embeddings:

```powershell
python setup_chatbot.py
```

This will:
- Generate embeddings for all resources (~10-50)
- Generate embeddings for all skills (~20-30)
- Takes 1-2 minutes
- Uses OpenAI embeddings API

### Step 3: Start Chatting!

```powershell
python chat_with_database.py
```

## Usage Examples

### Example Conversation

```
You: What skills should I learn as a Junior?

Bot: Great question! Based on current market demand, here are the top skills 
for Junior students:

**Immediate Focus:**
- **Generative AI** (Demand: 95) - Hot emerging field with lots of opportunities
- **Python** (Demand: 95) - Essential foundation for AI/ML and backend development
- **Docker** (Demand: 90) - Industry standard for containerization

**Learning Resources:**
- Coursera: Develop Generative AI Applications
- LangChain Documentation: https://python.langchain.com/
- Docker Getting Started Guide

I recommend starting with Python basics, then moving to GenAI concepts!

---

You: Tell me more about LangChain

Bot: **LangChain** is a powerful framework for building applications with Large 
Language Models (LLMs). Here's what you should know:

**Category:** AI/ML
**Difficulty:** Intermediate
**Demand Score:** 90/100

**Why Learn It:**
- Build chatbots and AI assistants
- Create RAG (Retrieval Augmented Generation) systems
- Integrate multiple AI models
- Growing industry adoption

**Learning Resources:**
1. LangChain Documentation (Official)
   https://python.langchain.com/docs/get_started/introduction

2. LangChain GitHub Repo
   https://github.com/langchain-ai/langchain

**Prerequisites:** Python, basic understanding of APIs

Would you like specific tutorials or project ideas?

---

You: Yes, show me project ideas

Bot: Here are beginner-friendly LangChain projects:

1. **AI Document Q&A**
   - Upload PDFs and ask questions
   - Uses RAG for accurate answers
   - Great for learning resource management

2. **Personal Learning Assistant**
   - Chatbot that tracks your learning goals
   - Recommends skills based on interests
   - Similar to what you're using now!

3. **Code Helper Bot**
   - Answers programming questions
   - Suggests code improvements
   - Explains error messages

4. **Study Buddy**
   - Creates flashcards from notes
   - Quizzes you on topics
   - Tracks progress over time

Start with project #1 - it teaches core LangChain concepts like:
- Document loaders
- Vector stores
- Chains and agents
- Memory management

Want resources for any specific project?
```

## Example Questions

### Skills Discovery
```
- What skills should I learn?
- What are the top trending skills?
- Tell me about Generative AI
- What's the demand for React?
- Should I learn Kubernetes?
```

### Learning Resources
```
- Show me Python tutorials
- Find GenAI courses
- Best resources for learning Docker
- Where can I learn RAG?
```

### Career Planning
```
- How do I become an AI engineer?
- What skills do I need for web development?
- Career path for data science
- Skills for cloud engineering
```

### Comparisons
```
- Python vs JavaScript for beginners
- AWS vs Azure for students
- React vs Vue.js which to learn?
```

## Special Commands

- `quit` or `exit` - End conversation
- `clear` - Clear conversation history
- `level` - Change your student level

## How It Works

### 1. Vector Embeddings

When you ask a question:
```
"What are good AI skills?"
```

The system:
1. Converts your question to a 1536-dimensional vector
2. Searches database for similar skill vectors
3. Finds semantically related skills (GenAI, LLM, ML, etc.)
4. Returns top matches with context

### 2. Semantic Search

Traditional search (keyword matching):
```
Query: "machine learning"
Finds: Only items with exact phrase "machine learning"
```

Semantic search (meaning-based):
```
Query: "machine learning"
Finds: ML, AI, Neural Networks, Deep Learning, TensorFlow, etc.
Understanding: All are related concepts!
```

### 3. Context-Aware Responses

The chatbot remembers conversation context:
```
You: What is LangChain?
Bot: [Explains LangChain]

You: How do I learn it?
Bot: [Knows "it" refers to LangChain from context]
```

## Database Schema

### Vector Tables

**resource_embeddings**
- `id` - UUID
- `resource_id` - Foreign key to learning_resources
- `embedding` - vector(1536) - OpenAI embedding
- `content_text` - Original text

**skill_embeddings**
- `id` - UUID
- `skill_id` - Foreign key to it_skills
- `embedding` - vector(1536)
- `description_text` - Skill description

**chat_history**
- `id` - UUID
- `session_id` - Conversation session
- `user_message` - What you asked
- `bot_response` - What bot answered
- `context_used` - Data used for response

### Search Functions

**search_similar_resources(query_embedding, threshold, count)**
- Input: Vector embedding
- Output: Similar resources with similarity scores
- Uses: Cosine distance

**search_similar_skills(query_embedding, threshold, count)**
- Input: Vector embedding
- Output: Similar skills with scores
- Uses: Cosine distance

## Programmatic Usage

### Python API

```python
from db_integration.chatbot import SkillsChatbot

# Initialize chatbot
bot = SkillsChatbot()

# Ask a question
response = bot.chat("What should I learn?", student_level="Junior")
print(response)

# Get skill details
details = bot.get_skill_details("Python")
print(details)

# Get recommendations
recs = bot.get_recommendations("Junior", focus_area="AI/ML")
for skill in recs:
    print(f"{skill['skill_name']}: {skill['demand_score']}")

# Search with embeddings
from db_integration.embedding_manager import EmbeddingManager

manager = EmbeddingManager()
similar = manager.search_similar_skills("artificial intelligence", limit=5)
for skill in similar:
    print(f"{skill['skill_name']} (similarity: {skill['similarity']:.2f})")
```

## Cost Considerations

### OpenAI API Costs

**Embedding Generation (One-time)**
- Model: text-embedding-ada-002
- Cost: $0.0001 per 1K tokens
- For 50 resources + 30 skills: ~$0.01
- Run once, reuse embeddings

**Chat Queries**
- Model: gpt-4-turbo
- Cost: ~$0.01-0.03 per query
- Depends on conversation length

**Tips to Save Costs:**
1. Generate embeddings once
2. Use gpt-3.5-turbo for cheaper queries
3. Clear conversation history periodically
4. Cache frequent queries

## Troubleshooting

**Error: "cannot import name 'create_client'"**
- Folder renamed to `db_integration` to avoid conflicts
- Imports updated automatically

**Error: "relation 'resource_embeddings' does not exist"**
- Run `vector_embeddings.sql` in Supabase SQL Editor

**Error: "column 'embedding' does not exist"**
- Enable pgvector extension in Supabase
- Run: `CREATE EXTENSION vector;`

**No results from semantic search**
- Generate embeddings first: `python setup_chatbot.py`
- Ensure data is loaded in database

**Chatbot gives generic responses**
- Check if embeddings are created
- Verify data in `resource_embeddings` and `skill_embeddings` tables
- Ensure OpenAI API key is valid

## Advanced Features

### Custom Similarity Thresholds

```python
# More strict matching (higher quality, fewer results)
results = manager.search_similar_skills("AI", limit=5)

# Adjust in SQL:
SELECT * FROM search_similar_skills(
    query_embedding, 
    0.8,  -- Higher threshold = more similar required
    10
);
```

### Multi-turn Conversations

The chatbot maintains context across multiple questions:

```python
bot = SkillsChatbot()

# Question 1
bot.chat("What is Python?")

# Question 2 (uses context from Q1)
bot.chat("Show me resources for it")  # "it" = Python

# Question 3 (builds on conversation)
bot.chat("What about advanced topics?")  # Advanced Python topics
```

### Session Management

```python
# Track specific user session
bot = SkillsChatbot(session_id="student_123")

# Later, retrieve history
history = bot.get_session_history()
for msg in history:
    print(f"User: {msg['user_message']}")
    print(f"Bot: {msg['bot_response']}\n")
```

## Benefits

### For Students
- **Instant Answers** - No searching through docs
- **Personalized** - Tailored to your level
- **Conversational** - Ask follow-ups naturally
- **Always Updated** - Database refreshes weekly

### For Educators
- **Student Analytics** - Track common questions
- **Curriculum Insights** - See what students want to learn
- **Automated Support** - Reduce repetitive questions
- **Data-Driven** - Recommendations based on real demand

## Next Steps

1. ✅ Set up vector embeddings
2. ✅ Generate embeddings for data
3. ✅ Start chatting with database
4. 📚 Ask questions and learn
5. 🔄 Update data weekly
6. 🚀 Build your own chatbot features!

## Integration Ideas

- **Discord Bot** - Add to study server
- **Web Dashboard** - Build React frontend
- **Mobile App** - iOS/Android chatbot
- **Slack Bot** - Team learning assistant
- **Email Digest** - Weekly skill recommendations

---

**Ready to chat with your database?**

```powershell
python chat_with_database.py
```

