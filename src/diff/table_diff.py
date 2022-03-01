#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict, OrderedDict
from typing import Any, Dict, List

from src.exceptions.exceptions import UnsafeOperationException
from src.model.table import Table
from src.model.column import Column


class TableDiff:
    """
    This class is used as a helper class to compute the difference between Hive tables.
    """

    @classmethod
    def diff(cls, old: Table, new: Table) -> Dict[str, Any]:
        """
        Compared two table objects and product a dictionary containing the
        differences between the new table and the old.

        :param old: The original Table from which to compute difference
        :param new: The new Table against which to compute differece
        """

        attributes = [
            "name",
            "comment",
            "modifier",
            "partition",
            "location",
            "clustered_by",
            "row_format",
            "skewed_by",
            "storage",
            "table_properties",
        ]

        diff = {}
        for attr in attributes:
            if getattr(old, attr) != getattr(new, attr) and getattr(new, attr):
                diff[attr] = getattr(new, attr)

        if old.columns != new.columns:
            diff["columns"] = cls.diff_columns(old.columns, new.columns)

        return diff

    @classmethod
    def diff_columns(
        cls, old: OrderedDict[str, Column], new: OrderedDict[str, Column]
    ) -> Dict[str, List[Column]]:
        if len(set(old.keys()) - set(new.keys())) > 0:
            # TODO: Hive does not support column deletion.
            # However, it should be possible to support column renames.
            # We need to be explicit about what transitions are allowed to
            # prevent unsafe operations
            raise UnsafeOperationException("Unsafe column addition operation detected")

        diff = defaultdict(list)
        for idx, name in enumerate(new.keys()):
            if old.get(name) != new.get(name):
                if old.get(name) is None:
                    # If they are adding tables to the end of the table this is a safe
                    # operation.
                    diff["added"].append(new[name])

                else:
                    diff["changed"].append(new[name])

        return diff
