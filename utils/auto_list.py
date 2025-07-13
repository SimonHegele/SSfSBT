class AutoList(list):
    """
    This list automatically extends itself to allow accessing and
    setting values at indices beyond the current length of the list.
    """

    def __init__(self, default_factory=lambda: None):
        super().__init__()
        self.default_factory = default_factory

    def __getitem__(self, index):
        if index >= len(self):
            self.extend(self.default_factory() for _ in range(index + 1 - len(self)))
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend(self.default_factory() for _ in range(index + 1 - len(self)))
        super().__setitem__(index, value)
