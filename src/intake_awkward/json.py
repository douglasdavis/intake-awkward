from __future__ import annotations

from typing import TYPE_CHECKING, Any

from intake.source.base import DataSource, Schema

from intake_awkward import __version__

if TYPE_CHECKING:
    from awkward._v2.highlevel import Array as AwkwardArray
    from dask_awkward.core import Array


class JSONSource(DataSource):
    name = "awkward"
    version: str = __version__
    container: str = "awkward-array"
    partition_access: bool = True

    def __init__(
        self,
        urlpath: str | list[str],
        storage_options: dict[str, Any] | None = None,
        metadata: Any = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(metadata=metadata)
        self.urlpath = urlpath
        self.storage_options = storage_options or {}
        self._array: Array | None = None
        self.npartitions: int | None = None
        self.kwargs = kwargs

    def _get_schema(self) -> Schema:
        import dask_awkward as dak

        if self._array is None:
            self._array = dak.from_json(
                self.urlpath,
                storage_options=self.storage_options,
                **self.kwargs,
            )
            self.npartitions = self._array.npartitions

        return Schema(
            npartitions=self.npartitions,
            extra_metadata=self.metadata,
        )

    def to_dask(self) -> Array:
        self._get_schema()
        assert self._array is not None
        return self._array

    def _get_partition(self, i: int) -> AwkwardArray:
        self._get_schema()
        assert self._array is not None
        return self._array.partitions[i].compute()

    def read_partition(self, i) -> AwkwardArray:
        assert self._array is not None
        return self._get_partition(i)

    def read(self) -> AwkwardArray:
        self._get_schema()
        assert self._array is not None
        return self._array.compute()
