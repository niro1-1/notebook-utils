# Streaming Data Loaders
import os


class StreamingDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"{self.file_path} not found")

        if os.path.getsize(self.file_path) == 0:
            raise ValueError("Input file is empty")

        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()
