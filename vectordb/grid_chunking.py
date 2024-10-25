import time
import nest_asyncio
from llama_index.core import VectorStoreIndex
from llama_index.core.evaluation import DatasetGenerator, FaithfulnessEvaluator, RelevancyEvaluator
from llama_index.llms.openai import OpenAI
from llama_index.readers.web import SimpleWebPageReader
import openai
import os
from dotenv import load_dotenv
load_dotenv()

nest_asyncio.apply()


openai.api_key = os.getenv('OPENAI_API_KEY')
llm = OpenAI(temperature=0, model="gpt-4o-mini")
faithfulness_gpt4 = FaithfulnessEvaluator(llm=llm)
relevancy_gpt4 = RelevancyEvaluator(llm=llm)

documents = SimpleWebPageReader(html_to_text=True).load_data(
    ["https://hotmart.com/pt-br/blog/como-funciona-hotmart"]
)
data_generator = DatasetGenerator.from_documents(documents)
eval_questions = data_generator.generate_questions_from_nodes()
eval_documents = documents[:20]

def evaluate_response_time_and_accuracy(chunk_size):
    total_response_time = 0
    total_faithfulness = 0
    total_relevancy = 0
    vector_index = VectorStoreIndex.from_documents(eval_documents,llm=llm,chunk_size=chunk_size)
    query_engine = vector_index.as_query_engine()
    num_questions = len(eval_questions)

    for question in eval_questions:
        start_time = time.time()
        response_vector = query_engine.query(question)
        elapsed_time = time.time() - start_time
        
        faithfulness_result = faithfulness_gpt4.evaluate_response(response=response_vector).passing
        relevancy_result = relevancy_gpt4.evaluate_response(query=question, response=response_vector).passing

        total_response_time += elapsed_time
        total_faithfulness += faithfulness_result
        total_relevancy += relevancy_result

    average_response_time = total_response_time / num_questions
    average_faithfulness = total_faithfulness / num_questions
    average_relevancy = total_relevancy / num_questions

    return average_response_time, average_faithfulness, average_relevancy

for chunk_size in [128, 256, 512, 1024, 2048]:
    avg_time, avg_faithfulness, avg_relevancy = evaluate_response_time_and_accuracy(chunk_size)
    print(f"Chunk size {chunk_size} - Average Response time: {avg_time:.2f}s, Average Faithfulness: {avg_faithfulness:.2f}, Average Relevancy: {avg_relevancy:.2f}")

