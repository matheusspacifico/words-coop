from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, game_id: str):
        """Aceita uma nova conexão e a adiciona à sua sala de jogo."""
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)

    def disconnect(self, websocket: WebSocket, game_id: str):
        """Remove uma conexão da sala de jogo."""
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]

    async def broadcast(self, game_id: str, message: dict):
        """Envia uma mensagem JSON para todos os clientes na mesma sala."""
        if game_id in self.active_connections:
            message_json = json.dumps(message)
            for connection in self.active_connections[game_id]:
                await connection.send_text(message_json)

manager = ConnectionManager()