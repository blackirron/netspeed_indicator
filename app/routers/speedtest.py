"""
The actual "speed test" logic.

How internet speed testing works, conceptually:
- DOWNLOAD speed = send the client a known amount of data, client measures
  how long it took to arrive, computes Mbps.
- UPLOAD speed = client sends a known amount of data to us, WE measure how
  long it took to arrive, tell the client the elapsed time, client computes Mbps.

No Claude API involved anywhere in this app — pure I/O timing.
"""

import os
import time

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter(prefix="/speedtest", tags=["speedtest"])

CHUNK_SIZE = 64 * 1024  # 64KB per chunk while streaming


def _generate_random_chunks(total_bytes: int):
    remaining = total_bytes
    while remaining > 0:
        chunk = min(CHUNK_SIZE, remaining)
        yield os.urandom(chunk)
        remaining -= chunk


@router.get("/download")
def download_test(size_mb: float = 5.0):
    """
    Client calls this, times how long the full response takes to arrive,
    and computes: speed_mbps = (size_mb * 8) / seconds_elapsed
    """
    total_bytes = int(size_mb * 1024 * 1024)
    return StreamingResponse(
        _generate_random_chunks(total_bytes),
        media_type="application/octet-stream",
        headers={"Content-Length": str(total_bytes)},
    )


class UploadResult(BaseModel):
    received_bytes: int
    server_processing_seconds: float


@router.post("/upload", response_model=UploadResult)
async def upload_test(request: Request):
    """
    Client sends raw bytes as the request body and times the whole
    request/response round trip itself (that round-trip time is what
    matters for the client's upload Mbps calculation — the server
    processing time is just extra info).
    """
    start = time.perf_counter()
    body = await request.body()
    elapsed = time.perf_counter() - start
    return UploadResult(received_bytes=len(body), server_processing_seconds=elapsed)
