"""Real loopback HTTP with a synthetic server; no Ollama/native/model execution."""

import asyncio
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from app.ollama import OllamaClient
from app.retrieval.chunking import iter_chunks
from app.retrieval.embeddings import (
    DIMENSIONS,
    MODEL_DIGEST,
    MODEL_NAME,
    Embedder,
    EmbeddingError,
)
from tests.unit.test_chunking import csv_source


@pytest.fixture
def local_model_server():
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requests.append((self.path, None))
            self.reply(
                {"version": "0.40.16"}
                if self.path == "/api/version"
                else {"models": [{"name": MODEL_NAME, "digest": MODEL_DIGEST}]}
            )

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            requests.append((self.path, body))
            self.reply(
                {
                    "model": MODEL_NAME,
                    "embeddings": [
                        [1.0] + [0.0] * (DIMENSIONS - 1) for _ in body["input"]
                    ],
                }
            )

        def reply(self, body):
            data = json.dumps(body).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    server.timeout = 1
    thread = threading.Thread(
        target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
    )
    thread.start()
    try:
        yield server.server_port, requests, thread
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
        assert not thread.is_alive()


def test_csv_chunks_embed_over_real_loopback_without_inherited_proxy(
    local_model_server, monkeypatch
):
    port, seen, thread = local_model_server
    monkeypatch.setenv("HTTP_PROXY", "http://127.0.0.1:1")
    monkeypatch.setenv("ALL_PROXY", "http://127.0.0.1:1")
    monkeypatch.setenv("NO_PROXY", "")
    chunks = list(iter_chunks(csv_source(b"Name,Units\nNorth,42\nSouth,50\n")))

    def check_owned_test_server():
        if not thread.is_alive():
            raise RuntimeError("Synthetic test server stopped")

    async def run():
        async with OllamaClient(
            port, ownership_check=check_owned_test_server, timeout=2
        ) as client:
            service = Embedder(client)
            documents = await service.documents(chunks)
            query = await service.query("North units?", "query-1")
            return documents, query

    documents, query = asyncio.run(run())
    assert [e.source_id for e in documents.embeddings] == [c.chunk_id for c in chunks]
    assert all(
        len(e.vector) == 768 and e.vector[0] == 1.0 for e in documents.embeddings
    )
    assert query.space_id == documents.space_id
    bodies = [body for path, body in seen if path == "/api/embed"]
    assert bodies[0]["input"] == ["search_document: " + c.text for c in chunks]
    assert bodies[1]["input"] == ["search_query: North units?"]
    assert all(body["truncate"] is False and body["keep_alive"] == 0 for body in bodies)


def test_running_unowned_loopback_server_receives_nothing(local_model_server):
    port, seen, _ = local_model_server

    async def run():
        async with OllamaClient(port) as client:
            await Embedder(client).query("Question", "query-1")

    with pytest.raises(EmbeddingError, match="OWNERSHIP_UNVERIFIED"):
        asyncio.run(run())
    assert seen == []
