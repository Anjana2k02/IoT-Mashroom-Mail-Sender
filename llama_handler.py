import os
import pandas as pd
from llama_index.core import (
    VectorStoreIndex, 
    Document, 
    Settings,
    StorageContext,
    load_index_from_storage
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from config import LLAMA_CONFIG, OPENAI_API_KEY

def initialize_llama():
    """Initialize LlamaIndex with OpenAI settings"""
    try:
        # Validate API key exists
        if not OPENAI_API_KEY or OPENAI_API_KEY == 'your-actual-api-key-here':
            raise ValueError("⚠️  Please add your OpenAI API key to config.py")
        
        # Set OpenAI API key (CORRECT WAY)
        os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        
        # Configure LLM (CORRECT WAY - accessing dictionary keys properly)
        Settings.llm = OpenAI(
            model=LLAMA_CONFIG['model_name'],      # Access by key name
            temperature=LLAMA_CONFIG['temperature'], # Access by key name
            max_tokens=LLAMA_CONFIG['max_tokens']   # Access by key name
        )
        
        # Configure embeddings
        Settings.embed_model = OpenAIEmbedding()
        
        print("✅ LlamaIndex initialized successfully!")
        print(f"📍 Using model: {LLAMA_CONFIG['model_name']}")
        
    except Exception as e:
        print(f"❌ Error initializing LlamaIndex: {e}")
        raise

def create_index_from_dataframe(df, text_column='description'):
    """
    Create a VectorStoreIndex from a pandas DataFrame
    
    Args:
        df: pandas DataFrame
        text_column: column name containing text to index
    
    Returns:
        VectorStoreIndex object
    """
    try:
        if df is None or df.empty:
            print("⚠️  DataFrame is empty!")
            return None
            
        print(f"\n🔄 Creating index from {len(df)} rows...")
        
        # Convert DataFrame rows to Document objects
        documents = []
        for idx, row in df.iterrows():
            # Build text content
            text_parts = []
            
            # Add main text column
            if text_column in row and pd.notna(row[text_column]):
                text_parts.append(f"{text_column}: {row[text_column]}")
            
            # Add other columns
            for col in df.columns:
                if col != text_column and pd.notna(row[col]):
                    text_parts.append(f"{col}: {row[col]}")
            
            if not text_parts:
                continue
            
            text = "\n".join(text_parts)
            
            # Add metadata
            metadata = {
                'row_index': idx,
                **{col: str(row[col]) for col in df.columns if pd.notna(row[col])}
            }
            
            doc = Document(
                text=text,
                metadata=metadata
            )
            documents.append(doc)
        
        if not documents:
            print("⚠️  No valid documents created")
            return None
        
        # Create index
        print("🔄 Building vector index...")
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        print(f"✅ Index created with {len(documents)} documents!")
        
        return index
    
    except Exception as e:
        print(f"❌ Error creating index: {e}")
        import traceback
        traceback.print_exc()
        return None

def query_index(index, query_text):
    """
    Query the index with a question
    
    Args:
        index: VectorStoreIndex object
        query_text: question to ask
    
    Returns:
        Response string
    """
    try:
        if index is None:
            print("❌ Index is None!")
            return None
            
        print(f"\n🔍 Question: {query_text}")
        query_engine = index.as_query_engine()
        response = query_engine.query(query_text)
        return str(response)
    
    except Exception as e:
        print(f"❌ Error querying index: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_index(index, persist_dir=None):
    """
    Save index to disk
    
    Args:
        index: VectorStoreIndex object
        persist_dir: directory to save index
    """
    try:
        if index is None:
            print("❌ Cannot save None index")
            return
            
        if persist_dir is None:
            persist_dir = LLAMA_CONFIG['index_storage_path']
        
        # Create directory if needed
        os.makedirs(persist_dir, exist_ok=True)
        
        index.storage_context.persist(persist_dir=persist_dir)
        print(f"💾 Index saved to: {os.path.abspath(persist_dir)}")
        
    except Exception as e:
        print(f"❌ Error saving index: {e}")

def load_index(persist_dir=None):
    """
    Load index from disk
    
    Args:
        persist_dir: directory where index is saved
    
    Returns:
        VectorStoreIndex object or None
    """
    try:
        if persist_dir is None:
            persist_dir = LLAMA_CONFIG['index_storage_path']
        
        if not os.path.exists(persist_dir):
            print(f"⚠️  Directory not found: {persist_dir}")
            return None
        
        print(f"📂 Loading index from: {persist_dir}")
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)
        print("✅ Index loaded successfully!")
        
        return index
    
    except Exception as e:
        print(f"❌ Error loading index: {e}")
        import traceback
        traceback.print_exc()
        return None