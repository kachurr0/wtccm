import base64
import subprocess
from io import BytesIO
from tkinter import *
from tkinter import ttk
import os, shutil
from typing import Optional
from tkinter.filedialog import askdirectory, askopenfilename
import winreg as wr
import vdf, json
import ctypes
from pathlib import Path
from PIL import ImageTk, Image


local_path = Path(os.environ['LOCALAPPDATA']) / 'WTUtils' / 'WTCCM'
local_path.mkdir(parents=True, exist_ok=True)

os.chdir(local_path)

root = Tk()
root.resizable(False, False)
root.wm_title('WTCCM')

# Decoding and setting up icon
icon_b64 = 'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL64tAD3fCAA5I5PCemFPCfqgjRB6YExTuqBMFHqgDBR6H4uUed9LVHleyxR5XorUeR5LFHkeStR5HgsUeR4LFHjeCxR4ncsUeJ2LFHidixR3nQrTt51LUHcdzIm1X5DCeNtHwC1rqUAAAAAAAAAAAAAAAAAAAAAAAAAAADmlFcA4Z1qA+yIPEjvgi6z8H4o5vB9JfbveyP773si/O56IPzteB/86nUe/OlzHfzpcxz86HId/OhxHfzncR3853Ed/OZwHvzmcB785W8d/OZwHvzkbh775G8f9uJvIObhcSWy3HMtSMl/SwPRej8AAAAAAAAAAAAAAAAA6JleANm5pALwiz5o84Mt7vSAJv/0fiX/830k//J8Iv/weyH/7Xgf/+p0HP/mcRz/5HAb/+RvGv/kbhv/424a/+NtGv/jbhr/4m0b/+JtG//ibBv/4Wwa/+JsG//ibBz/420c/+RtHf/ibiHu3XMtacGPeALTfEYAAAAAAKDRvADzjD0A8ZBHPfWHMun2gyn/9YEo//WAJ//0fyb/8n0j/+15If/kch3/3m0b/9tsG//Zahv/12ka/9doGv/WaBn/1mcZ/9ZnGf/WZxr/1Wca/9VmGf/WZxn/12cZ/9loG//caRr/4Gsa/+NrHP/ibiLp3HQxPt9xKQCPu6YA651hANu6oQL1jT2d94cv//eFLf/3hCv/9oIp//J/Jv/qeCD/2m0c/89lGf/MYxj/yGEX/8VfFv/EXhb/w10W/8JcFv/CXBb/wVwW/8BbFv/AWxb/wFsV/8FbFv/DXBb/x18Y/9BjGP/ZaBn/4Gsb/+NtHv/gcSievZR/AtR/SQDwmVgA8JlYFvaNO9T4iTL/+Ycw//iGLv/1gij/4HUi/7JeIv+dUx//mE8e/5VNHv+RTB7/jkkc/4xIHP+LSBz/ikcc/4tHHP+KRxz/iUcb/4lHG/+JRhz/iUYb/49IGv+nTxP/wVsV/9FjGP/daRv/42wd/+JwJNPbejwV2no7APSXUwD0l1Mo+I486PqLNv/6izT/+Ykx//GBKf+afWj/S3yo/0d5qf9Geaj/RXio/0R3qP9Bdqf/QXWl/0B0pf8/dKX/P3Sl/z90pP8+c6P/PnOk/z5zpP8/c6T/QHGg/2tXUf+0VBL/zWAX/9tnGv/ibB3/5HAj5t95NSbfeDUA9plUAPaaVS76kD/t+405//uNN//7izP/7IMw/3uVqv9BlNv/QpLX/0KS1/9Bkdf/P5DW/z2P1f88jtT/O4zT/zmM0/85jdP/OYzS/zmL0f86jNL/OozS/zqM0v84jNT/UW6M/6xSFf/LYBj/2Wca/+JsHf/kbyLr4XcvK+J2LwD3nVgA951ZMPuSQu78jzz/+446//uMNv/shTT/fZet/0OU2f9Dktb/Q5HW/0SS1v9xq9v/h7be/4a13f+EtNz/grPb/4Ky2/+Ds9v/ZqLV/zyM0P88jND/O4vP/zmM0v9Rbo3/qlIW/8lgGP/XaBz/4Wwd/+VvIuvjdy8r43YuAPieWwD3n1ww/JNE7vyQPv/9jz3//I05/+yGNv9+mq//RZfc/0WU1/9Ek9f/SpbY/67P6v/H2uj/wNTj/77T4v+90uL/vdLh/8XY5v+bwuH/P47S/z6N0v89jNH/O47U/1Jvjv+rUhb/yWAY/9doHP/hbR7/5XAi6+N3Lyzjdi8A+J9eAPegXzD8lUbu/ZNA//2RP//7jzv/7Ic4/4Gcsf9Hmd7/R5ba/0aW2f9MmNn/r9Dr/8bZ6P+/0+P/vdPj/7zS4v+70eH/w9jm/5zD4v9Bj9P/P47T/z+O0/88j9X/U3CP/6tTFv/JYBj/1mcb/+FtHv/lcSPr43kxLON4MQD3oF8A96FhMPyXSu78lET//ZNC//yQPf/uiTr/g52y/0ma3/9JmNv/SJfa/02Z2/+x0ez/zN7q/8XZ5//E2Of/w9fm/8LW5f/I2+n/nsXj/0CQ0/8/j9T/P4/T/z2Q1v9TcY//q1IW/8lgGP/WZxv/4W0e/+ZxJOvlejMs5XoyAPiiYQD4omIw/JlM7vyVRv/8lEX//ZNA/++KPP+En7T/S5zh/0qZ3f9Jmdz/S5nc/3ey4v+Mvub/i73m/4m75f+Hu+T/hrnk/4a5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'
icon_data = base64.b64decode(icon_b64)
image = Image.open(BytesIO(icon_data))
icon = ImageTk.PhotoImage(image)
root.iconphoto(True, icon)

