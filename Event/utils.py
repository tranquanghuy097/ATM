import fastapi


class FastApiFactory():
    def get_app():
        app = fastapi.FastAPI()
        return app
