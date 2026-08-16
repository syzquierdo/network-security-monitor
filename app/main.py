from fastapi import FastAPI
from app.monitor import monitor_all_devices

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Network Monitor API is running"}


@app.get("/devices")
def get_devices():
    return monitor_all_devices()
    
