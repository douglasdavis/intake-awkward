from __future__ import annotations

from typing import TYPE_CHECKING, Any

from intake.source.base import DataSource, Schema

from intake_awkward import __version__

if TYPE_CHECKING:
    import awkward as ak
    from dask_awkward.lib.core import Array


class JSONSource(DataSource):
    name = "awkward_json"
    version: str = __version__
    container: str = "awkward"
    partition_access: bool = True

    def __init__(
        self,
        urlpath: str | list[str],
        storage_options: dict[str, Any] | None = None,
        metadata: Any = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(metadata=metadata, storage_options=storage_options or {})
        self.urlpath = urlpath
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
            dtype=repr(self._array._meta),
        )

    def _get_partition(self, i: int) -> ak.Array:
        self._get_schema()
        assert self._array is not None
        return self._array.partitions[i].compute()

    def to_dask(self) -> Array:
        self._get_schema()
        assert self._array is not None
        return self._array

    def read_partition(self, i) -> ak.Array:
        assert self._array is not None
        return self._get_partition(i)

    def read(self) -> ak.Array:
        self._get_schema()
        assert self._array is not None
        return self._array.compute()

    def close(self) -> None:
        pass
