from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os


class Groq:
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            temperature=0.7, groq_api_key=api_key, model="llama2-70b-4096"
        )
        
        # Initialize embeddings and vector store
        self.embeddings = HuggingFaceEmbeddings()
        self.vector_store = None
        self.initialize_knowledge_base()
        
        # Define career advice prompt template with RAG context
        self.career_template = """You are a career advisor chatbot. Use the following relevant context 
        and the user's input to provide helpful career advice.

        Context: {context}

        User Input: {user_input}

        Please provide career advice addressing the above input. Include:
        1. Direct answers to their questions, incorporating relevant context
        2. Practical next steps they can take
        3. Relevant resources or tools they might find helpful
        4. Words of encouragement

        Career Advice:"""

        self.prompt = PromptTemplate(
            input_variables=["context", "user_input"],
            template=self.career_template
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def initialize_knowledge_base(self):
        """Initialize the vector store with career-related documents"""
        # Path to career resources directory
        resources_dir = "career_resources"
        
        if os.path.exists(resources_dir):
            documents = []
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            
            # Load and process documents
            for filename in os.listdir(resources_dir):
                if filename.endswith('.txt'):
                    with open(os.path.join(resources_dir, filename), 'r') as f:
                        text = f.read()
                        chunks = text_splitter.split_text(text)
                        documents.extend(chunks)
            
            # Create vector store
            if documents:
                self.vector_store = FAISS.from_texts(documents, self.embeddings)
    
    def get_relevant_context(self, query: str, k: int = 3) -> str:
        """Retrieve relevant context from the vector store"""
        if self.vector_store is None:
            return ""
        
        docs = self.vector_store.similarity_search(query, k=k)
        return "\n".join(doc.page_content for doc in docs)
        
    def get_career_advice(self, user_input: str) -> str:
        """
        Generate career advice based on user input and relevant context
        """
        try:
            # Get relevant context from the knowledge base
            context = self.get_relevant_context(user_input)
            
            # Generate response using the LLM chain
            response = self.chain.run(
                context=context,
                user_input=user_input
            )
            return response
        except Exception as e:
            return f"Error generating advice: {str(e)}"
