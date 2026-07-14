from pathlib import Path
import os

class ConfigManager:
    def __init__(self):
        self.path = Path(os.environ['LOCALAPPDATA']) / 'WTUtils' / 'WTCCM' / 'config.json'
        
