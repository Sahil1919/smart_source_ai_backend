import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("core.server:app", port=port, reload=True)
