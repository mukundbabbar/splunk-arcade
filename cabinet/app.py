import os
import uvicorn
from src import create_app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, port=5000, root_path=f"/player/{os.getenv('PLAYER_NAME')}/")
