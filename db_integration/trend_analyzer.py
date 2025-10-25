"""Trend analysis for IT student skillsets."""

from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import pandas as pd
from db_integration.supabase_client import SupabaseManager


class TrendAnalyzer:
    """Analyze skill trends for IT students."""
    
    def __init__(self):
        """Initialize trend analyzer."""
        self.db = SupabaseManager()
    
    def get_student_skill_recommendations(self, student_level: str = "Junior") -> Dict[str, Any]:
        """Get skill recommendations for IT students.
        
        Args:
            student_level: One of: Freshman, Sophomore, Junior, Senior, Graduate
            
        Returns:
            Comprehensive skill recommendations
        """
        print(f"\nAnalyzing skills for {student_level} IT students...")
        
        # Get top skills
        top_skills = self.db.get_top_skills_for_students(limit=30)
        
        # Get trend summary
        trend_summary = self.db.get_skill_trend_summary()
        
        # Get recommended learning path
        learning_path = self.db.get_recommended_learning_path(student_level)
        
        # Categorize skills
        categorized = self._categorize_by_difficulty(top_skills, student_level)
        
        # Create recommendations
        recommendations = {
            'student_level': student_level,
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_skills': len(top_skills),
                'trending_skills': len([s for s in trend_summary if s.get('avg_trend_score', 0) > 70]),
                'recommended_count': len(learning_path)
            },
            'immediate_focus': categorized['immediate'],
            'next_to_learn': categorized['next'],
            'advanced_skills': categorized['advanced'],
            'trending_skills': self._get_trending_skills(trend_summary, limit=10),
            'learning_path': learning_path,
            'skill_categories': self._group_by_category(top_skills)
        }
        
        return recommendations
    
    def _categorize_by_difficulty(self, skills: List[Dict], student_level: str) -> Dict[str, List[Dict]]:
        """Categorize skills by difficulty relative to student level.
        
        Args:
            skills: List of skills
            student_level: Student's current level
            
        Returns:
            Categorized skills
        """
        # Define what level should focus on what difficulty
        level_focus = {
            'Freshman': {'immediate': 'Beginner', 'next': 'Intermediate', 'advanced': 'Advanced'},
            'Sophomore': {'immediate': 'Beginner', 'next': 'Intermediate', 'advanced': 'Advanced'},
            'Junior': {'immediate': 'Intermediate', 'next': 'Advanced', 'advanced': 'Advanced'},
            'Senior': {'immediate': 'Intermediate', 'next': 'Advanced', 'advanced': 'Advanced'},
            'Graduate': {'immediate': 'Advanced', 'next': 'Advanced', 'advanced': 'Advanced'}
        }
        
        focus = level_focus.get(student_level, level_focus['Junior'])
        
        categorized = {
            'immediate': [],
            'next': [],
            'advanced': []
        }
        
        for skill in skills[:15]:  # Top 15 skills
            difficulty = skill.get('difficulty_level', 'Intermediate')
            
            if difficulty == focus['immediate']:
                categorized['immediate'].append(skill)
            elif difficulty == focus['next']:
                categorized['next'].append(skill)
            else:
                categorized['advanced'].append(skill)
        
        return categorized
    
    def _get_trending_skills(self, trend_summary: List[Dict], limit: int = 10) -> List[Dict]:
        """Get top trending skills.
        
        Args:
            trend_summary: Trend summary data
            limit: Number of skills to return
            
        Returns:
            Top trending skills
        """
        # Sort by avg_trend_score
        sorted_trends = sorted(
            trend_summary,
            key=lambda x: x.get('avg_trend_score', 0),
            reverse=True
        )
        
        return sorted_trends[:limit]
    
    def _group_by_category(self, skills: List[Dict]) -> Dict[str, List[Dict]]:
        """Group skills by category.
        
        Args:
            skills: List of skills
            
        Returns:
            Skills grouped by category
        """
        grouped = {}
        
        for skill in skills:
            category = skill.get('category', 'Other')
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(skill)
        
        return grouped
    
    def get_skill_growth_data(self, days: int = 30) -> pd.DataFrame:
        """Get skill trend data for visualization.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            DataFrame with skill trends over time
        """
        trends = self.db.get_skill_trends(days=days)
        
        if not trends:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(trends)
        
        # Extract skill name from nested data if present
        if 'it_skills' in df.columns:
            df['skill_name'] = df['it_skills'].apply(lambda x: x.get('skill_name', '') if isinstance(x, dict) else '')
            df['category'] = df['it_skills'].apply(lambda x: x.get('category', '') if isinstance(x, dict) else '')
        
        return df
    
    def get_category_distribution(self) -> Dict[str, int]:
        """Get distribution of skills by category.
        
        Returns:
            Category distribution
        """
        skills = self.db.get_top_skills(limit=100)
        
        distribution = {}
        for skill in skills:
            category = skill.get('category', 'Other')
            distribution[category] = distribution.get(category, 0) + 1
        
        return distribution
    
    def get_top_skills_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """Get top skills in a specific category.
        
        Args:
            category: Category name
            limit: Number of skills to return
            
        Returns:
            Top skills in category
        """
        all_skills = self.db.get_top_skills(limit=100)
        
        category_skills = [s for s in all_skills if s.get('category') == category]
        return category_skills[:limit]
    
    def generate_learning_roadmap(self, student_level: str, focus_area: str = None) -> Dict[str, Any]:
        """Generate a personalized learning roadmap.
        
        Args:
            student_level: Student's current level
            focus_area: Optional focus area (AI/ML, Web Development, etc.)
            
        Returns:
            Learning roadmap with timeline
        """
        recommendations = self.get_student_skill_recommendations(student_level)
        
        roadmap = {
            'student_level': student_level,
            'focus_area': focus_area or 'General IT',
            'timeline': {
                'Month 1-2': recommendations['immediate_focus'][:3],
                'Month 3-4': recommendations['immediate_focus'][3:6] if len(recommendations['immediate_focus']) > 3 else recommendations['next_to_learn'][:3],
                'Month 5-6': recommendations['next_to_learn'][:3],
                'Month 7-12': recommendations['advanced_skills'][:5]
            },
            'priority_skills': recommendations['trending_skills'][:5]
        }
        
        return roadmap

