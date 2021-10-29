from pathlib import Path
from typing import Optional

from otsuvalidator import CPath

from .cfg import MODE, PATH, TypeFM
from .monitoring.classes import (FolderMonitoring, FolderMonitoringDir, FolderMonitoringFile)


def check_parent_and_child(dir_: Path, path: Path) -> bool:
    """dir_がpathの先祖パスであるかを調べます。

    Args:
        dir_ (Path): 先祖パスと思わしきパスです。
        path (Path): dir_下に存在すると思わしきパスです。

    Raises:
        ValueError: dir_がフォルダではない場合に投げられます。

    Returns:
        bool: フォルダdir_の中身を調べたとき、pathが存在するかどうかです。
    """
    if not dir_.is_dir():
        msg = f'{dir_}はフォルダではありません。'
        raise ValueError(msg)
    dir_ = dir_.resolve()
    path = path.resolve()
    if dir_ == path:
        return True
    return dir_ in path.parents


def get_digit(num: int) -> int:
    """桁数を返します。

    Args:
        num (int): 桁数を調べたい整数値です。

    Returns:
        int: 桁数です。
    """
    d = 0
    while True:
        num //= 10
        d += 1
        if num == 0:
            break
    return d


def get_fm(path: PATH, mode: MODE = 'df', *, cache_dir: Optional[PATH] = None) -> TypeFM:
    """フォルダ内のパスの削除・追加を監視するTypeFMのインスタンスを生成します。

    TypeFMがどのクラスのインスタンスであるかは、modeによって決定されます。

    mode:
        F: フォルダ内のファイルのみを監視します。
        D: フォルダ内のフォルダのみを監視します。
        DF: フォルダ内のパスを監視します。

    Args:
        path (PATH): 監視するフォルダのパスです。
        mode (MODE, optional): 監視モードです。初期値は'df'です。
        cache_dir (Optional[PATH], optional): キャッシュフォルダの生成先パスです。指定しなければ'<実行フォルダ>/monitoring_cache'になります。

    Returns:
        TypeFM: MonitoringFolderとして扱えるいずれかのクラスのインスタンスです。
    """
    m = mode.lower()
    path = CPath(exist_only=True, path_type=Path.is_dir).validate(path)
    if cache_dir is None:
        cache_dir = 'monitoring_cache'
    cache_dir = CPath(path_type=Path.is_dir).validate(cache_dir)
    if m == 'd':
        return FolderMonitoringDir(path, cache_dir)
    elif m == 'f':
        return FolderMonitoringFile(path, cache_dir)
    else:
        return FolderMonitoring(path, cache_dir)
