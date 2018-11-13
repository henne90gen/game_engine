from datetime import datetime


class timer:
    def __init__(self):
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = datetime.now()
        diff = self.end - self.start
        print(f"This took {diff.total_seconds()*1000.0} ms")
