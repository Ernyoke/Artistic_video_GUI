from threading import Lock


class Atomic:
    def set(self, val):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class AtomicBoolean(Atomic):
    def __init__(self):
        self.lock = Lock()
        self.val = False

    def set(self, val):
        with self.lock:
            self.val = val

    def get(self):
        with self.lock:
            return self.val

