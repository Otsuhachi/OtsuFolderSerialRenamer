from pathlib import Path


def ORDER_ATIME(path: Path) -> int:
    """パスのソート用関数です。最終アクセス日時でソートを行います。
    """
    return path.stat().st_atime_ns


def ORDER_CTIME(path: Path) -> int:
    """パスのソート用関数です。作成日時でソートを行います。
    """
    return path.stat().st_ctime_ns


def ORDER_MTIME(path: Path) -> int:
    """パス用のソート関数です。内容更新日時でソートを行います。
    """
    return path.stat().st_mtime_ns


def ORDER_NAME(path: Path) -> str:
    """パスのソート用関数です。名前でソートを行います。
    """
    return path.name
