class Configuration:
    def __init__(self, host: str = "http://localhost:8000"):
        self.host = host.rstrip("/")
