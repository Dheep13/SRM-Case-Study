"""Embedding manager for generating and storing vector embeddings."""

from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings
from db_integration.supabase_client import SupabaseManager
import config


class EmbeddingManager:
    """Manage vector embeddings for resources and skills."""
    
    def __init__(self):
        """Initialize embedding manager."""
        self.db = SupabaseManager()
        self.embeddings = OpenAIEmbeddings(api_key=config.OPENAI_API_KEY)
    
    def generate_resource_embeddings(self) -> int:
        """Generate embeddings for all learning resources.
        
        Returns:
            Number of embeddings created
        """
        print("\nGenerating embeddings for learning resources...")
        
        # Get all resources
        resources = self.db.get_all_resources(limit=1000)
        count = 0
        
        for resource in resources:
            try:
                # Create text to embed
                text = f"{resource.get('title', '')} {resource.get('description', '')} {resource.get('category', '')}"
                
                # Generate embedding
                embedding = self.embeddings.embed_query(text)
                
                # Store in database
                self.db.client.table('resource_embeddings').upsert({
                    'resource_id': resource['id'],
                    'embedding': embedding,
                    'content_text': text[:500]  # Store first 500 chars
                }, on_conflict='resource_id').execute()
                
                count += 1
                if count % 10 == 0:
                    print(f"  Processed {count}/{len(resources)} resources...")
            
            except Exception as e:
                print(f"  Error processing resource {resource.get('id')}: {e}")
                continue
        
        print(f"[OK] Created {count} resource embeddings")
        return count
    
    def generate_skill_embeddings(self) -> int:
        """Generate embeddings for all skills.
        
        Returns:
            Number of embeddings created
        """
        print("\nGenerating embeddings for skills...")
        
        # Get all skills
        skills = self.db.get_top_skills(limit=1000)
        count = 0
        
        for skill in skills:
            try:
                # Create text to embed
                text = f"{skill.get('skill_name', '')} {skill.get('description', '')} {skill.get('category', '')} {skill.get('difficulty_level', '')}"
                
                # Generate embedding
                embedding = self.embeddings.embed_query(text)
                
                # Store in database
                self.db.client.table('skill_embeddings').upsert({
                    'skill_id': skill['id'],
                    'embedding': embedding,
                    'description_text': text[:500]
                }, on_conflict='skill_id').execute()
                
                count += 1
                if count % 5 == 0:
                    print(f"  Processed {count}/{len(skills)} skills...")
            
            except Exception as e:
                print(f"  Error processing skill {skill.get('id')}: {e}")
                continue
        
        print(f"[OK] Created {count} skill embeddings")
        return count
    
    def generate_all_embeddings(self) -> Dict[str, int]:
        """Generate all embeddings.
        
        Returns:
            Count of embeddings created
        """
        print("\n" + "="*80)
        print("Generating Vector Embeddings for Chatbot")
        print("="*80)
        
        stats = {
            'resources': 0,
            'skills': 0
        }
        
        try:
            stats['resources'] = self.generate_resource_embeddings()
            stats['skills'] = self.generate_skill_embeddings()
            
            print("\n" + "="*80)
            print(f"[OK] Embedding Generation Complete!")
            print(f"  - Resource embeddings: {stats['resources']}")
            print(f"  - Skill embeddings: {stats['skills']}")
            print("="*80)
        
        except Exception as e:
            print(f"\n[ERROR] Error generating embeddings: {e}")
            import traceback
            traceback.print_exc()
        
        return stats
    
    def search_similar_resources(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar resources using embeddings.
        
        Args:
            query: Search query
            limit: Number of results
            
        Returns:
            List of similar resources
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        try:
            result = self.db.client.rpc(
                'search_similar_resources',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.6,
                    'match_count': limit
                }
            ).execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error searching resources: {e}")
            return []
    
    def search_similar_skills(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for similar skills using embeddings.
        
        Args:
            query: Search query
            limit: Number of results
            
        Returns:
            List of similar skills
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        try:
            result = self.db.client.rpc(
                'search_similar_skills',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.6,
                    'match_count': limit
                }
            ).execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error searching skills: {e}")
            return []

