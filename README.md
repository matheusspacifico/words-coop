### 1. Backend

```bash
cd backend
```

#### a. Crie e Ative o Ambiente Virtual (`venv`)

* **macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

* **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

#### b. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 2. Inicie o Servidor

```bash
uvicorn app.main:app --reload
```

* `app.main`: Refere-se ao arquivo `main.py` dentro da pasta `app/`.
* `:app`: Refere-se à instância `app = FastAPI()` criada no arquivo.
* `--reload`: Faz com que o servidor reinicie automaticamente a cada alteração no código.

Se tudo correu bem, você verá uma saída no terminal indicando que o servidor está rodando:

```
INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Endpoint do WebSocket

O servidor expõe um único endpoint para a comunicação via WebSocket:

`ws://127.0.0.1:8000/ws/{game_id}/{client_id}`

* `{game_id}`: Um identificador único para cada partida. O frontend deve gerar ou permitir que o usuário insira este ID para que os jogadores possam se encontrar na mesma "sala".
* `{client_id}`: Um identificador único para cada cliente/jogador, para que o backend saiba quem enviou qual mensagem.

