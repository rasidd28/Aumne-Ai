class PostSubmitResponse:
    def __init__(self, id: int = None, status: str = "", flagged_reasons: str = None, message: str = "", **kwargs):
        self.id = id
        self.status = status
        self.flagged_reasons = flagged_reasons
        self.message = message
