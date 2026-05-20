import asyncio

from search.database_searching.search import SearchEngine


async def get_search_results(query: str):

    search = SearchEngine()

    semantic_results = await search.semantic_search(query)
    hybrid_results = await search.hybrid_search(query, top_k=5)
    reranking_results = await search.hybrid_cohere_search(query, hybridresult=hybrid_results)

    def extract_text(results):

        texts = [result.get('text', '') for result in results if result.get('text')]
        return "\n\n".join(texts)

    return {
        "semantic": extract_text(semantic_results),
        "hybrid": extract_text(hybrid_results),
        "reranked": extract_text(reranking_results)
    }



