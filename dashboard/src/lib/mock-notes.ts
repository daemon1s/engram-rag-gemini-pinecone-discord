import { Note } from "@/types/note";

export const mockNotes: Note[] = [
  {
    id: 125,
    titulo: "Arquitectura de engram: decisiones iniciales",
    contenido: `## Objetivo

Un segundo cerebro consultable por lenguaje natural. La idea central es dejar de reexplicar contexto personal a cada modelo nuevo.

## Decisiones

- Pinecone para vectores y PostgreSQL para el texto plano
- Gemini para embeddings y consultas
- El servidor de Discord como log visual, no como fuente de verdad

## Aprendizaje

Separar la ingesta del consumo: el bot solo escribe, la API solo lee.`,
    tag: "proyectos",
    created_at: "2026-07-28T14:32:11.000Z",
    updated_at: "2026-07-28T14:32:11.000Z",
  },
  {
    id: 124,
    titulo: "Roadmap del dashboard web",
    contenido: `## Fase actual

- CRUD completo de notas
- Búsqueda semántica
- Autenticación con Discord

## Siguiente

- Filtros por rango de fechas
- Exportar notas en markdown
- Vistas por calendario`,
    tag: "proyectos",
    created_at: "2026-07-21T09:15:40.000Z",
    updated_at: "2026-07-21T09:15:40.000Z",
  },
  {
    id: 123,
    titulo: "Rust: primera semana",
    contenido: `## Impresiones

- El compilador es estricto pero los mensajes de error son excelentes
- El modelo de ownership cuesta al principio

## Mini proyecto

Un CLI que parsea archivos de configuración para practicar enums y pattern matching.`,
    tag: "aprendizaje",
    created_at: "2026-07-11T18:47:02.000Z",
    updated_at: "2026-07-11T18:47:02.000Z",
  },
  {
    id: 122,
    titulo: "Resumen: El hombre en busca de sentido",
    contenido: `## Ideas clave

- La búsqueda de sentido sostiene al ser humano incluso en el sufrimiento extremo
- La libertad interior no se puede arrebatar

## Aplicación

- Tener un "por qué" claro para cada proyecto personal
- El propósito vale más que la motivación`,
    tag: "lecturas",
    created_at: "2026-06-30T12:05:33.000Z",
    updated_at: "2026-06-30T12:05:33.000Z",
  },
  {
    id: 121,
    titulo: "Micro-saas de hábitos",
    contenido: `## Concepto

Una app donde cada hábito es un "experimento" con duración definida y métricas propias.

## Por qué

- Los hábitos con fecha de fin se mantienen mejor
- La gamificación tradicional aburre

## Riesgo

Mercado saturado. Diferenciador: enfoque en experimentación, no en rachas.`,
    tag: "ideas",
    created_at: "2026-06-18T20:21:54.000Z",
    updated_at: "2026-06-18T20:21:54.000Z",
  },
  {
    id: 120,
    titulo: "Revisión de mañana (10 minutos)",
    contenido: `1. Revisar notas de ayer y la cola de pendientes
2. Elegir la tarea más importante del día
3. Escribir una línea sobre el objetivo diario

Regla: antes de abrir cualquier red social, cerrar la revisión.`,
    tag: "rutina",
    created_at: "2026-06-02T08:40:19.000Z",
    updated_at: "2026-06-02T08:40:19.000Z",
  },
  {
    id: 119,
    titulo: "Café de especialidad: notas de cata",
    contenido: `## Perfil actual

- Origen: Colombia, Huila
- Notas: caramelo, naranja y chocolate con leche
- Molienda media, método V60, ratio 1:16

## Pendiente

Probar un proceso natural de Etiopía para comparar acidez.`,
    tag: "consumo",
    created_at: "2026-05-24T16:12:48.000Z",
    updated_at: "2026-05-24T16:12:48.000Z",
  },
  {
    id: 118,
    titulo: "Entrenamiento: ciclo de fuerza",
    contenido: `## Semana 1-4

- Fuerza base: sentadilla, press banca, remo
- 3 series x 5 repeticiones al 80% de la carga máxima
- Dos sesiones de movilidad entre medio

## Regla

Subir carga solo si la técnica del último set fue limpia.`,
    tag: "salud",
    created_at: "2026-05-13T11:29:07.000Z",
    updated_at: "2026-05-13T11:29:07.000Z",
  },
  {
    id: 117,
    titulo: "Presupuesto mensual",
    contenido: `## Distribución

- Vivienda: 30%
- Ahorro e inversión: 20%
- Alimentación: 15%
- Ocio y consumo: 10%
- Resto: flexible

## Automatización

- Día 1 del mes: transferencia de ahorro automática
- Revisar suscripciones cada trimestre`,
    tag: "finanzas",
    created_at: "2026-04-30T19:03:26.000Z",
    updated_at: "2026-04-30T19:03:26.000Z",
  },
  {
    id: 116,
    titulo: "Tailwind v4 y CSS moderno",
    contenido: `## Notas

- Las utilidades componen mejor que los componentes "atomizados"
- Container queries resuelven el responsive sin breakpoints intermedios

## Idea

Migrar los componentes del dashboard a container queries para simplificar estilos.`,
    tag: "aprendizaje",
    created_at: "2026-04-15T07:58:13.000Z",
    updated_at: "2026-04-15T07:58:13.000Z",
  },
  {
    id: 115,
    titulo: "Sobre la atención",
    contenido: `La atención es el recurso más caro del día. Cada notificación bien diseñada es una pequeña deuda contra la concentración.

Regla personal: una sola pestaña de investigación abierta por tarea.`,
    tag: "reflexiones",
    created_at: "2026-03-29T15:44:36.000Z",
    updated_at: "2026-03-29T15:44:36.000Z",
  },
  {
    id: 114,
    titulo: "Podcast sobre diseño de software",
    contenido: `## Concepto

Charlas de 30 minutos con personas de distintos rubros sobre cómo piensan al resolver problemas.

## Formato

- Un problema concreto por episodio
- La invitada explica cómo lo atacaría
- Cierre con lección aplicable al software

## Nombre tentativo

"Problemas bien planteados"`,
    tag: "ideas",
    created_at: "2026-03-12T10:26:51.000Z",
    updated_at: "2026-03-12T10:26:51.000Z",
  },
  {
    id: 113,
    titulo: "Santiago: fin de semana",
    contenido: `## Itinerario tentativo

- Viernes: cerro San Cristóbal al atardecer
- Sábado: bodega de Casablanca
- Domingo: walk por Barrio Lastarria

## Logística

- Bus ida y vuelta, airbnb cerca de la plaza`,
    tag: "viajes",
    created_at: "2026-02-25T17:38:22.000Z",
    updated_at: "2026-02-25T17:38:22.000Z",
  },
  {
    id: 112,
    titulo: "Pipeline de embeddings: flujo completo",
    contenido: `## Flujo

1. Texto de la nota
2. Gemini embedding con recorte Matryoshka a 768 dimensiones
3. Vector en Pinecone con metadata mínima
4. pinecone_id en PostgreSQL para sincronización

## Lección

No saturar Pinecone con texto: los vectores viven separados del contenido real.`,
    tag: "proyectos",
    created_at: "2026-02-08T13:51:09.000Z",
    updated_at: "2026-02-08T13:51:09.000Z",
  },
];