VERSION = '1.0'

def ensure_config():
    if not os.path.isfile(local_path / 'wtccm.json'):
        reset_config()

def reset_config(_config = None):
    default_config = {
        'version': VERSION,
        'path': {
            'downloads': '',
            'wt': '',
            'winrar': '',
            'documents': ''
        }
    }

    with open("wtccm.json", "w", encoding="utf-8") as f:
        json.dump(default_config, f, ensure_ascii=False, indent=4)

    if _config:
        _config = load_config()

cnames = Variable()
selected_dist = StringVar()
sentmsg = StringVar()
statusmsg = StringVar()
delete_after_processing = BooleanVar()

def updateSelection(*args):
    idxs = listBox.curselection()
    sel = []
    for idx in idxs:
        sel.append(cnames.get()[idx])
    sentmsg.set(f'Selected archives: {len(sel)}')
    return sel

def proccesArchives(*args, _config):
    idxs = listBox.curselection()
    sel = []
    for idx in idxs:
        sel.append(cnames.get()[idx])
    if not sel:
        return
    dist = selected_dist.get()
    downloads_fd = get_default_downloads_folder(_config)
    move_and_extract_archive(downloads_fd, os.path.join(locate_wt(_config), dist) if dist != "UserSights\\all_tanks" else get_sights_folder(_config), sel, winrar_exe=get_default_winrar_folder(_config),delete_archive=delete_after_processing.get(), create_dir=False if selected_dist.get() == 'UserSights\\all_tanks' else True)
    update_listbox(_config)
    listBox.selection_clear(0, END)
    statusmsg.set('Archives processed.')

