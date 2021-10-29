from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator, Optional, cast

from otsutil import ObjectSaver, setup_path
from otsuvalidator import CPath

from ..cfg import PATH_FILTER, TypeFM


class FM(ABC):
    """フォルダ内のパスの変更を監視するFolderMonitoringの基底クラスです。
    """
    cache: dict[Path, tuple[int, int]]
    cache_file: Path = cast(Path, CPath())
    path: Path = cast(Path, CPath(exist_only=True))

    def __enter__(self) -> TypeFM:
        return self

    def __exit__(self, *ex) -> None:
        self.update()

    def __init__(self, path: Path, cache_dir: Path) -> None:
        """パスの変更を監視を行いたいフォルダのパスを指定して、インスタンスを生成します。

        Args:
            path (Path): パスの変更を監視を行いたいフォルダのパスです。
            monitoring_cache_dir (Path): キャッシュフォルダの生成先のパスです。
        """
        self.path = path
        self.change = False
        self.cache_file = cache_dir / f'{self.path.name}.cache'
        self.diff: list[str] = []
        setup_path(self.cache_file)
        self.update_cache()
        self.check()

    def __bool__(self) -> bool:
        return self.check()

    def check(self) -> bool:
        if self.change:
            return True
        self.update_cache()
        if not self.cache_file.exists():
            self.update_cache_file()
            return False
        try:
            cache = self.cache
            old_cache: dict[Path, tuple[int, int]] = ObjectSaver(self.cache_file).load_file()
            if cache == old_cache:
                return False
            diff = self.diff
            for k, v in cache.items():
                if (ov := old_cache.get(k)) is None:
                    diff.append(f'add:\t{k}')
                    continue
                if v != ov:
                    diff.append(f'modify:\t{k}')
            if (rems := set(old_cache.keys()) - set(cache.keys())):
                for rem in rems:
                    diff.append(f'remove:\t{rem}')
            self.change = True
            return True
        except:
            self.update_cache_file()
            return False

    def get_difference(self) -> tuple[int, list[str]]:
        diff = self.diff
        return len(diff), diff

    def iterdir(self, fltr: Optional[PATH_FILTER] = None) -> Generator[Path, None, None]:
        for p in filter(fltr, self.path.iterdir()):
            yield p.resolve()

    def update(self) -> None:
        self.update_cache()
        self.update_cache_file()

    def update_cache(self) -> None:
        cache = {}
        for path in self.paths:
            stat = path.stat()
            data = stat.st_mtime_ns, stat.st_ctime_ns
            cache[path] = data
        self.cache = cache

    def update_cache_file(self) -> None:
        ObjectSaver(self.cache_file).save_file(self.cache)
        self.change = False
        self.diff = []

    @property
    @abstractmethod
    def paths(self) -> set[Path]:
        pass


class FolderMonitoringFile(FM):
    """フォルダ内のファイルの変更を監視するFolderMonitoringクラスです。
    """
    @property
    def paths(self) -> set[Path]:
        return {x for x in self.iterdir(Path.is_file)}


class FolderMonitoringDir(FM):
    """フォルダ内のフォルダの変更を監視するFolderMonitoringクラスです。
    """
    @property
    def paths(self) -> set[Path]:
        return {x for x in self.iterdir(Path.is_dir)}


class FolderMonitoring(FM):
    """フォルダ内のパスの変更を監視するFolderMonitoringクラスです。
    """
    @property
    def paths(self) -> set[Path]:
        return {x for x in self.iterdir()}
