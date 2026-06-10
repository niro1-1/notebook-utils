"""Streaming data loader with empty file error handling."""

from data_loaders import DataLoader, EmptyFileError


class StreamingDataLoader:
    """Streaming data loader that validates for empty files."""

    def __init__(self, filepath, batch_size=32):
        self.filepath = filepath
        self.batch_size = batch_size

    def __iter__(self):
        lines = DataLoader(self.filepath).load_lines()
        for i in range(0, len(lines), self.batch_size):
            yield lines[i:i + self.batch_size]
