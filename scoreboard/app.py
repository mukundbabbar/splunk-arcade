from waitress import serve

from src import create_app, run_dummy_scores

if __name__ == "__main__":
    run_dummy_scores()
    app = create_app()
    serve(app, port=5000, threads=32)
