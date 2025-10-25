"""Generate embeddings without prompts."""

from db_integration.embedding_manager import EmbeddingManager

print("\nGenerating vector embeddings...")
print("This will take 1-2 minutes...\n")

manager = EmbeddingManager()
stats = manager.generate_all_embeddings()

print(f"\n[OK] Complete!")
print(f"  Resources embedded: {stats['resources']}")
print(f"  Skills embedded: {stats['skills']}")
print(f"\nRAG is now active! You can use the chatbot.")

