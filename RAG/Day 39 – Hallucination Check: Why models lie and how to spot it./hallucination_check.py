import chromadb
import ollama
import re
client=chromadb.PersistentClient(path='/Users/chetanhirekurubar/Desktop/RagProjectDB')
collection=client.get_collection(name='chetan')
queries=[
    # "What is the boiling point of nitrogen?",
    "What is the refund policy for premium enterprise tier customers added in Q4 2024?"
    # "Summarize everything about our global expansion strategy."
    ]
for query in queries:
    results=collection.query(
        query_texts=query,
        n_results=3
    )
    context=''
    docs=results['documents'][0]
    for i,chunk in enumerate(docs):
        context+=f"Source {i+1} : {chunk} \n\n"
    context+=f"Source 4 : Premium enterprise tier customers added in Q4 2024 are eligible for a 60-day full refund, no questions asked. \n\n"
    # print(context)
    prompt=f'''
        "Answer only using the provided context. For every claim you make, you must cite the Source number inline. 
        If information is not in the context, respond with 'I don't know'."
        context={context}
        Question={query}
        Answer:
        '''
    response=ollama.chat(
        model='qwen3:4b',
        messages=[
            {

                'role':'user',
                'content':prompt
            }
        ]
    )
    llm_response=response['message']['content']
    print(llm_response)

    #Extract cited source number
    citation_match=re.search(r"Source\s*(\d+)",llm_response)
    if not citation_match:
        print("No Citation Found")
        exit()
    source_number=int(citation_match.group(1))
    print("Cited Source : ",source_number)

    #Extract claim text
    claim_text=llm_response.split("Source")[0].strip().lower()
    print("\nClaim Text : ")
    print(claim_text)

    #Get actual retrieved chunks
    chunks=results['documents'][0]
    if source_number>len(chunks):
        print("invalid source number")
        exit()

    keywords = ["refund", "enterprise", "Q4 2024", "60-day"]
    source_text=[kw for kw in keywords if kw.lower() in source_text]
