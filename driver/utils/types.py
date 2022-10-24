from typing import (
    Tuple,
    Dict,
    List,
    Any
)

from numpy import (
    ndarray
)

Frame = ndarray or List[float]# Picture is a flattened (1D) numpy array

Metadata = ndarray or List[Any] # Metadata is a flattened (1D) numpy array

Picture = Tuple[Frame, Metadata] # Picture is a tuple of a frame and metadata