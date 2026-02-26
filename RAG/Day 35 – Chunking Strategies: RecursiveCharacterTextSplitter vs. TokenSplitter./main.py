#Step 1: Environment Setup & Imports
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Step 2: Loading Your Text (random paragraph with each para have ending with '\n\n' its represent para ends)
sample_text="""ChatGPT
ChatGPT is an AI assistant developed by OpenAI designed for conversation, coding, learning, and problem-solving.
It uses large language models to understand context and generate human-like responses.
It is widely used for education, software development, and productivity tasks.
\n\n
Gemini
Gemini is Google’s multimodal AI model built to work across text, images, code, and reasoning tasks.
It integrates deeply with Google products like Search, Docs, and Android ecosystems.
Its strength lies in real-time information access and large-scale reasoning capabilities.
\n\n
Anthropic (Claude)
Anthropic develops Claude, an AI assistant focused on safety, alignment, and reliable reasoning.
Claude is designed to follow instructions carefully and produce structured, thoughtful responses.
It is commonly used for long-document analysis, writing, and enterprise workflows.
\n\n
Perplexity
Perplexity is an AI search assistant that combines language models with live web retrieval.
It focuses on answering questions with sources and citations for verification.
Users often use it as an AI-powered alternative to traditional search engines.\n\n
"""
#Step 3: Creating the Splitter
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=15
)

# Step 4: Splitting the Text
chunks=text_splitter.split_text(sample_text)

#Step 5: Print Number of Chunks
# print(len(chunks))

#Step 6: Inspect First Chunk
# print(chunks[0])

#Step 7: Inspect All Chunks
# for i,chunk in enumerate(chunks):
#     print("Chunk ",i," ",chunk)

#Step 8: Adding Metadata to Chunks
chunks_with_metadata=[]
for i,chunk in enumerate(chunks):
    chunks_with_metadata.append({"text":chunk,"source":"Sample_doc","chunk_id":i})

#Step 9: Print First Item from Metadata List
# print(chunks_with_metadata[0])

#Step 10: Compare Different Chunk Sizes
# small_text_splitter=RecursiveCharacterTextSplitter(
#     chunk_size=50,
#     chunk_overlap=10
# )
# small_chunks=small_text_splitter.split_text(sample_text)

# large_text_splitter=RecursiveCharacterTextSplitter(
#     chunk_size=300,
#     chunk_overlap=50
# )
# large_chunks=large_text_splitter.split_text(sample_text)

#Step 11: Compare Chunk Counts
# print("Small Chunks : ",len(small_chunks))
# print("Medium Chunks : ",len(chunks))
# print("Large Chunks : ",len(large_chunks))

#Step 12:Prepare Chunks for Embedding(In the embedding stage, the model only needs plain text strings not dictionaries)
texts_for_embedding=[item["text"] for item in chunks_with_metadata]
print(texts_for_embedding)