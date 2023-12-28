import os
import json
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from angle_emb import AnglE, Prompts
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("C:\\Users\\saimu\\OneDrive\\Desktop\\coding\\models\\llama7b-chat-hf")



def read_quality_dataset(quality_json_file):
    with open(quality_json_file,'r') as f:
        data=json.load(f)
    article_id=[]
    article=[]
    questions=[]
    return article_id,article,questions

class basic_retriever():

    def __init__(self,text):
        self.passage=text
    def splitting_text(self,chunk_size=200,chunk_overlap=40):
        self.chunk_overlap=chunk_overlap
        self.chunk_size=chunk_size
        self.angle= AnglE.from_pretrained("C:\\Users\\saimu\\OneDrive\\Desktop\\coding\\models\\angel", pooling_strategy='cls').cuda()
        self.angle.set_prompt(prompt=Prompts.C)
        splitter=RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            tokenizer,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        splitted_docs=splitter.split_text(self.passage)
        self.docs=[]
        self.embeddings=[]
        id=1
        for doc in splitted_docs:
            self.docs.append(Document(page_content=doc,metadata={"id":id}))
            embed= self.angle.encode({'text': doc}, to_numpy=True)[0]
            self.embeddings.append(embed)
            id+=1
    
    def set(self,text):
        self.passage=text
        self.splitting_text(self.chunk_size,self.chunk_overlap)
    
    def retrieval_question_only(self,question,top_k):
        query_encoding=self.angle.encode({'text':question},to_numpy=True)[0]
        scores=[]
        for embed in self.embeddings:
            score=((np.dot(embed,query_encoding))/(np.linalg.norm(embed)*np.linalg.norm(query_encoding)))
            scores.append(score)
        scores_index=np.argsort(scores)[::-1]
        retrieved_docs=[]
        for index in scores_index[:top_k]:
           document=self.docs[index]
           score=scores[index]
           retrieved_docs.append({"document":document.page_content,"score":score})
        return retrieved_docs


        
