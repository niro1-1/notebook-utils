"""Data loader with error handling for empty files."""

class EmptyFileError(Exception):
    """Raised when attempting to load data from an empty file."""
    pass


class DataLoader:
    """A data loader that validates files are not empty before loading."""

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        """Load data from file, raising EmptyFileError if file is empty."""
        import os
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        if os.path.getsize(self.filepath) == 0:
            raise EmptyFileError(f"File is empty: {self.filepath}")
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def load_lines(self):
        """Load lines from file, raising EmptyFileError if file is empty."""
        content = self.load()
        lines = content.strip().split('\n')
        if not lines or (len(lines) == 1 and not lines[0]):
            raise EmptyFileError(f"File contains no data: {self.filepath}")
        return lines
