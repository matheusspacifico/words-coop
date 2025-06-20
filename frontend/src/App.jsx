import { useState, useEffect, useRef } from "react";

export default function App() {
  const [gameId, setGameId] = useState("");
  const [clientId, setClientId] = useState("");
  const [connected, setConnected] = useState(false);
  const [socket, setSocket] = useState(null);
  const [guess, setGuess] = useState("");
  const [messages, setMessages] = useState([]);
  const [turn, setTurn] = useState(null);
  const [players, setPlayers] = useState([]);
  const guessesEndRef = useRef(null);

  useEffect(() => {
    if (guessesEndRef.current) {
      guessesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const connectWebSocket = () => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${gameId}/${clientId}`);
    ws.onopen = () => {
      setConnected(true);
      setMessages([]);
    };
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data);
      if (data.event === "game_state" || data.event === "game_start") {
        setTurn(data.turn);
        setPlayers(data.players);
      }
      if (data.event === "game_update") {
        setTurn(data.turn);
        addMessage(`Tentativa: ${data.guess} → ${data.result.join("")}`);
      }
      if (data.event === "game_over") {
        addMessage(data.message);
      }
      if (data.event === "player_left") {
        addMessage(data.message);
      }
      if (data.message) addMessage(data.message);
    };
    ws.onclose = () => {
      setConnected(false);
      setSocket(null);
      addMessage("Conexão encerrada.");
    };
    setSocket(ws);
  };

  const addMessage = (msg) => {
    setMessages((prev) => [...prev, msg]);
  };

  const submitGuess = () => {
    if (guess.length !== 5) return alert("A palavra deve ter 5 letras.");
    socket.send(JSON.stringify({ event: "submit_guess", word: guess }));
    setGuess("");
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gray-900 text-white">
      {!connected ? (
        <div className="space-y-4 w-full max-w-sm">
          <input
            type="text"
            className="w-full p-2 rounded bg-gray-800"
            placeholder="ID da Sala"
            value={gameId}
            onChange={(e) => setGameId(e.target.value)}
          />
          <input
            type="text"
            className="w-full p-2 rounded bg-gray-800"
            placeholder="Seu Nome ou ID"
            value={clientId}
            onChange={(e) => setClientId(e.target.value)}
          />
          <button
            className="w-full p-2 rounded bg-green-600 hover:bg-green-700"
            onClick={connectWebSocket}
          >
            Entrar no jogo
          </button>
        </div>
      ) : (
        <div className="w-full max-w-md space-y-3">
          <div className="text-sm text-gray-400">
            Jogadores: {players.join(", ")}
            <br />
            Turno de: {turn}
          </div>
          <div className="h-64 overflow-y-auto bg-gray-800 rounded p-2 text-sm">
            {messages.map((msg, idx) => (
              <div key={idx} className="mb-1">
                {msg}
              </div>
            ))}
            <div ref={guessesEndRef} />
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              className="flex-1 p-2 rounded bg-gray-700"
              maxLength={5}
              value={guess}
              onChange={(e) => setGuess(e.target.value.toUpperCase())}
            />
            <button
              className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-700"
              onClick={submitGuess}
              disabled={turn !== clientId}
            >
              Jogar
            </button>
          </div>
          <button
            className="w-full p-2 rounded bg-red-600 hover:bg-red-700 mt-2"
            onClick={() => {
              socket.close();
              setConnected(false);
            }}
          >
            Sair
          </button>
        </div>
      )}
    </div>
  );
}
