import pandas as pd
# Example dataset: user queries and associated document sections
data = [
    {"query": "What is RAG?", "section": "Introduction to RAG"},
    {"query": "Benefits of RAG", "section": "RAG Benefits and Use Cases"},
    {"query": "How does chunking work?", "section": "Chunking in RAG Systems"}
]
# Convert data to a DataFrame
df = pd.DataFrame(data)
def prioritize_chunks(queries, sections):
    """
    Prioritize chunks based on query relevance.
    """
    chunk_score = {}
    for query in queries:
        for section in sections:
            # Simplified scoring: counting overlapping keywords
            score = len(set(query.lower().split()) & set(section.lower().split()))
            chunk_score[section] = chunk_score.get(section, 0) + score

    # Sort chunks by relevance score
    return sorted(chunk_score.items(), key=lambda x: x[1], reverse=True)
# Example usage
queries = df['query']
sections = df['section']
prioritized_chunks = prioritize_chunks(queries, sections)
print("Prioritized Chunks:")
for section, score in prioritized_chunks:
    print(f"{section}: {score}")