1. Copy `.env.example` -> `.env`, fill values (OpenAI & Pinecone & MySQL creds).
2. Start with docker-compose:
   docker compose up --build
   This will launch MySQL and the Flask web app at http://localhost:5000

3. Ingest KB:
   - Prepare knowledge.csv with columns id,text
   - Exec into container or run locally:
     python ingest_kb.py --csv knowledge.csv

4. Visit:
   - Frontend: http://localhost:5000/
   - Admin: http://localhost:5000/admin/
