"""Data loader to sync GenAI agent results to Supabase."""

from typing import Dict, Any, List
from datetime import date
from db_integration.supabase_client import SupabaseManager
from db_integration.skill_extractor import SkillExtractor, calculate_skill_demand
import json


class DataLoader:
    """Load GenAI agent data into Supabase."""
    
    def __init__(self):
        """Initialize data loader."""
        self.db = SupabaseManager()
        self.skill_extractor = SkillExtractor()
    
    def load_report(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Load a complete agent report into Supabase.
        
        Args:
            report: Report from GenAIAgentOrchestrator
            
        Returns:
            Loading statistics
        """
        stats = {
            'resources_loaded': 0,
            'topics_loaded': 0,
            'skills_extracted': 0,
            'skills_linked': 0,
            'trends_created': 0
        }
        
        print("\n" + "="*80)
        print("Loading Data to Supabase")
        print("="*80)
        
        # Load learning resources
        print(f"\n[1/5] Loading {len(report.get('learning_resources', []))} learning resources...")
        resources = report.get('learning_resources', [])
        loaded_resources = self.db.bulk_insert_resources(resources)
        stats['resources_loaded'] = len(loaded_resources)
        print(f"Loaded {stats['resources_loaded']} resources")
        
        # Load trending topics
        print(f"\n[2/5] Loading {len(report.get('trending_topics', []))} trending topics...")
        topics = report.get('trending_topics', [])
        loaded_topics = self.db.bulk_insert_topics(topics)
        stats['topics_loaded'] = len(loaded_topics)
        print(f"Loaded {stats['topics_loaded']} topics")
        
        # Extract and load skills
        print(f"\n[3/5] Extracting skills from resources...")
        all_skills = {}
        resource_skill_links = []
        
        for resource_data, db_resource in zip(resources, loaded_resources):
            if not db_resource or 'id' not in db_resource:
                continue
            
            # Extract skills
            skills = self.skill_extractor.extract_and_categorize(resource_data)
            
            for skill in skills:
                skill_name = skill['skill_name']
                
                # Track unique skills
                if skill_name not in all_skills:
                    all_skills[skill_name] = skill
                
                # Record link between resource and skill
                resource_skill_links.append({
                    'resource_id': db_resource['id'],
                    'skill': skill
                })
        
        print(f"Extracted {len(all_skills)} unique skills")
        
        # Insert skills into database
        print(f"\n[4/5] Inserting skills into database...")
        skill_id_map = {}
        
        for skill_name, skill_data in all_skills.items():
            # Check if skill already exists
            existing_skill = self.db.get_skill_by_name(skill_name)
            
            if existing_skill:
                skill_id_map[skill_name] = existing_skill['id']
            else:
                # Calculate demand score
                demand_score = calculate_skill_demand(skill_name, resources)
                
                # Insert new skill
                new_skill = {
                    'skill_name': skill_name,
                    'category': skill_data['category'],
                    'difficulty_level': skill_data.get('difficulty_level', 'Intermediate'),
                    'demand_score': demand_score,
                    'description': f"Skill in {skill_data['category']}"
                }
                
                inserted = self.db.insert_skill(new_skill)
                if inserted and 'id' in inserted:
                    skill_id_map[skill_name] = inserted['id']
                    stats['skills_extracted'] += 1
        
        print(f"Inserted {stats['skills_extracted']} new skills")
        
        # Link resources to skills
        print(f"\n[5/5] Linking resources to skills...")
        for link in resource_skill_links:
            resource_id = link['resource_id']
            skill_name = link['skill']['skill_name']
            
            if skill_name in skill_id_map:
                skill_id = skill_id_map[skill_name]
                relevance = int(link['skill'].get('confidence', 0.5) * 10)
                self.db.link_resource_to_skill(resource_id, skill_id, relevance)
                stats['skills_linked'] += 1
        
        print(f"Created {stats['skills_linked']} resource-skill links")
        
        # Create skill trends for today
        print(f"\n[BONUS] Creating skill trend records...")
        today = date.today()
        
        for skill_name, skill_id in skill_id_map.items():
            # Count mentions in loaded resources
            mentions = sum(1 for r in resources 
                          if skill_name.lower() in f"{r.get('title', '')} {r.get('description', '')}".lower())
            
            # Count GitHub references in topics
            github_stars = sum(t.get('metrics', {}).get('stars', 0) 
                             for t in topics 
                             if skill_name.lower() in t.get('title', '').lower())
            
            # Count LinkedIn engagement in topics (Bug Fix #1)
            linkedin_posts = sum(t.get('metrics', {}).get('estimated_posts', 0) 
                               for t in topics 
                               if skill_name.lower() in t.get('title', '').lower() or 
                                  skill_name.lower() in t.get('description', '').lower())
            
            # Calculate weighted trend score (Bug Fix #2)
            from db_integration.skill_extractor import calculate_weighted_trend_score
            trend_score = calculate_weighted_trend_score(
                mention_count=mentions,
                github_stars=github_stars,
                linkedin_posts=linkedin_posts,
                total_resources=len(resources)
            )
            
            trend_data = {
                'date': today.isoformat(),
                'mentions': mentions,
                'resources': len([l for l in resource_skill_links 
                                 if l['skill']['skill_name'] == skill_name]),
                'github_stars': github_stars,
                'linkedin_posts': linkedin_posts,
                'score': trend_score
            }
            
            self.db.insert_skill_trend(skill_id, trend_data)
            stats['trends_created'] += 1
        
        print(f"Created {stats['trends_created']} trend records")
        
        print("\n" + "="*80)
        print("Data Loading Complete!")
        print("="*80)
        
        return stats
    
    def load_from_json_file(self, filename: str) -> Dict[str, Any]:
        """Load data from a JSON report file.
        
        Args:
            filename: Path to JSON report file
            
        Returns:
            Loading statistics
        """
        print(f"\nLoading report from {filename}...")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            return self.load_report(report)
        
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {filename}: {e}")
            return {}
        except Exception as e:
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()
            return {}


def load_data_to_supabase(report: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to load data to Supabase.
    
    Args:
        report: Agent report dictionary
        
    Returns:
        Loading statistics
    """
    loader = DataLoader()
    return loader.load_report(report)

