import ctypes
import json
from pathlib import Path
import os
import winreg as wr
from typing import Optional

import vdf

class ConfigManager:
    def __init__(self):
        self.dir_path = Path(os.environ['LOCALAPPDATA']) / 'WTUtils' / 'WTCCM'
        self.__default_template: dict[str, dict[str, str] | list[str]] = {
            'path': {
                'downloads': '',
                'wt': '',
                'winrar': '',
                'documents': '',
                'sights': ''
            },
            'enabledSoundmods': []
        }
        self.loaded = None
        self.load()

    # Basic control functions. Do not return anything.
    def load(self):
        self.__ensure()
        with open(self.dir_path / 'wtccm.json', 'r+', encoding='utf-8') as file:
            saved_in_json = json.load(file)
        self.loaded = saved_in_json

    def save(self):
        with open(self.dir_path / 'wtccm.json', 'w', encoding='utf-8') as file:
            json.dump(self.loaded, file, indent=4, ensure_ascii=False)

    def __ensure(self):
        if not os.path.isfile(self.dir_path / 'wtccm.json'):
            self.reset()

    def reset(self):
        self.dir_path.mkdir(parents=True, exist_ok=True)    # Создание папки конфига
        with open(self.dir_path / 'wtccm.json', "w", encoding="utf-8") as file:
            json.dump(self.__default_template, file, ensure_ascii=False, indent=4)
        self.load()


    # *_path functions: Return a Path object either from config or fetch it from system itself.
    @property
    def wt_path(self)           -> Path:
        if self.loaded['path']['wt']: return Path(self.loaded['path']['wt'])

        Registry = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        RawKey = wr.OpenKey(Registry, r"SOFTWARE\WOW6432Node\Valve\Steam")
        path = wr.QueryValueEx(RawKey, "InstallPath")[0]
        with open(f'{path}\\steamapps\\libraryfolders.vdf', encoding='utf-8') as file:
            steamapps_path = vdf.load(file)['libraryfolders']['1']['path']
        wt_path = f'{steamapps_path}\\steamapps\\common\\War Thunder\\'
        self.loaded['path']['wt'] = wt_path
        self.save()
        return Path(wt_path)

    @property
    def winrar_path(self)       -> Path:
        if self.loaded['path']['winrar']: return Path(self.loaded['path']['winrar'])

        wr_path = os.path.join(os.environ.get("ProgramFiles"), 'WinRAR', 'WinRAR.exe')
        self.loaded['path']['winrar'] = wr_path
        self.save()
        return Path(wr_path)

    @property
    def documents_path(self)    -> Path:
        if self.loaded['path']['documents']: return Path(self.loaded['path']['documents'])

        CSIDL_PERSONAL = 5
        buf = ctypes.create_unicode_buffer(260)
        # noinspection PyUnresolvedReferences
        ctypes.windll.shell32.SHGetFolderPathW(
            None, CSIDL_PERSONAL, None, 0, buf
        )
        documents_folder = str(Path(buf.value))
        self.loaded['path']['documents'] = documents_folder
        self.save()
        return Path(documents_folder)

    @property
    def downloads_path(self)    -> Path:
        if self.loaded['path']['downloads']: return Path(self.loaded['path']['downloads'])

        download_folder = Path.home() / "Downloads"
        self.loaded['path']['downloads'] = str(download_folder)
        self.save()
        return Path(download_folder)

    @property
    def sights_path(self)       -> Path:
        if self.loaded['path']['sights']: return Path(self.loaded['path']['sights'])

        with open(self.documents_path / "My Games\\WarThunder\\Saves\\lastlogin.blk", 'r', encoding='utf-8') as file:
            lastlogin = file.readline().removeprefix("uid:i64=").removesuffix('\n')
        sights_folder = self.documents_path / lastlogin / "production\\UserSights\\all_tanks\\"
        self.loaded['path']['sights'] = str(sights_folder)
        self.save()
        return Path(sights_folder)

    def save_enabled_mods(self, values:list[Path]):
        self.loaded['enabledSoundmods'] = []
        for value in values:
            self.loaded['enabledSoundmods'].append(str(value))
        self.save()

    @property
    def enabled_mods(self) -> Optional[list[Path]]:
        if not self.loaded['enabledSoundmods']: return None
        return [Path(x) for x in self.loaded['enabledSoundmods']]
