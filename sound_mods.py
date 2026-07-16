import wtccm
from pathlib import Path
from typing import Optional
config = wtccm.load_config()

wt_path = Path(wtccm.locate_wt(config))

def toggle_enable_mod(wt_path: Path, forcevalue: Optional[bool] = None) -> bool:
    """Toggles the enable_mod in config.blk and returns current value."""
    path = wt_path / 'config.blk'
    original_cfg = path.read_text(encoding='utf-8')
    if forcevalue is None:
        cfg = original_cfg.replace('enable_mod:b=no', 'enable_mod:b=yes')
        if original_cfg == cfg:
            cfg = cfg.replace('enable_mod:b=yes', 'enable_mod:b=no')
            path.write_text(cfg, encoding="utf-8")
            return False
        path.write_text(cfg, encoding="utf-8")
        return True

    elif forcevalue:
        cfg = original_cfg.replace('enable_mod:b=no', 'enable_mod:b=yes')
        path.write_text(cfg, encoding="utf-8")
        return True

    else:
        cfg = original_cfg.replace('enable_mod:b=yes', 'enable_mod:b=no')
        path.write_text(cfg, encoding="utf-8")
        return False

def process_sound_archive(*args, _config):
    pass
#wip