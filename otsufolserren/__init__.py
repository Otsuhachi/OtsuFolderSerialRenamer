import ctypes

if ctypes.windll.shell32.IsUserAnAdmin() == 1:
    msg = f'このライブラリは重要なファイル構成を破壊する恐れがあるため、管理者権限で実行することはできません。'
    raise PermissionError(msg)
del ctypes

from .funcs import get_fm
from .orders import ORDER_ATIME, ORDER_CTIME, ORDER_MTIME, ORDER_NAME
from .serial_renamer.classes import FolderSerialRenamer
