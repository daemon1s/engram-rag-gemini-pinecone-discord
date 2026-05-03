-- Tabla principal de notas
CREATE TABLE IF NOT EXISTS notas (
    id          SERIAL PRIMARY KEY,
    contenido   TEXT NOT NULL,
    tag         VARCHAR(100),           -- nombre del canal de discord (ej: 'proyectos', 'reflexiones')
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW(),
    pinecone_id VARCHAR(100),           -- id del vector en pinecone para sincronización
    discord_message_id VARCHAR(100)     -- id del mensaje en discord (solo referencia visual)
);

-- Índice para filtrado por tag
CREATE INDEX IF NOT EXISTS idx_notas_tag ON notas(tag);

-- Índice para filtrado temporal
CREATE INDEX IF NOT EXISTS idx_notas_created_at ON notas(created_at);
