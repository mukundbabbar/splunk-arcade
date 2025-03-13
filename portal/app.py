import uvicorn
from src import create_app

if __name__ == "__main__":
    app = create_app()
    # Using multiple workers instead of threads since uvicorn is async
    uvicorn.run(app, port=5000, workers=4)
