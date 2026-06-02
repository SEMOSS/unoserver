import subprocess, tempfile, os
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Unoserver API",
    version="1.0.0",
    description="API for converting documents using unoserver",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def healthz():
    r = subprocess.run(["unoping", "--host", "127.0.0.1", "--port", "2003"])
    if r.returncode != 0:
        raise HTTPException(503, "unoserver not ready")
    return {"ok": True}


@app.post("/convert")
async def convert(file: UploadFile, to: str = "pdf"):
    if not file.filename:
        raise HTTPException(400, "File must have a filename")
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, file.filename)
        out = os.path.join(d, f"out.{to}")
        with open(src, "wb") as f:
            f.write(await file.read())
        proc = subprocess.run(
            ["unoconvert", "--port", "2003", "--convert-to", to, src, out],
            capture_output=True,
        )
        if proc.returncode != 0:
            raise HTTPException(500, proc.stderr.decode()[:500])
        with open(out, "rb") as f:
            return Response(f.read(), media_type="application/pdf")
