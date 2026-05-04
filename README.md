# OCI Integrator API

## Setup

```bash
pip install -r requirements.txt
```

## Correr en local

```bash
uvicorn app.main:app --reload
```

## Endpoints

| Método | Ruta             | Descripción                              | HTTP Code |
|--------|------------------|------------------------------------------|-----------|
| GET    | /ping            | Health check simple                      | 200       |
| POST   | /items           | Crea un item (simula escritura en BD)    | 201       |
| POST   | /jobs            | Lanza proceso largo en background        | 202       |
| GET    | /jobs/{job_id}   | Consulta estado de un job               | 200 / 404 |

## Docs interactivas

Swagger UI → http://localhost:8000/docs  
ReDoc      → http://localhost:8000/redoc
