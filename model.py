class task:
    def __init__(self):
        self.id = None
        self.name = None
        self.content = None
        self.status = None


    def set(self,num,name,content):
        self.id = num
        self.name = name
        self.content = content
        self.status = "Todo"

    def __repr__(self):
        return f"Task(id={self.id}, name={self.name!r}, status={self.status!r} content={self.content!r})"

    def __str__(self):
        return f"[{self.id}] {self.name}"