def locate_wt(_config: dict = None, force_registry: bool = False) -> Optional[str]:
    if not _config['path']['wt'] or force_registry:
        Registry = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        RawKey = wr.OpenKey(Registry, r"SOFTWARE\WOW6432Node\Valve\Steam")
        path = wr.QueryValueEx(RawKey, "InstallPath")[0]

        print('Located steam: ' + path)
        with open(f'{path}\\steamapps\\libraryfolders.vdf', encoding='utf-8') as file:
            steamapps_path = vdf.load(file)['libraryfolders']['1']['path']
        print('Located steamapps library: ' + steamapps_path)
        wt_path = f'{steamapps_path}\\steamapps\\common\\War Thunder\\'
        if os.path.exists(wt_path):
            print(f'Located War Thunder folder: {wt_path}')
            _config['path']['wt'] = wt_path
            save_config(_config)
            print('Saved path to config')
            return wt_path

        print('ERROR War Thunder folder not found')
        return set_wt_dir(_config)
    print('Located War Thunder folder in config file.')
    return _config['path']['wt']

def find_recent_archives(folder_path, days=3):
    """Находит архивы в папке, изменённые за последние N дней."""
    import time
    current_time = time.time()
    recent_archives = []

    # Проходим по файлам в указанной папке
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Проверяем, что это файл и он является архивом (RAR, ZIP, 7Z и т. д.)
        if os.path.isfile(file_path) and file_name.lower().endswith(('.rar', '.zip', '.7z')):
            # Получаем время последнего изменения файла
            modified_time = os.path.getmtime(file_path)

            # Проверяем, изменён ли файл за последние `days` дней
            if (current_time - modified_time) <= days * 86400:  # 86400 секунд в сутках
                recent_archives.append(file_name)

    return recent_archives

def load_config() -> dict:
    ensure_config()
    with open('wtccm.json', 'r+', encoding='utf-8') as file:
        saved_in_json = json.load(file)
    return saved_in_json

def save_config(_config: dict) -> None:
    with open('wtccm.json', 'w', encoding='utf-8') as file:
        json.dump(_config, file, indent=4, ensure_ascii=False)

def update_listbox(_config: dict) -> None:
    downloads = get_default_downloads_folder(_config)
    recent_archives = find_recent_archives(downloads, days=10)
    listBox.delete(0, 'end')
    for each_item in range(len(recent_archives)):
        listBox.insert(END, recent_archives[each_item])
        # coloring alternative lines of listbox
        listBox.itemconfig(each_item,
                           bg="white" if each_item % 2 == 0 else "lavender")

def save_default_downloads_folder(_config: dict) -> Optional[str]:
    """:returns: True if successful, else False"""
    download_folder = os.path.expanduser("~") + "\\Downloads\\"
    if os.path.exists(download_folder):
        _config['path']['downloads'] = download_folder
        save_config(_config)
        print('Default download folder saved')
        return download_folder
    print('ERROR Downloads folder not found')
    return None

def get_default_downloads_folder(_config: dict) -> str:
    if not _config['path']['downloads']:
        _config['path']['downloads'] = save_default_downloads_folder(_config)
    if os.path.exists(_config['path']['downloads']):
        return _config['path']['downloads']
    else:
        print('ERROR Downloads folder not found')
        return set_dw_dir(_config)

def get_default_winrar_folder(_config) -> str:
    if not _config['path']['winrar']:
        wr_path = os.path.join(os.environ.get("ProgramFiles"), 'WinRAR', 'WinRAR.exe')
        _config['path']['winrar'] = wr_path
        save_config(_config)
        return wr_path
    if os.path.exists(_config['path']['winrar']):
        return _config['path']['winrar']
    else:
        print('ERROR Downloads folder not found')
        return set_wr_file(_config)

def save_default_documents_folder(_config) -> str:
    CSIDL_PERSONAL = 5
    buf = ctypes.create_unicode_buffer(260)
    ctypes.windll.shell32.SHGetFolderPathW(
        None, CSIDL_PERSONAL, None, 0, buf
    )

    documents_folder = str(Path(buf.value))
    _config['path']['documents'] = documents_folder
    save_config(_config)
    return str(documents_folder)

def get_documents_folder(_config) -> str:
    if not _config['path']['documents']:
        _config['path']['documents'] = save_default_documents_folder(_config)
    if os.path.isdir(_config['path']['documents']):
        return _config['path']['documents']
    else:
        print('ERROR Documents folder not found')
        return set_dw_dir(_config)


