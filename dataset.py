import functools

@functools.lru_cache(maxsize=128)
def get_dataset(path):
    # Load dataset from the given path
    pass
