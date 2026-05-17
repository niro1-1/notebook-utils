# Streaming Data Loaders

This implementation provides support for loading data in a streaming manner, allowing datasets that do not fit in memory to be processed efficiently.

## Implementation Details
- Added `StreamingDataLoader` class.
- Integrated with S3 for on-demand batch retrieval.

## Usage
```python
loader = StreamingDataLoader(s3_bucket='my-bucket', data_key='data/')
for batch in loader:
    process(batch)
``n