def move_and_extract_archive(source_dir: str, destination_dir: str, archive_name: str | list, winrar_exe: str =r"C:\Program Files\WinRAR\WinRAR.exe", delete_archive: bool = True, create_dir: bool = True):
    """
    Перемещает, разархивирует и удаляет архив в определенную папку.
    """

    if not archive_name:
        return
    if isinstance(archive_name, list):
        print('\33[93m> Архивы определены как список. Выполнение рекурсии...')
        for key, archive in enumerate(archive_name):
            print(f'\33[92m{key+1}/{len(archive_name)}')
            try:
                move_and_extract_archive(source_dir, destination_dir, archive, winrar_exe, delete_archive, create_dir)
            except Exception as exc:
                print(f'\33[91mОшибка при выполнении действий с архивом {archive}:')
                print(exc)
        return
    # Формируем полные пути к архиву
    source_path = os.path.join(source_dir, archive_name)
    dest_path = os.path.join(destination_dir, archive_name)

    # Проверяем, существует ли архив в исходной папке
    if not os.path.exists(source_path):
        print(f"\33[91mАрхив \33[95m{archive_name}\33[91m не найден в папке \33[96m{source_dir}\33[91m.")
        return

    # Перемещаем архив из папки A в папку B
    try:
        shutil.move(source_path, dest_path if create_dir else destination_dir)
        print(f"\33[92mАрхив \33[95m{archive_name}\33[92m успешно перемещён из \33[96m{source_dir}\33[92m в \33[96m{destination_dir}\33[92m.")
    except Exception as e:
        print(f"\33[91mОшибка при перемещении архива: {e}")
        return

    if create_dir:
        # Создаём папку для распаковки (по названию архива, без .rar)
        extract_folder = os.path.join(destination_dir, os.path.splitext(archive_name)[0])
        os.makedirs(extract_folder, exist_ok=True)

        # Подготавливаем команду для распаковки архива в отдельную папку
    else:
        extract_folder = destination_dir
    command = [winrar_exe, 'x', dest_path, extract_folder]
    print(f'{command = }')

    # Выполняем команду распаковки
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("\33[92mРаспаковка выполнена успешно в папку:\33[96m", extract_folder)
        if result.stdout:
            print(result.stdout)

        # Если флаг delete_archive=True, удаляем архив после успешной распаковки
        if delete_archive:
            os.remove(dest_path)
            print(f"\33[93mАрхив \33[95m{archive_name} \33[93mудалён после распаковки.")

    except subprocess.CalledProcessError as e:
        print("\33[91mОшибка при распаковке архива:")
        print(e.stderr)

def get_sights_folder(_config):
    path = os.path.join(get_documents_folder(_config), "My Games\\WarThunder\\Saves\\")
    with open(os.path.join(path, "lastlogin.blk"), 'r', encoding='utf-8') as file:
        lastlogin = file.readline().removeprefix("uid:i64=").removesuffix('\n')
    path = os.path.join(path, lastlogin, "production\\UserSights\\all_tanks\\")
    return path

config = load_config()


def set_wr_file(_config):
    selected = askopenfilename(defaultextension='exe', title="Select WinRAR.exe File", initialdir=os.environ.get("ProgramFiles"), filetypes=(('Executable', 'exe',),))
    _config['path']['winrar'] = selected
    save_config(_config)
    return selected

def set_wt_dir(_config):
    selected = askdirectory(mustexist=True, title="Select War Thunder Folder", initialdir=os.path.expanduser('~'))
    _config['path']['wt'] = selected
    save_config(_config)
    return selected

def set_dw_dir(_config):
    selected = askdirectory(mustexist=True, title="Select Downloads Folder", initialdir=os.path.expanduser('~'))
    _config['path']['downloads'] = selected
    save_config(_config)
    return selected

