# Engram

Personal knowledge management system and Retrieval-Augmented Generation (RAG) assistant. It captures atomic notes through Discord, indexes vector embeddings via Google Gemini into Pinecone, stores structured records in PostgreSQL, and provides a Next.js management dashboard with bidirectional synchronization.

<br>

<p align="center">
  <a href="https://engram.daemonize.me" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Live_Demo-engram.daemonize.me-06B6D4?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Live Demo" />
  </a>
</p>

<br>

<p align="center">
  <video src="https://raw.githubusercontent.com/daemon1s/engram-rag-gemini-pinecone-discord/main/screenshots/engram.webm" width="100%" autoplay loop muted playsinline controls></video>
</p>

<p align="center">
  <img src="screenshots/dashboard.png" alt="Engram Dashboard" width="100%" />
</p>

## System Architecture

```
[Discord User] ---> [Discord Bot (Python)] <---> [PostgreSQL 16]
                           |                           ^
                           +---> [Gemini Embeddings]   |
                           |             |             |
                           +---> [Pinecone Vector DB]  |
                                         |             |
[Web User] ---------> [Next.js Dashboard] -------------+
                                 |
                                 +--- HTTP POST (sync) ---> [Bot aiohttp:5000]
```

### Core Pipelines

1. **Ingestion (Discord)**:
   - Command `/create` triggers a modal dialog for title and note content.
   - Generates a 768-dimensional embedding using `gemini-embedding-2` (Matryoshka representation with `RETRIEVAL_DOCUMENT` task type).
   - Upserts vector data into Pinecone and persists note content, category tags, and timestamps in PostgreSQL.
   - Posts a visual card in the target Discord channel and records `discord_message_id`.

2. **RAG Query Pipeline (Discord)**:
   - Command `/query [prompt]` embeds the user question with `RETRIEVAL_QUERY`.
   - Queries Pinecone via cosine similarity (`top_k=5`) to retrieve relevant vector IDs.
   - Fetches full note content from PostgreSQL using the matching IDs.
   - Assembles structured context and generates a grounded response using `gemini-3.1-flash-lite`.

3. **Dashboard Management & Bidirectional Sync**:
   - Next.js dashboard provides full-text search (`ILIKE` on titles, content, and tags), tag filtering, and note editing/deletion.
   - On note update or deletion via Server Actions, the dashboard updates PostgreSQL, refreshes Pinecone vectors, and sends an internal HTTP `POST` to the bot's aiohttp server (port 5000) to update or delete the Discord message in real time.

## Tech Stack

- **Bot**: Python 3.12, Discord.py 2, asyncpg, google-genai, pinecone-client, aiohttp, python-dotenv
- **Dashboard**: Next.js 16.2 (App Router), React 19, Tailwind CSS v4, Auth.js v5 (OAuth Discord), pg, Framer Motion
- **Storage**: PostgreSQL 16, Pinecone (Serverless)
- **Deployment**: Docker Compose

## Project Structure

```
secondbrain/
├── bot/
│   ├── commands/           # Slash command handlers (/create, /query, /edit, /pending)
│   ├── ui/                 # Discord modals and view components
│   └── main.py             # Bot initialization and aiohttp sync listener
├── core/
│   ├── embeddings.py       # Gemini embedding generation
│   ├── rag.py              # Context building and LLM prompting
│   ├── search.py           # Pinecone vector querying
│   └── notes.py            # PostgreSQL database operations
├── db/
│   ├── migrations/         # SQL schema initialization (01_init.sql)
│   └── connection.py       # asyncpg connection pooling
├── dashboard/
│   ├── src/
│   │   ├── app/            # Next.js pages (/dashboard, /login, /demo)
│   │   ├── components/     # UI cards, modals, and search bars
│   │   ├── lib/            # Server actions, pg pool, and Pinecone client
│   │   └── auth.ts         # Auth.js configuration and access whitelist
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── Dockerfile              # Bot container definition
```

## Local Setup

### Prerequisites
- Docker and Docker Compose
- Discord Bot Token and Guild ID
- Google Gemini API Key
- Pinecone API Key

### Configuration

Create a `.env` file in the root directory:

```env
# Discord
DISCORD_TOKEN=your_bot_token
DISCORD_GUILD_ID=your_guild_id

# PostgreSQL
POSTGRES_USER=engram_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=db_engram
POSTGRES_URL=postgresql://engram_user:your_db_password@postgres:5432/db_engram

# Pinecone & Gemini
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=engram-index
GEMINI_API_KEY=your_gemini_api_key

# Dashboard Auth
AUTH_SECRET=your_generated_auth_secret
AUTH_DISCORD_ID=your_discord_oauth_client_id
AUTH_DISCORD_SECRET=your_discord_oauth_client_secret
ALLOWED_EMAIL=your_email@example.com
```

### Running with Docker

```bash
docker compose up -d --build
```

Endpoints:
- Web Dashboard: `http://localhost:3000`
- PostgreSQL: `localhost:5432`
- Bot Sync Listener: `http://localhost:5000` (internal)
