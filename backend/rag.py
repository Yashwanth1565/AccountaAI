"""
==========================================================
AccountaAI - Retrieval Augmented Generation (RAG)
----------------------------------------------------------
Stores meeting transcripts and answers questions
using ChromaDB + Gemini.
==========================================================
"""

import chromadb

from google import genai
from sentence_transformers import SentenceTransformer

from backend.config import GOOGLE_API_KEY
from backend.config import CHROMA_DB_DIR
from backend.config import CHROMA_COLLECTION
from backend.config import EMBEDDING_MODEL


class RAG:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DB_DIR)
        )   
        self.collection = self.client.get_or_create_collection(
            CHROMA_COLLECTION
        )
        self.embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        self.gemini = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        print("RAG Initialized Successfully!")

    # ----------------------------------------------------

    def add_meeting(
        self,
        meeting_id,
        transcript
    ):

        embedding = self.embedding_model.encode(
            transcript
        ).tolist()

        self.collection.upsert(
            ids=[str(meeting_id)],
            documents=[transcript],
            embeddings=[embedding]
        )

    # ----------------------------------------------------

    def ask(self, question):

        embedding = self.embedding_model.encode(
            question
        ).tolist()

        results = self.collection.query(

            query_embeddings=[embedding],

            n_results=3

        )

        documents = results["documents"][0]

        if len(documents) == 0:
            return "No previous meeting found."

        context = "\n\n".join(documents)

        prompt = f"""
You are an AI Meeting Assistant.

Answer ONLY using the meeting context below.

Meeting Context:

{context}

Question:

{question}

If the answer is unavailable,
say "Not discussed in previous meetings."
"""

        response = self.gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text


rag = RAG()