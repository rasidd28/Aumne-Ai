class PostPublishResponse:
    def __init__(self, id: int = None, status: str = "", message: str = "", **kwargs):
        self.id = id
        self.status = status
        self.message = message
