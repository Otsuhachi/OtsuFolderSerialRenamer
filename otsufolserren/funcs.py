from pathlib import Path
from typing import Optional

from .cfg import MODE, PATH, PATH_FILTER, TypeFM
from .monitoring.classes import (FolderMonitoring, FolderMonitoringDir, FolderMonitoringFile)


def check_path(path: PATH, path_type: Optional[PATH_FILTER] = None, exist_only: bool = False) -> Path:
    """パスが指定した形式に従っているかを判定し、従っている場合にはそのパスのPathオブジェクトを返します。

    Args:
        path (PATH): 判定したいパスです。
        path_type (Optional[PATH_FILTER], optional): 判定用の関数です。Path.is_dirなどが使えます。
        exist_only (bool, optional): 判定結果にかかわらず、存在しなければ例外を発生させます。

    Raises:
        FileExistsError: パスが指定形式に従っていない場合に投げられます。
        FileNotFoundError: パスが存在していない場合に投げられます。

    Returns:
        Path: パスのPathオブジェクトです。
    """
    if isinstance(path, Path):
        p = path
    else:
        p = Path(path)
    p = p.resolve()
    if p.exists():
        if path_type is None:
            return p
        elif path_type(p):
            return p
        msg = f'{p}は指定した形式のパスではありません。'
        raise FileExistsError(msg)
    if exist_only:
        msg = f'{p}は存在しないパスです。'
        raise FileNotFoundError(msg)
    return p


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
    path = check_path(path, Path.is_dir, True)
    if cache_dir is None:
        cache_dir = 'monitoring_cache'
    cache_dir = check_path(cache_dir, Path.is_dir)
    if m == 'd':
        return FolderMonitoringDir(path, cache_dir)
    elif m == 'f':
        return FolderMonitoringFile(path, cache_dir)
    else:
        return FolderMonitoring(path, cache_dir)
