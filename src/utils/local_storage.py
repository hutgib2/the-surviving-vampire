import sys
import json

WEB = sys.platform == "emscripten"

if WEB:
    import platform as _js  # pygbag's JS bridge, NOT the stdlib platform module
else:
    import os


class LocalStorage:
    """
	Stores all data as one dict under a single key.
    Uses the browser's localStorage under pygbag, and a JSON file on desktop.
    Values can be anything JSON-serializable: numbers, strings, bools, None, lists and dicts.
    """

    def __init__(self, path, key, default=None):
        self.file = path    # file name on desktop
        self.key = key      # localStorage key on web
        self.default = default or {}
        self.data = self.load()

    def save(self):
        """Write the current data to storage."""
        text = json.dumps(self.data)
        if WEB:
            _js.window.localStorage.setItem(self.key, text)
        else:
            with open(self.file, "w") as f:
                f.write(text)

    def load(self):
        """Read the data from storage, or return a copy of the default."""
        try:
            if WEB:
                text = _js.window.localStorage.getItem(self.key)
                if not text:  # key doesn't exist yet (JS null)
                    return dict(self.default)
            else:
                if not os.path.exists(self.file):
                    return dict(self.default)
                with open(self.file) as f:
                    text = f.read()
            return json.loads(text)
        except Exception:
            return dict(self.default)  # corrupt or unreadable save, so start fresh

    def clear(self):
        """Delete the save and reset the data to the default."""
        if WEB:
            _js.window.localStorage.removeItem(self.key)
        elif os.path.exists(self.file):
            os.remove(self.file)
        self.data = dict(self.default)

    # dict-style access to the data: storage["high_score"] = 100
    def get(self, name, default=None):
        return self.data.get(name, default)

    def __getitem__(self, name):
        return self.data[name]

    def __setitem__(self, name, value):
        self.data[name] = value

    def __contains__(self, name):
        return name in self.data

    def __repr__(self):
        return f"LocalStorage({self.data!r})"
