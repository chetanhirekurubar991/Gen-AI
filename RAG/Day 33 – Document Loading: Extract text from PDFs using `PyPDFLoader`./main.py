#Step 1: Install Required Libraries & Step 2: Load a PDF Using PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
loaders=PyPDFLoader("//Users/chetanhirekurubar/Desktop/RAGTestFiles/test_document.pdf")
docs=loaders.load()
# print(type(docs))
# print(len(docs))

print(docs)

#Step 3: Inspect Document Structure
# first_doc=docs[0]
# print(type(first_doc))
# print(first_doc.page_content)
# print(first_doc.metadata)

#Step 4: Extract Page Content and Metadata Separately
# for i,doc in enumerate(docs):
#     print(f'----- Page {i+1} -----')
#     print("Content : ",doc.page_content)
#     print("Page Number : ",doc.metadata["page"]+1)
#     print("Source : ",doc.metadata["source"])

#Step 5: Handle Multi-Page PDF
# print(f"Total Pages Loaded : {len(docs)}")
# for doc in docs:
#     print(f"Page {doc.metadata['page']+1} | Characters : {len(doc.page_content)}")

#Step 6: Attach Custom Metadata
for doc in docs:
    doc.metadata["ingestion_time"]=datetime.now().isoformat()
    doc.metadata["category"]="Policy"
    doc.metadata["version"]="v1"
    doc.metadata["page_number"]=doc.metadata["page"]+1
print(docs[0].metadata)

#Step 7: Verify Text Quality
# quality_passed=[]
# quality_failed=[]
# for doc in docs:
#     content=doc.page_content.strip()
#     if len(content)<20:   # set a minimum character threshold
#         quality_failed.append(doc)
#     else:
#         quality_passed.append(doc)
# print("Passed : ",len(quality_passed))
# print("Failed/Flagged",len(quality_failed))

#Step 8: Prepare Final Output for Chunking Stage
#if you want to run Step 8 its also run in "Step 6" without "Step 6" its shows error (not executed)
try:
    def prepare_for_chunking(docs):
        output=[]
        for doc in docs:
            output.append({
                "content":doc.page_content,
                "metadata":{
                    "source":doc.metadata["source"],
                    "page_number":doc.metadata["page_number"],
                    "category":doc.metadata["category"],
                    "ingestion_time":doc.metadata["ingestion_time"],
                    "version":doc.metadata["version"]
                }
            })
        return output
    result=prepare_for_chunking(docs)
    print("Total docs ready for chunking : ",len(result))
    print("First doc preview : ",result[0])
except KeyError:
    print("Problem : Check 'Step 6' is not a comment because step 6 is added key to docs variable")
except Exception as e:
    print("Error : ",e)