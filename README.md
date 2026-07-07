# engram

<p align="center">
  <img src="./dashboard/public/logo.png" alt="engram logo" width="150">
</p>

<p align="center">
  <b>Segundo cerebro personal con RAG, Discord y panel de administración</b>
</p>

<p align="center">
  <a href="https://github.com/daemon1s/engram-rag-gemini-pinecone-discord/actions">
    <img src="https://github.com/daemon1s/engram-rag-gemini-pinecone-discord/actions/workflows/deploy.yml/badge.svg" alt="Compilación y despliegue de engram">
  </a>
  <img src="https://img.shields.io/badge/Next.js-15-black?style=flat&logo=nextdotjs&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?style=flat&logo=tailwindcss&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Discord.py-v2-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord.py">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Pinecone-Vector_DB-000000?style=flat&logo=pinecone&logoColor=white" alt="Pinecone">
  <img src="https://img.shields.io/badge/Gemini_API-Google_Cloud-1A73E8?style=flat&logo=googlegemini&logoColor=white" alt="Gemini API">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Nginx_Proxy_Manager-Proxy-009639?style=flat&logo=nginx&logoColor=white" alt="Nginx Proxy Manager">
</p>

Sistema RAG (Retrieval-Augmented Generation) personal diseñado para funcionar como un segundo cerebro. Permite almacenar, gestionar y consultar información personal en lenguaje natural a través de un bot de Discord y un panel web de administración (dashboard), evitando la necesidad de reexplicar contexto a modelos de lenguaje en cada nueva sesión.

## Diagrama de despliegue

![Diagrama de despliegue](./docs/engram_diagramadespliegue.png)

---

## Arquitectura del sistema

El sistema está compuesto por cuatro componentes principales que se ejecutan de manera integrada en un entorno virtualizado con Docker:

### Componentes principales

1. **Bot de Discord (ingesta y consultas):** desarrollado en Python (`discord.py`). Actúa como la interfaz de usuario conversacional primaria. Permite registrar notas mediante comandos de barra (`/create`), editar o eliminar notas existentes, y realizar búsquedas semánticas (`/query`). Adicionalmente, expone un servidor HTTP interno (`aiohttp`) en el puerto 5000 para recibir eventos de sincronización del panel web.
2. **Dashboard web:** desarrollado con Next.js 15, Tailwind v4 y Auth.js v5. Proporciona una interfaz visual ("Vision UI") para buscar, filtrar, editar y eliminar notas directamente desde el navegador. La autenticación está restringida a un correo electrónico específico mediante sesión local segura con proveedor de Discord.
3. **Base de datos relacional (PostgreSQL):** almacena la información estructurada en texto plano, incluyendo títulos, contenidos, categorías (tags extraídos del canal de Discord), fechas de creación/actualización, identificadores de mensajes en Discord e identificadores vectoriales de Pinecone.
4. **Base de datos vectorial (Pinecone):** almacena los vectores de embeddings de 768 dimensiones generados con el modelo `gemini-embedding-2` utilizando técnicas de Matryoshka learning. Solo almacena los vectores y metadatos básicos (id, categoría y fecha) para proteger la privacidad de la información textual y reducir el consumo de memoria RAM del servidor VPS.

---

## Flujo de funcionamiento

### 1. Ingesta y gestión de notas
* **Desde Discord:** al ejecutar `/create`, el bot registra la nota en la base de datos PostgreSQL, genera el embedding utilizando la API de Gemini, almacena el vector resultante en Pinecone y publica una tarjeta visual fija (sticky note) en el canal correspondiente de Discord guardando su `message_id`.
* **Desde el dashboard:** al editar o eliminar una nota, Next.js actualiza la base de datos local, sincroniza los vectores en Pinecone y realiza una petición HTTP interna (`POST`) al puerto 5000 del bot. Esto permite que el bot actualice o elimine instantáneamente el mensaje de Discord respectivo.

### 2. Consultas y generación aumentada (RAG)
* Al ejecutar `/query [pregunta]` en Discord, el sistema genera el embedding de la pregunta mediante la API de Gemini.
* Realiza una búsqueda de similitud de coseno en el índice de Pinecone para recuperar los metadatos de las notas más relevantes.
* Recupera el contenido textual de dichas notas desde PostgreSQL utilizando los identificadores devueltos por la búsqueda vectorial.
* Envía la pregunta junto con el contexto estructurado al modelo `gemini-3.1-flash-lite-preview` para generar una respuesta precisa y contextualizada.

---

## Esquema de base de datos

La base de datos relacional utiliza la siguiente estructura en PostgreSQL:

```sql
-- Tabla principal de notas
CREATE TABLE notas (
    id          SERIAL PRIMARY KEY,
    titulo      VARCHAR(255) NOT NULL,
    contenido   TEXT NOT NULL,
    tag         VARCHAR(100),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW(),
    pinecone_id VARCHAR(100),
    discord_message_id VARCHAR(100)
);

-- Índices para optimización de consultas
CREATE INDEX idx_notas_tag ON notas(tag);
CREATE INDEX idx_notas_created_at ON notas(created_at);
```

---

## Configuración del entorno

Para inicializar el proyecto es necesario crear un archivo `.env` en la raíz del repositorio basándose en `.env.example`:

