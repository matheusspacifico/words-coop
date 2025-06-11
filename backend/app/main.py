from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

from .websocket_manager import manager
from .game_logic import escolher_palavra, avaliar_tentativa

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_games = {}

@app.websocket("/ws/{game_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, client_id: str):
    await manager.connect(websocket, game_id)
    
    if game_id not in active_games:
        active_games[game_id] = {
            "palavra_secreta": escolher_palavra(),
            "tentativas": [],
            "resultados": [],
            "jogadores": [],
            "turno": 0,
            "max_tentativas": 6
        }
    
    game = active_games[game_id]
    
    if client_id not in game["jogadores"]:
        game["jogadores"].append(client_id)
        
    await websocket.send_text(json.dumps({
        "event": "game_state",
        "guesses": game["tentativas"],
        "results": game["resultados"],
        "turn": game["jogadores"][game["turno"] % len(game["jogadores"])] if game["jogadores"] else None,
        "players": game["jogadores"]
    }))

    if len(game["jogadores"]) == 2:
        await manager.broadcast(game_id, {
            "event": "game_start",
            "message": "Ambos os jogadores estão conectados. O jogo começou!",
            "turn": game["jogadores"][game["turno"]]
        })
        
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["event"] == "submit_guess":
                tentativa = message["word"].upper()
                
                if len(tentativa) != 5 or not tentativa.isalpha():
                    continue
                
                jogador_da_vez = game["jogadores"][game["turno"] % 2]
                if client_id != jogador_da_vez:
                    continue

                resultado = avaliar_tentativa(game["palavra_secreta"], tentativa)
                game["tentativas"].append(tentativa)
                game["resultados"].append(resultado)
                game["turno"] += 1
                
                venceu = (tentativa == game["palavra_secreta"])
                perdeu = (len(game["tentativas"]) >= game["max_tentativas"]) and not venceu
                
                update_message = {
                    "event": "game_update",
                    "guess": tentativa,
                    "result": resultado,
                    "turn": game["jogadores"][game["turno"] % 2]
                }
                await manager.broadcast(game_id, update_message)

                if venceu:
                    await manager.broadcast(game_id, {
                        "event": "game_over",
                        "outcome": "vitoria",
                        "message": f"Parabéns! Vocês adivinharam a palavra: {game['palavra_secreta']}"
                    })
                elif perdeu:
                    await manager.broadcast(game_id, {
                        "event": "game_over",
                        "outcome": "derrota",
                        "message": f"Fim de jogo! A palavra era: {game['palavra_secreta']}"
                    })

    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)
        game["jogadores"].remove(client_id)
        await manager.broadcast(game_id, {"event": "player_left", "message": f"Jogador {client_id} saiu."})
        if not game["jogadores"]:
            del active_games[game_id]