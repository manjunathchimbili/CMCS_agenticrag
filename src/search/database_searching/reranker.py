from dotenv import load_dotenv
from common.utils.settings import aws_client, MODEL_ID

load_dotenv()


class CohereReranker:
    
    def __init__(self):
        self.client = aws_client('bedrock-agent-runtime')
        self.model_id = "cohere.rerank-v3-5:0"
        self.region = "us-east-1"
        self.model_package_arn = f"arn:aws:bedrock:{self.region}::foundation-model/{self.model_id}"

    async def rerank_results(self, query, documents, top_k: int = 5):

        if not documents:
            return []
        
        source = []
        for doc in documents:
            if isinstance(doc, str):
                source.append({
                        "type": "INLINE",
                        "inlineDocumentSource": {
                            "type": "TEXT",
                            "textDocument": {
                                "text": doc
                            }
                        }
                    })
            elif isinstance(doc, dict) and 'text' in doc:
                source.append({
                        "type": "INLINE",
                        "inlineDocumentSource": {
                            "type": "TEXT",
                            "textDocument": {
                                "text": doc['text']
                            }
                        }
                    })
            else:
                raise ValueError("Each document must be either a string or a dict with a 'text' key.")
        

        num_results = min(top_k, len(source))
        
        response = self.client.rerank(
                        queries=[
                            {
                                "type": "TEXT",
                                "textQuery": {
                                    "text": query
                                }
                            }
                        ],
                        sources=source,
                        rerankingConfiguration={
                            "type": "BEDROCK_RERANKING_MODEL",
                            "bedrockRerankingConfiguration": {
                            "numberOfResults": num_results,
                            "modelConfiguration": {
                            "modelArn": self.model_package_arn,
                                }
                            }
                        }
        )

        results = response['results']
    


        reranked = []
        for result in results:
            idx = result['index']
            score = result['relevanceScore']
            original_doc = documents[idx]
            doc_dict = original_doc if isinstance(original_doc, dict) else {"text": original_doc}
            reranked.append({
                **doc_dict,
                "rerank_score": score,
                "original_index": idx
            })
            
        return reranked