```bash
# Discord
DISCORD_TOKEN=tu_token_de_bot
DISCORD_GUILD_ID=tu_guild_id

# PostgreSQL
POSTGRES_URL=postgresql://engram_user:engram_password@postgres:5432/db_engram

# Pinecone
PINECONE_API_KEY=tu_api_key_de_pinecone
PINECONE_INDEX_NAME=engram-index

# Gemini API
GEMINI_API_KEY=tu_api_key_de_gemini

# Dashboard Auth
ALLOWED_EMAIL=tu_correo@dominio.com
AUTH_SECRET=tu_secreto_de_autenticacion
```

---

## Estructura del proyecto

El repositorio está organizado de la siguiente manera:

```text
.
├── .github/workflows/   # Flujos de CI/CD (deploy.yml)
├── bot/                 # Código del bot de Discord (discord.py)
│   ├── commands/        # Comandos slash (create, edit_delete, query, pending)
│   ├── ui/              # Componentes de UI de Discord (modales, botones)
│   └── main.py          # Punto de entrada del bot
├── core/                # Lógica del motor RAG
│   ├── notes.py         # Operaciones CRUD en PostgreSQL
│   ├── embeddings.py    # Generación y normalización de embeddings
│   ├── rag.py           # Generación de respuestas con contexto de Gemini
│   └── search.py        # Algoritmos de búsqueda en Pinecone
├── dashboard/           # Panel web de administración (Next.js 15)
│   ├── src/app/         # Rutas, acciones de servidor y layouts
│   └── src/components/  # Componentes visuales bajo la estética Vision UI
├── db/                  # Gestión de la base de datos
│   ├── connection.py    # Pool de conexiones asíncronas con asyncpg
│   └── migrations/      # Scripts SQL para inicialización y parches
├── services/            # Clientes y wrappers de APIs de terceros
│   ├── gemini_client.py # Cliente oficial de Google GenAI
│   └── pinecone_client.py # Cliente de base de datos vectorial Pinecone
├── docker-compose.yml   # Orquestación de contenedores locales y producción
├── Dockerfile           # Receta de compilación para el bot y core
└── requirements.txt     # Dependencias de Python
```

---

## Comandos del bot de Discord

El bot interactúa mediante comandos de barra (slash commands) que se mapean automáticamente en el servidor:

| Comando | Descripción |
| :--- | :--- |
| `/create [contenido]` | Registra una nota nueva en la base de datos y genera su vector. La publica de forma visual en el canal. |
| `/edit [id]` | Abre un cuadro de diálogo modal pre-rellenado para editar el título y contenido de una nota existente. |
| `/delete [id]` | Elimina de forma atómica la nota de PostgreSQL, su mensaje en Discord y su vector en Pinecone. |
| `/query [pregunta]` | Realiza una búsqueda semántica de las notas relevantes y genera una respuesta contextualizada. |
| `/pending` | Interfaz interactiva y paginada para sincronizar o eliminar notas que fallaron por red o límites de API. |

---

## Seguridad y privacidad de datos

El diseño de la arquitectura implementa medidas estrictas de privacidad y seguridad:
* **Aislamiento de texto sensible:** la base de datos vectorial Pinecone solo almacena los identificadores de la nota, la categoría y el vector matemático de 768 números flotantes. El texto en plano y contenido sensible de las notas jamás sale del servidor local VPS ni se envía a servicios vectoriales externos.
* **Acceso restringido al dashboard:** la autenticación en el panel web de Next.js está protegida a nivel de servidor (Server Actions) y restringe el acceso únicamente al correo electrónico configurado en `ALLOWED_EMAIL` mediante el proveedor de Discord.
* **Mitigación de fugas en Discord:** los mensajes de error, estados de carga y ventanas interactivas del bot se eliminan automáticamente del canal después de 30 segundos (auto-prune) para mantener la limpieza visual y evitar la exposición pública de logs.
* **Puerto Postgres seguro:** en la configuración de Docker, la base de datos PostgreSQL está expuesta únicamente a la interfaz de loopback local (`127.0.0.1:5432`), impidiendo accesos no autorizados desde la red pública del VPS.

---

## Integración continua y despliegue (CI/CD)

El proyecto cuenta con un pipeline de automatización en GitHub Actions detallado en `.github/workflows/deploy.yml` que se ejecuta tras cada confirmación en la rama `main`:
El flujo de despliegue automático consta de dos etapas principales:

1. **Compilación y empaquetado (build-and-push):**
   * Se ejecuta en un entorno virtualizado de GitHub Actions al detectar un cambio en la rama `main`.
   * Compila las imágenes de Docker para el bot (`Dockerfile` en la raíz) y para el panel web (`Dockerfile` en `/dashboard`).
   * Sube ambas imágenes con la etiqueta `:latest` a Docker Hub utilizando credenciales almacenadas de manera segura.

2. **Despliegue automático en el servidor VPS:**
   * Una vez compiladas las imágenes, GitHub Actions inicia una conexión SSH segura con el servidor VPS.
   * Ejecuta comandos en el servidor para actualizar el código del repositorio (`git fetch` y `git reset`), descargar las nuevas versiones de las imágenes desde Docker Hub (`docker compose pull`), recrear los servicios en segundo plano (`docker compose up -d --wait`) y realizar una limpieza de imágenes en desuso (`docker image prune`) para optimizar el espacio en disco.

### Ejecución del entorno de producción y local

Para desplegar localmente el entorno completo (incluyendo la base de datos Postgres local, el bot y el dashboard):

```bash
docker-compose up -d --build
```

