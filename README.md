




***********************************************(RUN the GraphQL)*******************************************************************************

mutation {
  processQuery(query: "What are the key features of the contract?") {
    query
    semantic {
      searchType
      response
      strategy
    }
    hybrid {
      searchType
      response
      strategy
    }
    reranked {
      searchType
      response
      strategy
    }
  }
}

***********************************************(RUN the GraphQL)*******************************************************************************
# CMCS_agenticrag
