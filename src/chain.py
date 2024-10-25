from langchain import hub

class RagChain:
    def __init__(self,llm,vectorstore):
        self.llm = llm
        self.prompt = hub.pull("rlm/rag-prompt")
        self.vectorstore = vectorstore

    def invoke(self, input):
        return self.llm.invoke(self.prompt.format(context=self.vectorstore.similarity_search(input,k=2)[0].page_content, question=input))
    
    async def ainvoke(self, input):
        results = await self.vectorstore.asimilarity_search(input,k=2)
        print(results)
        context = "/n".join([doc.page_content for doc in results])
        response = await self.llm.ainvoke(self.prompt.format(context=context, question=input))
        return response