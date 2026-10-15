class PostResponse:
    def __init__(self, id: int = None, title: str = "", content: str = "", status: str = "", flagged_reasons: str = None, created_at: str = None, **kwargs):
        self.id = id
        self.title = title
        self.content = content
        self.status = status
        self.flagged_reasons = flagged_reasons
        self.created_at = created_at
