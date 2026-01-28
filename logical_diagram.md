┌──────────────────────────────────────────┐
│              Frontend (Web)              │
│ Upload | Chat | Quizzes | Flashcards     │
│ Progress | Document Explorer             │
└──────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────┐
│               API Layer (FastAPI)        │
│ Auth | Upload | Query | Quiz | History   │
└──────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────┐
│        Orchestration Layer (LangGraph)   │
│ Intent Router: Ask | Quiz | Review       │
└──────────────────────────────────────────┘
         │                 │                  │
         ▼                 ▼                  ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────────┐
│   PageIndex    │ │ Relational DB  │ │  Memory Manager    │
│ Document Tree  │ │ Users & Logs   │ │ Short + Long Term  │
└────────────────┘ └────────────────┘ └────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│     Section-Based Retrieval Engine       │
│ Match Chapter → Section → Page Range     │
└──────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────┐
│        Prompt Builder (Grounded)         │
│ Inject Section Content + User Memory     │
└──────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────┐
│                 LLM API                  │
│ Answers | Summaries | Quizzes | Cards    │
└──────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────┐
│        Logging & Evaluation (Optional)   │
└──────────────────────────────────────────┘