export interface Note {
  id: number;
  titulo: string;
  contenido: string;
  tag: string;
  created_at: string;
  updated_at: string;
  pinecone_id?: string;
  discord_message_id?: string;
}
