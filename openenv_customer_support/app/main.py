from fastapi import FastAPI
from openenv.core.env_server import create_fastapi_app
from environment import GuessNumberEnv

app: FastAPI = create_fastapi_app(GuessNumberEnv)