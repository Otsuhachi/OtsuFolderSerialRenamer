import re

from pathlib import Path
from typing import Any, Callable, Generator, Literal, Optional, Protocol, Union

I_REGEX = re.compile('.*(\\{i(?:\\:.=?[1-9]\\d*[dxXb])?\\}).*')
D = Literal['d', 'D']
DF = Literal['df', 'fd', 'DF', 'FD']
F = Literal['f', 'F']
MODE = Literal[D, DF, F]
PATH = Union[str, Path]
PATH_FILTER = Callable[[Path], bool]
PATH_ORDER = Callable[[Path], 'UseableSortKey']
RENAME_PREVIEW = dict[Path, Path]


class UseableSortKey(Protocol):
    """ソートのキーとして使用可能であることを示すプロトコルです。
    """
    def __lt__(self, __other: Any) -> bool:
        ...


class TypeFM(Protocol):
    """フォルダ内のパスの変更を監視するFolderMonitoringであることを示すプロトコルです。
    """
    def __enter__(self) -> 'TypeFM':
        ...

    def __exit__(self, *ex) -> None:
        ...

    def __bool__(self) -> bool:
        ...

    def check(self) -> bool:
        """フォルダ内のパスの変更を検知します。

        Returns:
            bool: フォルダ内のパスの変更です。
        """
        ...

    def get_difference(self) -> tuple[int, list[str]]:
        """発見した変更件数と概要のリストを返します。

        ただし、一度変更を発見した場合はupdate_cache_file()されない限り新しい変更を確認できません。

        Returns:
            tuple[int, list[str]]: 件数と概要のリストです。
        """
        ...

    def iterdir(self, fltr: Optional[PATH_FILTER] = None) -> Generator[Path, None, None]:
        """このTypeFMなインスタンスが監視しているフォルダから条件に一致したパスのジェネレータを返します。

        Args:
            fltr (Optional[PATH_FILTER], optional): 条件用の関数です。指定しなければすべてのパスを返します。

        Yields:
            Generator[Path, None, None]: 条件に一致したパスのジェネレータです。
        """
        ...

    def update(self) -> None:
        """キャッシュとキャッシュファイルの更新を行います。
        """
        ...

    def update_cache(self) -> None:
        """キャッシュを更新します。

        {<Path>: (<変更日時>, <作成日時>),...}
        """
        ...

    def update_cache_file(self) -> None:
        """現在のキャッシュでキャッシュファイルを上書きします。
        """
        ...

    @property
    def cache(self) -> dict[Path, tuple[int, int]]:
        """このフォルダの最新のキャッシュです。

        Returns:
            dict[Path, tuple[int, int]]: {<Path>: (<更新日時>, <生成日時>), ...}形式の辞書です。
        """
        ...

    @property
    def cache_file(self) -> Path:
        """このTypeFMなインスタンスが管理するキャッシュファイルのパスです。

        Returns:
            Path: キャッシュファイルのパスです。
        """
        ...

    @property
    def path(self) -> Path:
        """監視するフォルダのパスです。

        Returns:
            Path: 監視するフォルダのパスです。
        """
        ...

    @property
    def paths(self) -> set[Path]:
        """このTypeFMなインスタンスが監視しているパスの一覧を返します。

        Returns:
            set[Path]: 監視しているパスの一覧です。
        """
        ...
