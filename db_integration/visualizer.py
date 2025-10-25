"""Visualization generator for IT skill trends."""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
from db_integration.trend_analyzer import TrendAnalyzer


class SkillTrendVisualizer:
    """Create visualizations for skill trends."""
    
    def __init__(self):
        """Initialize visualizer."""
        self.analyzer = TrendAnalyzer()
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def create_top_skills_chart(self, output_file: str = 'top_skills_chart.png', limit: int = 15):
        """Create bar chart of top skills for IT students.
        
        Args:
            output_file: Output filename
            limit: Number of skills to show
        """
        print(f"\nGenerating top skills chart...")
        
        # Get data
        skills = self.analyzer.db.get_top_skills_for_students(limit=limit)
        
        if not skills:
            print("No data available for chart")
            return
        
        # Prepare data
        skill_names = [s.get('skill_name', 'Unknown')[:20] for s in skills]
        demand_scores = [s.get('demand_score', 0) for s in skills]
        categories = [s.get('category', 'Other') for s in skills]
        
        # Create color map
        unique_categories = list(set(categories))
        colors = plt.cm.Set3(range(len(unique_categories)))
        category_colors = {cat: colors[i] for i, cat in enumerate(unique_categories)}
        bar_colors = [category_colors[cat] for cat in categories]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create horizontal bar chart
        y_pos = range(len(skill_names))
        bars = ax.barh(y_pos, demand_scores, color=bar_colors)
        
        # Customize
        ax.set_yticks(y_pos)
        ax.set_yticklabels(skill_names)
        ax.invert_yaxis()
        ax.set_xlabel('Demand Score', fontsize=12, fontweight='bold')
        ax.set_title('Top IT Skills for Students (By Demand)', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, 105)
        
        # Add value labels
        for i, (bar, score) in enumerate(zip(bars, demand_scores)):
            ax.text(score + 1, i, f'{score}', va='center', fontsize=9)
        
        # Add legend
        legend_elements = [plt.Rectangle((0,0),1,1, fc=category_colors[cat], label=cat) 
                          for cat in unique_categories]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
        
        # Add grid
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Chart saved to {output_file}")
    
    def create_category_distribution_chart(self, output_file: str = 'category_distribution.png'):
        """Create pie chart of skill category distribution.
        
        Args:
            output_file: Output filename
        """
        print(f"\nGenerating category distribution chart...")
        
        # Get data
        distribution = self.analyzer.get_category_distribution()
        
        if not distribution:
            print("No data available for chart")
            return
        
        # Prepare data
        categories = list(distribution.keys())
        counts = list(distribution.values())
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            counts,
            labels=categories,
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Set3(range(len(categories)))
        )
        
        # Customize text
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        ax.set_title('IT Skills by Category', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Chart saved to {output_file}")
    
    def create_skill_trend_timeline(self, output_file: str = 'skill_trends_timeline.png', days: int = 30):
        """Create line chart of skill trends over time.
        
        Args:
            output_file: Output filename
            days: Number of days to show
        """
        print(f"\nGenerating skill trends timeline...")
        
        # Get data
        df = self.analyzer.get_skill_growth_data(days=days)
        
        if df.empty:
            print("No trend data available")
            return
        
        # Get top 5 skills by average trend score
        if 'skill_name' in df.columns and 'trend_score' in df.columns:
            top_skills = df.groupby('skill_name')['trend_score'].mean().nlargest(5).index.tolist()
            
            # Create figure
            fig, ax = plt.subplots(figsize=(12, 6))
            
            for skill in top_skills:
                skill_data = df[df['skill_name'] == skill].sort_values('trend_date')
                if not skill_data.empty:
                    ax.plot(skill_data['trend_date'], skill_data['trend_score'], 
                           marker='o', label=skill, linewidth=2)
            
            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Trend Score', fontsize=12, fontweight='bold')
            ax.set_title('IT Skill Trends Over Time (Top 5)', fontsize=14, fontweight='bold', pad=20)
            ax.legend(loc='best', fontsize=10)
            ax.grid(True, alpha=0.3)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Chart saved to {output_file}")
        else:
            print("Insufficient data for timeline chart")
    
    def create_student_roadmap_chart(self, student_level: str, output_file: str = 'student_roadmap.png'):
        """Create visual roadmap for student learning path.
        
        Args:
            student_level: Student's current level
            output_file: Output filename
        """
        print(f"\nGenerating learning roadmap for {student_level} students...")
        
        # Get roadmap
        roadmap = self.analyzer.generate_learning_roadmap(student_level)
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Left chart: Timeline
        timeline = roadmap['timeline']
        phases = list(timeline.keys())
        skill_counts = [len(timeline[phase]) for phase in phases]
        
        ax1.barh(phases, skill_counts, color=plt.cm.Pastel1(range(len(phases))))
        ax1.set_xlabel('Number of Skills', fontsize=11, fontweight='bold')
        ax1.set_title(f'Learning Timeline for {student_level}', fontsize=13, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        # Add skill counts
        for i, count in enumerate(skill_counts):
            ax1.text(count + 0.1, i, str(count), va='center', fontweight='bold')
        
        # Right chart: Priority skills
        priority_skills = roadmap['priority_skills'][:5]
        if priority_skills:
            skill_names = [s.get('skill_name', 'Unknown')[:15] for s in priority_skills]
            scores = [s.get('avg_trend_score', 0) for s in priority_skills]
            
            ax2.barh(range(len(skill_names)), scores, color=plt.cm.RdYlGn(0.7))
            ax2.set_yticks(range(len(skill_names)))
            ax2.set_yticklabels(skill_names)
            ax2.invert_yaxis()
            ax2.set_xlabel('Trend Score', fontsize=11, fontweight='bold')
            ax2.set_title('Priority Skills (Trending)', fontsize=13, fontweight='bold')
            ax2.grid(axis='x', alpha=0.3)
            
            # Add value labels
            for i, score in enumerate(scores):
                ax2.text(score + 1, i, f'{score:.1f}', va='center', fontsize=9)
        
        plt.suptitle(f'IT Student Learning Roadmap - {student_level} Level', 
                    fontsize=15, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Roadmap chart saved to {output_file}")
    
    def create_all_charts(self, student_level: str = "Junior"):
        """Generate all visualization charts.
        
        Args:
            student_level: Student level for roadmap
        """
        print("\n" + "="*80)
        print("Generating All Visualization Charts")
        print("="*80)
        
        try:
            self.create_top_skills_chart()
            self.create_category_distribution_chart()
            self.create_skill_trend_timeline()
            self.create_student_roadmap_chart(student_level)
            
            print("\n" + "="*80)
            print("All charts generated successfully!")
            print("="*80)
            
        except Exception as e:
            print(f"Error generating charts: {e}")
            import traceback
            traceback.print_exc()

