"""Skill extraction and categorization for IT students."""

from typing import List, Dict, Any, Set
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import config
import re


# IT Skills taxonomy for students
IT_SKILLS_TAXONOMY = {
    'AI/ML': [
        'Generative AI', 'GenAI', 'LLM', 'Large Language Models', 'GPT',
        'LangChain', 'LangGraph', 'Prompt Engineering', 'RAG',
        'Retrieval Augmented Generation', 'Fine-tuning', 'Vector Databases',
        'Embeddings', 'Transformers', 'BERT', 'OpenAI', 'Hugging Face',
        'Machine Learning', 'Deep Learning', 'Neural Networks', 'NLP',
        'Computer Vision', 'TensorFlow', 'PyTorch', 'Keras'
    ],
    'Programming': [
        'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#',
        'Go', 'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin',
        'Object-Oriented Programming', 'Functional Programming',
        'Data Structures', 'Algorithms', 'Design Patterns'
    ],
    'Web Development': [
        'HTML', 'CSS', 'React', 'Vue.js', 'Angular', 'Next.js',
        'Node.js', 'Express', 'Django', 'Flask', 'FastAPI',
        'REST APIs', 'GraphQL', 'WebSockets', 'Responsive Design',
        'Frontend', 'Backend', 'Full Stack'
    ],
    'Cloud': [
        'AWS', 'Azure', 'Google Cloud', 'GCP', 'Cloud Computing',
        'Docker', 'Kubernetes', 'Serverless', 'Lambda', 'EC2',
        'S3', 'Container', 'Microservices', 'Cloud Architecture'
    ],
    'Database': [
        'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis',
        'Database Design', 'NoSQL', 'Relational Database',
        'Supabase', 'Firebase', 'DynamoDB', 'Cassandra'
    ],
    'DevOps': [
        'Git', 'GitHub', 'GitLab', 'CI/CD', 'Jenkins',
        'GitHub Actions', 'DevOps', 'Automation', 'Testing',
        'Unit Testing', 'Integration Testing', 'Deployment'
    ],
    'Data Science': [
        'Data Analysis', 'Data Visualization', 'pandas', 'NumPy',
        'Matplotlib', 'Seaborn', 'Jupyter', 'Statistics',
        'Big Data', 'Spark', 'Hadoop', 'ETL'
    ],
    'Mobile': [
        'iOS Development', 'Android Development', 'React Native',
        'Flutter', 'Mobile Apps', 'SwiftUI', 'Jetpack Compose'
    ]
}


