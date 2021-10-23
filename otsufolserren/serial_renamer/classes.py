from pathlib import Path
from typing import Generator, Optional

from ..cfg import I_REGEX, PATH_FILTER, PATH_ORDER, RENAME_PREVIEW, TypeFM
from ..funcs import get_digit


class FolderSerialRenamer:
    """フォルダ内のパスを連番リネームするクラスです。
    """
    def __enter__(self) -> 'FolderSerialRenamer':
        return self

    def __exit__(self, *ex) -> None:
        self.update()

    def __init__(self, fm: TypeFM, name_template: Optional[str] = None, order: Optional[PATH_ORDER] = None) -> None:
        """監視するフォルダ、名前のテンプレート、並び順を決める関数を渡して、FolderSerialRenamerインスタンスを生成します。

        Args:
            fm (TypeFM): 監視するフォルダのFolderMonitoringインスタンスです。
            name_template (Optional[str], optional): 名前のテンプレートです。"{i:03d}"など整数iに対するフォーマット(ただし右寄せ限定)を指定することができます。指定しなければ末尾に{i:0<対象の桁数>d}が指定されます。
            order (Optional[PATH_ORDER], optional): 並び順を決める関数です。
        """
        self.fm = fm
        self.name_template = name_template
        self.order = order

    def __bool__(self) -> bool:
        return self.check()

    def check(self) -> bool:
        """フォルダ内のパスの変更を検知します。

        Returns:
            bool: フォルダ内のパスの変更です。
        """
        return self.fm.check()

    def get_difference(self) -> tuple[int, list[str]]:
        """発見した変更件数と概要のリストを返します。

        ただし、一度変更を発見した場合はupdate_cache_file()されない限り新しい変更を確認できません。

        Returns:
            tuple[int, list[str]]: 件数と概要のリストです。
        """
        return self.fm.get_difference()

    def get_preview(self) -> RENAME_PREVIEW:
        """リネームのプレビューを取得します。

        Returns:
            RENAME_PREVIEW: {<元のパス>: <リネーム後のパス>, ...}です。
        """
        mf = self.fm
        order = self.order
        paths = mf.paths
        dirs = sorted(filter(Path.is_dir, paths), key=order)
        files = sorted(filter(Path.is_file, paths), key=order)
        digit_dir = get_digit(len(dirs))
        digit_file = get_digit(len(files))
        ntmp = self.name_template
        if ntmp is None:
            ntmp_dir = f'{{i:0{digit_dir}d}}'
            ntmp_file = f'{{i:0{digit_file}d}}'
        else:
            if I_REGEX.match(ntmp):
                ntmp_dir = ntmp
                ntmp_file = ntmp
            else:
                ntmp_dir = f'{ntmp}{{i:0{digit_dir}d}}'
                ntmp_file = f'{ntmp}{{i:0{digit_file}d}}'
        prev = {}
        for i, d in enumerate(dirs):
            i += 1
            np = (d.with_name(ntmp_dir.format(i=i))).resolve()
            prev[d] = np
        for i, f in enumerate(files):
            i += 1
            np = (f.with_stem(ntmp_file.format(i=i))).resolve()
            prev[f] = np
        return prev

    def iterdir(self, fltr: Optional[PATH_FILTER] = None) -> Generator[Path, None, None]:
        """監視しているフォルダから条件に一致したパスのジェネレータを返します。

        Args:
            fltr (Optional[PATH_FILTER], optional): 条件用の関数です。指定しなければすべてのパスを返します。

        Yields:
            Generator[Path, None, None]: 条件に一致したパスのジェネレータです。
        """
        yield from self.fm.iterdir(fltr)

    def rename(self, only_when_change: bool = True, *, preview: Optional[RENAME_PREVIEW] = None) -> None:
        """リネームを実行します。

        Args:
            only_when_change (bool, optional): フォルダに変更を発見したときのみリネームを実行します。
            preview (Optional[RENAME_PREVIEW], optional): リネームのプレビューです。基本的にself.get_preview()で取得した値以外を渡さないでください。
        """
        mf = self.fm
        if only_when_change and not mf:
            return
        if preview is None:
            preview = self.get_preview()
        laters: RENAME_PREVIEW = {}
        for k, v in preview.items():
            if k == v:
                continue
            if v in preview:
                name = k.stem
                suffix = k.suffix
                np = (k.parent / f'{name}(1){suffix}').resolve()
                cur = 1
                paths = mf.paths
                while np in paths:
                    cur += 1
                    np = (k.parent / f'{name}({cur}){suffix}').resolve()
                k.rename(np)
                laters[np] = v
            else:
                k.rename(v)
        for k, v in laters.items():
            k.rename(v)
        self.update()

    def update(self) -> None:
        """キャッシュとキャッシュファイルを更新します。
        """
        self.fm.update()

    def update_cache(self) -> None:
        """キャッシュを更新します。

        {<Path>: (<変更日時>, <作成日時>),...}
        """
        self.fm.update_cache()

    def update_cache_file(self) -> None:
        """現在のキャッシュでキャッシュファイルを上書きします。
        """
        self.fm.update_cache_file()

    @property
    def cache(self) -> dict[Path, tuple[int, int]]:
        """このフォルダの最新のキャッシュです。

        Returns:
            dict[Path, tuple[int, int]]: {<Path>: (<更新日時>, <生成日時>), ...}形式の辞書です。
        """
        return self.fm.cache

    @property
    def cache_file(self) -> Path:
        """このTypeFMなインスタンスが管理するキャッシュファイルのパスです。

        Returns:
            Path: キャッシュファイルのパスです。
        """
        return self.fm.cache_file

    @property
    def path(self) -> Path:
        """監視するフォルダのパスです。

        Returns:
            Path: 監視するフォルダのパスです。
        """
        return self.fm.path

    @property
    def paths(self) -> set[Path]:
        """このTypeFMなインスタンスが監視しているパスの一覧を返します。

        Returns:
            set[Path]: 監視しているパスの一覧です。
        """
        return self.fm.paths
