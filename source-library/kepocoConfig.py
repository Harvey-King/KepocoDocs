
def updateAudio(newval):
    import kepoco
    kepoco.audio.setEnabled(newval)
    kepoco.audio.play(500,20)

def updateBirghtness(newval):
    import kepoco
    kepoco.display.brightness(newval)


class Configuration:
    
    _settings = {
        "audioenabled": {
            "shortname": "Audio",
            "options": ["Off", "On"],
            "default": 1,
            "onchange": updateAudio
        },
        "lastgame": {
            "default": "/Games/Evaluator/Evaluator.py",
            "hidden": True,
        },
        "brightness": {
            "shortname": "Brite",
            "options": ["Low", "Mid", "Hi"],
            "values": [1, 28, 127],
            "default": 1,
            "onchange": updateBirghtness
        },
        "vga": {
            "shortname": "VGA",
            "options": ["Off", "Copy", "Only"],
            "default": 1,
        }
    }
    
    _index2key = list(sorted(k for k, v in _settings.items() if ("hidden" not in v) or (not v["hidden"])))
    _key2index = {k: i for i, k in enumerate(_index2key)}
    
    def __init__(self):
        self._options = {k: v["default"] for k, v in Configuration._settings.items()}
        try:
            with open("kepoco.cfg", "r") as f:
                for l in f.readlines():
                    k, v = l.strip().split("=")
                    try: 
                        self._options[k] = int(v)
                    except:
                        self._options[k] = v
        except OSError:
            pass
    
    def __getitem__(self, key):
        return self._options[Configuration.toKey(key)]
    
    def __setitem__(self, key, value):
        key = Configuration.toKey(key)
        if self._options[key] == value:
            return
        info = Configuration._settings[key]
        self._options[key]=(value%len(info["options"])) if "options" in info else value
        with open("kepoco.cfg", "w") as f:
            for k, v in self._options.items():
                f.write(f"{k}={v}\n")
        if "onchange" in info:
            info["onchange"](info["values"][value] if "values" in info else value)
    
    def __getattr__(self,key):
        if key in self._options:
            idx = self._options[key]
            info = Configuration._settings[key]
            if "values" in info:
                return info["values"][idx]
            return info["options"][idx] if "options" in info else idx
        return super().__getattr__(key)
    
    def getOption(self, key):
        key = Configuration.toKey(key)
        idx = self._options[key]
        info = Configuration._settings[key]
        if "values" in info:
            return info["values"][idx]
        return info["options"][idx] if "options" in info else idx
    
    def getValue(self, key):
        key = Configuration.toKey(key)
        idx = self._options[key]
        info = Configuration._settings[key]
        return info["values"][idx] if "values" in info else idx
    
    def items(self):
        return self._options.items()
    
    def keys(self):
        return self._options.keys()
    
    def values(self):
        return ((k, info["values"][idx] if "values" in (info:=Configuration._settings[k]) else idx) for k, idx in self._options.items())
    
    def options(self):
        return ((k, info["options"][idx] if "options" in (info:=Configuration._settings[k]) else idx) for k, idx in self._options.items())
    
    def __len__(self):
        return len(self._options)
    
    @classmethod
    def toKey(cls, key):
        if isinstance(key, str):
            return key
        elif isinstance(key, int):
            return Configuration._index2key[key]
        else:
            raise KeyError(key)
    
    @classmethod
    def settings(cls):
        return list(Configuration._index2key)
    
    @classmethod
    def allSettings(cls):
        return list(Configuration._settings.keys())
    
    @classmethod
    def getOptions(cls, key):
        info = Configuration._settings[Configuration.toKey(key)]
        return info["options"] if "options" in info else None
    
    @classmethod
    def getValues(cls, key):
        info = Configuration._settings[Configuration.toKey(key)]
        if "values" in info:
            return info["values"]
        if "options" in info:
            return list(range(len(info["options"])))
        return Nones
    
    @classmethod
    def getShortName(cls, key):
        return Configuration._settings[Configuration.toKey(key)]["shortname"]
    
    def __repr__(self):
        return f"Configuration{ {k: v for k, v in self.options()} }"


settings = Configuration()

if __name__ == "__main__":
    print(settings)
    print(settings["brightness"])
    print(settings.brightness)
    print(settings.lastgame)
