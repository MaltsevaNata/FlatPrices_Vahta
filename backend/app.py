
from api.WebSocketAPI import WebSocketAPI


def create_app():
    service = WebSocketAPI()
    return service.app


app = create_app()


if __name__ == '__main__':
    service = WebSocketAPI()
    service.run()