class SkillExtractor:
    """Extract and categorize IT skills from learning resources."""
    
    def __init__(self):
        """Initialize skill extractor."""
        try:
            self.llm = ChatOpenAI(
                model=config.LLM_MODEL,
                temperature=0.3,
                api_key=config.OPENAI_API_KEY
            )
        except Exception:
            self.llm = None
            print("[WARNING] LLM not available, using keyword-based extraction only")
        
        # Create normalized skill map for faster lookup
        self.skill_map = self._build_skill_map()
    
    def _build_skill_map(self) -> Dict[str, str]:
        """Build normalized skill name to category mapping."""
        skill_map = {}
        for category, skills in IT_SKILLS_TAXONOMY.items():
            for skill in skills:
                skill_map[skill.lower()] = {
                    'name': skill,
                    'category': category
                }
        return skill_map
    
    def extract_skills_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills from text using keyword matching.
        
        Args:
            text: Text to extract skills from
            
        Returns:
            List of extracted skills with metadata
        """
        text_lower = text.lower()
        found_skills = []
        seen_skills = set()
        
        for skill_key, skill_data in self.skill_map.items():
            # Check if skill is mentioned in text
            if skill_key in text_lower:
                skill_name = skill_data['name']
                if skill_name not in seen_skills:
                    found_skills.append({
                        'skill_name': skill_name,
                        'category': skill_data['category'],
                        'confidence': 0.8
                    })
                    seen_skills.add(skill_name)
        
        return found_skills
    
    def extract_skills_from_resource(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract skills from a learning resource.
        
        Args:
            resource: Resource with title, description, etc.
            
        Returns:
            List of extracted skills
        """
        # Combine title and description for analysis
        text = f"{resource.get('title', '')} {resource.get('description', '')}"
        
        # Extract using keyword matching
        skills = self.extract_skills_from_text(text)
        
        # If LLM is available, enhance with AI extraction
        if self.llm and len(text) > 50:
            ai_skills = self._extract_with_llm(text)
            skills = self._merge_skills(skills, ai_skills)
        
        return skills
    
    def _extract_with_llm(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills using LLM.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of extracted skills
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an IT skills expert. Extract relevant IT skills 
            mentioned in the text. Focus on skills that IT students should learn.
            Return only the skill names, one per line."""),
            ("user", "Text: {text}\n\nExtract IT skills:")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(text=text[:500]))
            skill_lines = response.content.strip().split('\n')
            
            skills = []
            for line in skill_lines:
                # Clean up the line
                skill_name = re.sub(r'^[-*•]\s*', '', line).strip()
                if skill_name and len(skill_name) > 2:
                    # Try to categorize
                    category = self._categorize_skill(skill_name)
                    skills.append({
                        'skill_name': skill_name,
                        'category': category,
                        'confidence': 0.7
                    })
            
            return skills
        except Exception as e:
            print(f"[WARNING] LLM extraction failed: {e}")
            return []
    
    def _categorize_skill(self, skill_name: str) -> str:
        """Categorize a skill name.
        
        Args:
            skill_name: Name of the skill
            
        Returns:
            Category name
        """
        skill_lower = skill_name.lower()
        
        # Check if it matches any known skill
        if skill_lower in self.skill_map:
            return self.skill_map[skill_lower]['category']
        
        # Use keyword matching to guess category
        for category, skills in IT_SKILLS_TAXONOMY.items():
            for known_skill in skills:
                if known_skill.lower() in skill_lower or skill_lower in known_skill.lower():
                    return category
        
        return 'Other'
    
    def _merge_skills(self, skills1: List[Dict], skills2: List[Dict]) -> List[Dict]:
        """Merge two lists of skills, removing duplicates.
        
        Args:
            skills1: First list of skills
            skills2: Second list of skills
            
        Returns:
            Merged list
        """
        merged = {}
        
        for skill in skills1 + skills2:
            name = skill['skill_name']
            if name not in merged or skill['confidence'] > merged[name]['confidence']:
                merged[name] = skill
        
        return list(merged.values())
    
    def categorize_difficulty(self, skill_name: str) -> str:
        """Determine difficulty level of a skill.
        
        Args:
            skill_name: Name of the skill
            
        Returns:
            Difficulty level: Beginner, Intermediate, or Advanced
        """
        skill_lower = skill_name.lower()
        
        # Beginner skills
        beginner_keywords = [
            'html', 'css', 'python', 'git', 'sql', 'javascript basics',
            'data structures', 'algorithms', 'programming basics'
        ]
        
        # Advanced skills
        advanced_keywords = [
            'kubernetes', 'distributed systems', 'fine-tuning', 'rag',
            'advanced', 'architecture', 'scalability', 'microservices',
            'system design'
        ]
        
        if any(kw in skill_lower for kw in beginner_keywords):
            return 'Beginner'
        elif any(kw in skill_lower for kw in advanced_keywords):
            return 'Advanced'
        else:
            return 'Intermediate'
    
    def extract_and_categorize(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract skills from resource and add full categorization.
        
        Args:
            resource: Learning resource
            
        Returns:
            List of fully categorized skills
        """
        skills = self.extract_skills_from_resource(resource)
        
        # Add difficulty level
        for skill in skills:
            skill['difficulty_level'] = self.categorize_difficulty(skill['skill_name'])
        
        return skills


def calculate_skill_demand(skill_name: str, resources: List[Dict[str, Any]]) -> int:
    """Calculate demand score for a skill based on mentions.
    
    Args:
        skill_name: Name of the skill
        resources: List of resources to analyze
        
    Returns:
        Demand score (0-100)
    """
    mention_count = 0
    skill_lower = skill_name.lower()
    
    for resource in resources:
        text = f"{resource.get('title', '')} {resource.get('description', '')}".lower()
        if skill_lower in text:
            mention_count += 1
    
    # Normalize to 0-100 scale
    max_mentions = len(resources) * 0.3  # Assume max 30% mention rate
    score = min(100, int((mention_count / max_mentions) * 100)) if max_mentions > 0 else 0
    
    return max(score, 50)  # Minimum score of 50 for known skills

