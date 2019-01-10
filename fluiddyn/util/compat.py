try:
    # python 3.8+
    from functools import cached_property
except ImportError:
    from cached_property import cached_property