def set_dc_dir(_config):
    selected = askdirectory(mustexist=True, title="Select Documents Folder", initialdir=os.path.expanduser('~'))
    _config['path']['documents'] = selected
    save_config(_config)
    return selected



ensure_config()

c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

listBox = Listbox(c, listvariable=cnames, height=5, width=3, selectmode='multiple')

lbl = ttk.Label(c, text="Select archives to process:")

g1 = ttk.Radiobutton(c, text='Skins/Camouflages', variable=selected_dist, value='UserSkins')
g2 = ttk.Radiobutton(c, text='Sights', variable=selected_dist, value='UserSights\\all_tanks')
g3 = ttk.Radiobutton(c, text='Missions', variable=selected_dist, value='UserMissions')

send = ttk.Button(c, text='Move & Unpack selected', command=lambda: proccesArchives(_config=config), default='active')
sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
status = ttk.Label(c, textvariable=statusmsg, anchor=W)

refreshBtn = ttk.Button(c, text='Refresh', command=lambda: update_listbox(_config=config), default='active')
tb1 = ttk.Checkbutton(c, text='Delete archive after processing?', variable=delete_after_processing, onvalue=True, offvalue=False)

selectAllBtn = ttk.Button(c, text='Select All', command=lambda: (listBox.selection_set(0, END), updateSelection()), default='active', width=10)
unselectAllBtn = ttk.Button(c, text='Unselect All', command=lambda: (listBox.selection_clear(0, END), updateSelection()), default='active', width=10)

menu = Menu(root)
file_menu = Menu(menu)
root.config(menu=menu)
menu.add_cascade(label='Debug', menu=file_menu)
file_menu.add_command(label='Reset Memory', command=lambda: reset_config(config))
file_menu.add_command(label='Set WinRAR directory', command=lambda: set_wr_file(config))
file_menu.add_command(label='Set War Thunder directory', command=lambda: set_wt_dir(config))
file_menu.add_command(label='Set Downloads folder', command=lambda: set_dw_dir(config))

open_menu_wt = Menu(menu)
menu.add_cascade(label='Open', menu=open_menu_wt)
open_menu_wt.add_command(label='UserSkins', command=lambda: os.system(f'explorer "{os.path.join(locate_wt(config), "UserSkins\\")}"'))
open_menu_wt.add_command(label='UserSights', command=lambda: os.system(f'explorer "{os.path.join(locate_wt(config), "UserSights\\")}"'))
open_menu_wt.add_command(label='UserMissions', command=lambda: os.system(f'explorer "{os.path.join(locate_wt(config), "UserMissions\\")}"'))

refreshBtn.grid(column=0, row=6, sticky=(N, W), padx=160)

selectAllBtn.grid(column=0, row=6, sticky=(N, W), ipadx=5)
unselectAllBtn.grid(column=0, row=6, sticky=(N, W), padx=80, ipadx=5)

listBox.grid(column=0, row=0, rowspan=6, sticky=(N,S,E,W), ipadx=20)
lbl.grid(column=1, row=0, padx=10, pady=5)
g1.grid(column=1, row=1, sticky=W, padx=20)
g2.grid(column=1, row=2, sticky=W, padx=20)
g3.grid(column=1, row=3, sticky=W, padx=20)
tb1.grid(column=1, row=4, sticky=W, padx=20, columnspan=2)
send.grid(column=1, row=6, sticky=(E, S))
sentlbl.grid(column=1, row=5, columnspan=2, sticky=N, pady=5, padx=5)
status.grid(column=0, row=7, columnspan=2, sticky=(W,E))
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)

listBox.bind('<<ListboxSelect>>', updateSelection)
# listBox.bind('<Double-1>', lambda *args: proccesArchives(_config=config))
# root.bind('<Return>', lambda *args: proccesArchives(_config=config))

update_listbox(config)
sentmsg.set('')
statusmsg.set('')
selected_dist.set('UserSkins')
delete_after_processing.set(True)
updateSelection()

if __name__ == '__main__':
    root.mainloop()