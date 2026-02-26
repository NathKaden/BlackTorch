# 🔥 BlackTorch

> Plateforme de génération de modèles 3D par IA, optimisée pour les GPU NVIDIA Blackwell.

---

## 🧱 Stack Technique

| Couche        | Technologie                                                       |
|---------------|-------------------------------------------------------------------|
| Frontend      | Next.js 15, HeroUI, React Three Fiber, TanStack Query            |
| Backend       | FastAPI, Python 3.12, Clean Architecture + DDD                   |
| IA / ML       | PyTorch 2.5+, StableFast3D, FP4 (Blackwell)                      |
| Messaging     | Redis 7 (queue + Pub/Sub)                                        |
| Temps réel    | WebSockets (FastAPI native)                                       |
| Format sortie | `.glb` (GLTF Binary)                                             |
| Conteneurs    | Docker + docker-compose                                           |

---

## 🗂️ Architecture

```
BlackTorch/
├── client/                          # Frontend — Next.js 15 + Atomic Design
│   └── src/
│       ├── app/                     # App Router (layout, page)
│       ├── components/
│       │   ├── atoms/               # Button, Input, ModelBadge
│       │   ├── molecules/           # SearchBar, ModelCard
│       │   └── organisms/           # ThreeCanvas, GenerationPanel
│       ├── core/
│       │   ├── domain/              # Types TS : Prompt, Job, ThreeDModel
│       │   └── use-cases/           # useGenerateModel, useJobStatus
│       ├── lib/                     # api-client.ts
│       └── providers/               # HeroUI + TanStack Query
│
└── server/                          # Backend — FastAPI + Clean Archi + DDD
    ├── domain/
    │   ├── entities/                # Prompt, Job, ThreeDModel
    │   └── repositories/            # Interfaces abstraites (ports)
    ├── application/
    │   └── use_cases/               # GenerateModelFromText, GetModelStatus
    ├── infrastructure/
    │   ├── adapters/                # StableFast3DAdapter, StorageAdapter
    │   ├── redis/                   # JobQueue, RedisJobRepository
    │   └── worker/                  # Worker IA (boucle de consommation)
    ├── interfaces/
    │   ├── routes/                  # generation.py, websocket.py, models.py
    │   ├── schemas.py               # DTOs Pydantic
    │   ├── dependencies.py          # FastAPI Depends (DI)
    │   └── main.py                  # Application FastAPI
    └── tests/                       # Tests unitaires domaine
```

---

## ⚙️ Workflow de Génération IA

```
[Utilisateur] → Prompt texte
      ↓
[Next.js] useGenerateModel() → POST /api/v1/generate
      ↓
[FastAPI] → Crée un Job (PENDING) → Redis Queue
      ↓
[Worker PyTorch — RTX]
  ├── Charge StableFast3D (FP4 / Blackwell, < 12 Go VRAM)
  ├── Publie la progression → Redis Pub/Sub (20% → 50% → 80%)
  └── Export mesh → .glb → StorageAdapter
      ↓
[WebSocket] → Notifie le client en temps réel
      ↓
[React Three Fiber] → Affiche le modèle 3D (OrbitControls + autoRotate)
```

---

## 🚀 Installation

### Prérequis

- Node.js `20+`
- Python `3.12+`
- CUDA `12.8+` + drivers NVIDIA Blackwell
- Redis `7+` (ou Docker)

### 1. Frontend

```bash
cd client
npm install
cp .env.local.example .env.local   # ou éditer manuellement
npm run dev                         # → http://localhost:3000
```

### 2. Backend

```bash
cd server
python -m venv .venv
.venv\Scripts\activate              # Windows
pip install -r requirements.txt

# PyTorch avec CUDA 12.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

### 3. Lancer les services

```bash
# Terminal 1 — API
uvicorn server.interfaces.main:app --reload --port 8000

# Terminal 2 — Worker IA
python -m server.infrastructure.worker.main

# Terminal 3 — Redis (si pas dockerisé)
docker run -p 6379:6379 redis:7-alpine
```

### 4. Tout-en-un avec Docker

```bash
docker-compose up --build
```

---

## 🧪 Tests

```bash
cd server
pytest tests/ -v
```

---

## 📡 API Reference

| Méthode     | Endpoint                          | Description                    |
|-------------|-----------------------------------|--------------------------------|
| `POST`      | `/api/v1/generate`                | Soumettre un prompt            |
| `GET`       | `/api/v1/jobs/{job_id}`           | Statut HTTP d'un job           |
| `WS`        | `/api/v1/ws/jobs/{job_id}`        | Statut temps réel (WebSocket)  |
| `GET`       | `/api/v1/models/{job_id}/download`| Télécharger le `.glb`          |
| `GET`       | `/health`                         | Health check                   |

---

## 📄 Licence

MIT

