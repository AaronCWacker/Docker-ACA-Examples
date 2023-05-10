from typing import Union

from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello EXAMPLE": os.environ.get("EXAMPLE"),
            "Hello SECRET_EXAMPLE": os.environ.get("SECRET_EXAMPLE")
            }
