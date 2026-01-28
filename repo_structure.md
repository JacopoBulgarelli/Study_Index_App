### Repo structure
studyindex/
├── backend/
├── frontend/
├── infra/
├── docs/
├── scripts/
└── README.md

### Backend structure
backend/
├── app/
│   ├── main.py                    # FastAPI entrypoint
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── upload.py
│   │   │   ├── query.py
│   │   │   ├── quiz.py
│   │   │   ├── flashcards.py
│   │   │   └── history.py
│   │   └── dependencies.py
│   │
│   ├── ingestion/
│   │   ├── pageindex_loader.py     # PageIndex integration
│   │   ├── structure_parser.py     # Chapters/sections/pages
│   │   └── section_store.py        # Store in DB
│   │
│   ├── retrieval/
│   │   ├── section_matcher.py      # Match query → section
│   │   ├── hierarchy_search.py     # Navigate tree
│   │   └── context_builder.py      # Build grounded context
│   │
│   ├── orchestration/
│   │   ├── graph.py                # LangGraph state machine
│   │   ├── state.py                # TypedDict schema
│   │   └── nodes/
│   │       ├── detect_intent.py
│   │       ├── retrieve_section.py
│   │       ├── generate_answer.py
│   │       ├── generate_quiz.py
│   │       ├── generate_flashcards.py
│   │       └── update_memory.py
│   │
│   ├── memory/
│   │   ├── session_memory.py       # Short-term context
│   │   ├── long_term_memory.py     # User history DB
│   │   ├── weakness_tracker.py     # Weak topic detection
│   │   └── recall_engine.py        # Topic recall logic
│   │
│   ├── db/
│   │   ├── models.py               # SQLAlchemy models
│   │   ├── session.py
│   │   └── migrations/
│   │
│   ├── llm/
│   │   ├── client.py
│   │   └── prompt_templates.py
│   │
│   ├── evaluation/
│   │   ├── logging.py
│   │   └── metrics.py              # Optional quality scoring
│   │
│   └── utils/
│       ├── text.py
│       ├── matching.py
│       └── validators.py
│
├── tests/
│   ├── test_retrieval.py
│   ├── test_memory.py
│   └── test_api.py
│
├── requirements.txt
└── Dockerfile

### Frontend structure
frontend/
├── src/
│   ├── pages/
│   │   ├── Upload.tsx
│   │   ├── Library.tsx
│   │   ├── Chat.tsx
│   │   ├── Quiz.tsx
│   │   ├── Flashcards.tsx
│   │   └── Dashboard.tsx
│   │
│   ├── components/
│   │   ├── DocumentOutline.tsx
│   │   ├── SectionViewer.tsx
│   │   ├── ChatWindow.tsx
│   │   ├── QuizPlayer.tsx
│   │   └── ProgressTracker.tsx
│   │
│   ├── api/
│   │   └── client.ts
│   │
│   └── state/
│       └── store.ts
│
└── package.json