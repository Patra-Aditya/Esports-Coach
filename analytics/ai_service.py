import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from django.conf import settings

# Initialize Chroma directory in the project root
CHROMA_PERSIST_DIR = os.path.join(settings.BASE_DIR, "chroma_db")

def get_llm():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.7)

def get_embeddings():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2", google_api_key=api_key)

def ingest_strategy_document(title, content):
    """
    Ingest a new strategy document into the local Chroma vector store.
    """
    embeddings = get_embeddings()
    if not embeddings:
        return False
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.create_documents([content], metadatas=[{"title": title}])
    
    vectorstore = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)
    vectorstore.add_documents(docs)
    return True

def get_coaching_feedback(user_stats, query):
    """
    Provide AI coaching based on user stats and strategy DB.
    """
    llm = get_llm()
    embeddings = get_embeddings()
    if not llm or not embeddings:
        return "System Warning: Google API Key is not set. The AI Coach cannot provide feedback."
        
    vectorstore = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)
    
    # Retrieve relevant strategies based on the query
    retrieved_docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    prompt = PromptTemplate(
        input_variables=["context", "stats", "query"],
        template="""
        You are a high-level competitive esports AI coach. 
        Your goal is to provide actionable, encouraging, and highly specific advice based on the user's recent performance stats and advanced strategies.
        
        Advanced Strategies Context:
        {context}
        
        User's Recent Stats:
        {stats}
        
        User's Query / Current Focus:
        {query}
        
        Provide natural-language coaching feedback to help the player push to higher ranks. Be concise but impactful.
        """
    )
    
    chain = prompt | llm
    response = chain.invoke({
        "context": context if context else "No specific strategies found, use general game knowledge.",
        "stats": user_stats,
        "query": query
    })
    
    return response.content
