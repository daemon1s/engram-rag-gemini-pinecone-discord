import { Pinecone } from '@pinecone-database/pinecone';

const pc = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY || '',
});

export const pineconeIndex = pc.index(process.env.PINECONE_INDEX_NAME || 'engram-rag');

export async function upsertVector(id: string, values: number[], metadata: Record<string, any>) {
  await pineconeIndex.upsert({
    records: [
      {
        id: id.toString(),
        values: values,
        metadata: metadata
      }
    ]
  });
}

export async function deleteVector(id: string) {
  await pineconeIndex.deleteOne({ id: id.toString() });
}
