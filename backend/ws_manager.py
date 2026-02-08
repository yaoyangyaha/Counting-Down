# ws_manager.py
from fastapi import WebSocket
from typing import List
import asyncio

class WSManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.connections:
            self.connections.remove(ws)

    async def broadcast(self, data):
        # 广播给所有已连接客户端
        for ws in self.connections:
            try:
                await ws.send_json(data)
            except:
                self.disconnect(ws)

# 单例
ws_manager = WSManager()
