import shutil
from typing import Optional
from pathlib import Path
from config import ConfigManager


class SoundManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.stored_path = self.config.dir_path / 'SoundMods'
        self.stored_path.mkdir(parents=True, exist_ok=True)
        self.enabled_mods: list[Path] = self.config.enabled_mods

    def toggle_soundmod(self, forcevalue: Optional[bool] = None) -> bool:
        """Toggles the enable_mod in config.blk and returns current value."""
        path = self.config.wt_path / 'config.blk'
        original_cfg = path.read_text(encoding='utf-8')
        if forcevalue is None:
            forcevalue = False if self.soundmod_enabled else True

        if forcevalue:
            cfg = original_cfg.replace('enable_mod:b=no', 'enable_mod:b=yes')
            path.write_text(cfg, encoding="utf-8")
            return True

        else:
            cfg = original_cfg.replace('enable_mod:b=yes', 'enable_mod:b=no')
            path.write_text(cfg, encoding="utf-8")
            return False

    @property
    def soundmod_enabled(self) -> bool:
        path = self.config.wt_path / 'config.blk'
        return True if path.read_text(encoding='utf-8').find('enable_mod:b=yes') != -1 else False

    @property
    def stored_mods(self) -> list[Path]:
        stored: list[Path] = []
        for mod in self.stored_path.iterdir():
            stored.append(mod)
        return stored

    def enable_mod(self, mod: Path, clear_dir: bool = True) -> None:
        if not mod: return
        mod_folder = self.config.wt_path / 'sound' / 'mod'
        if clear_dir:
            shutil.rmtree(mod_folder)
            mod_folder.mkdir()
        shutil.copytree(mod, mod_folder, dirs_exist_ok=True)
        self.enabled_mods = [mod]
        self.config.save_enabled_mods([mod])


    @property
    def disabled_mods(self) -> list[Path]:
        stored = self.stored_mods.copy()
        if self.enabled_mods:
            for mod in self.enabled_mods:
                stored.remove(mod)
        return stored

    def disable_mod(self, mod: Path):
        if not mod: return
        mod_folder = self.config.wt_path / 'sound' / 'mod'
        self.enabled_mods.remove(mod)
        self.config.save_enabled_mods(self.enabled_mods)
        shutil.rmtree(mod_folder)
        mod_folder.mkdir()
