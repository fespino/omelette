import asyncio
import logging
import typing

from jinja2 import Template
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

template = """
<!doctype html>
<html>
    <head>
        <script type="text/javascript">
            function runWebSockets() {
                if ("WebSocket" in window) {
                    var ws = new WebSocket("ws://localhost:8000/om");
                    ws.onopen = function() {
                        console.log("Sending websocket data")
                        ws.send("Hello from client")
                    };
                    ws.onmessage = function(e) {
                        console.log(e.data)
                        Object.entries(JSON.parse(e.data)).forEach(([key, value]) => {
                            console.log(key, value)
                            const el = document.querySelector(`[data-om_${key}]`)
                            el.textContent = value
                        })
                    };
                    ws.onclose = function() {
                        console.log("Closing websocket connection");
                    };
                } else {
                    alert("WS not supported, sorry!")
                }
            }
        </script>
    </head>
    <body>
        <a href="javascript:runWebSockets()">Start counting!</a>
        <p data-om_counter>0</p>
        <p data-om_msg>Nothing yet</p>
    </body>
</html>
"""

app = Starlette()
logger = logging.getLogger()


@app.route("/")
async def homepage(_: Request) -> HTMLResponse:
    return HTMLResponse(Template(template).render())


@app.websocket_route("/om")
class WebSocketTicks(WebSocketEndpoint):
    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.ticker_task = asyncio.create_task(self.tick(websocket))
        logger.debug("connected")

    async def on_disconnect(self, _: WebSocket, close_code: int) -> None:
        self.ticker_task.cancel()
        logger.debug("disconnect: %s", close_code)

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        await websocket.send_json(dict(msg=data))

    async def tick(self, websocket: WebSocket) -> None:
        counter = 0
        while True:
            logger.debug(counter)
            await websocket.send_json(dict(counter=counter))
            counter += 1
            await asyncio.sleep(1)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, log_level="debug")
