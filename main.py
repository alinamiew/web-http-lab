from fastapi import FastAPI, Response
from fastapi.testclient import TestClient

app = FastAPI(title="Notes API", version="0.1.0")
