## Random Seed Handling

To ensure reproducibility in experiments, it is crucial to manage the random seed effectively. This section outlines how to handle random seeds within the notebook-utils package.

### Setting the Random Seed

You can set the random seed using the following function:

```python
import random
import numpy as np
import torch

def set_random_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
```

### Propagation of Random Seed

When using multiple libraries, ensure that the random seed is set for each library to maintain consistency across your experiments. This will help in achieving reproducible results across different runs.
```

### Example Usage

```python
set_random_seed(42)
# Your code here
```
``