import chromadb
import ollama

#Step 2A : DB connection is heavy & Should initialize once & Query many times
client = chromadb.PersistentClient(path='/Users/chetanhirekurubar/Desktop/RagProjectDB')
collection = client.get_collection(name='chetan')

#STEP 1: Take User Query Input & STEP 7: Test With Multiple Queries
while True:
    query=input("Ank any questions..! : ").strip().lower()
    # print('You Asked  : ',query)
    if query in ['exit','bye']:
        break
    #STEP 2B : Retrieve Top-K Chunks from ChromaDB
    results=collection.query(
        query_texts=[query],
        n_results=3,
    )
    # print(results)

    #STEP 3: Extract and Construct a Structured Context String
    context=''
    docs=results['documents'][0]
    for i,chunk in enumerate(docs):
        context +=f"Source {i+1} : {chunk} \n\n"
    # print(context)

    #STEP 4: Build a RAG Prompt Template
    prompt=f'''
    You are a helpful assistant. Answer only using this provided context.
    If Answer is not in context, Say "I Don't Know" .
    Context : {context}
    Question : {query}
    Answer :
    '''

    #STEP 5: Send Prompt to LLM
    response=ollama.chat(
        model='deepseek-coder:6.7b',
        messages=[
            {
                'role':'user',
                'content':prompt
            }
        ]
    )
    print(response['message']['content'])
    # print(response)

    #STEP 6: Add Citation Format at the End
    # print("--- Sources ---")
    # print(results['metadatas'][0])
    # for i, metadata in enumerate(results['metadatas'][0]):
    #     print(f"[Source {i+1}]: page {metadata['source']}")

