const WebSocket = require("ws");

const websocket = new WebSocket("ws://localhost:8765");

websocket.onopen = () => {
    console.log("WebSocket connected");
    websocket.send("10011010");
};

websocket.onmessage = (event) => {
    console.log(`Received: ${event.data}`);
};

websocket.onerror = (event) => {
    console.error("WebSocket error:", event);
};