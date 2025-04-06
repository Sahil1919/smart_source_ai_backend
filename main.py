import uvicorn

if __name__ == "__main__":
    uvicorn.run("core.server:app", reload=True)
