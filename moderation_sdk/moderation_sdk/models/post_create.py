class PostCreate:
    def __init__(self, title: str = "", content: str = ""):
        self.title = title
        self.content = content

    def to_dict(self):
        return {"title": self.title, "content": self.content}
