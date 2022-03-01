#!/usr/bin/env python3
from __future__ import annotations

from collections import OrderedDict
from typing import List, Optional

from src.model.clustered_by import ClusteredBy
from src.model.column import Column
from src.model.location import Location
from src.model.row_format import RowFormat
from src.model.skewed_by import SkewedBy
from src.model.storage import Storage
from src.model.table_properties import TableProperties


class Table:
    """
    This class is used to model the representation of a Table in Hive.
    """

    def __init__(
        self,
        name: str,
        modifier: Optional[str],
        comment: Optional[str],
        partition: Optional[List[List[str]]],
    ) -> None:
        self.name = name
        self.modifier = modifier
        self.comment = comment
        self.partition = partition

        self._clustered_by: Optional[ClusteredBy] = None
        self._columns: OrderedDict[str, Column] = OrderedDict()
        self._location: Optional[Location] = None
        self._row_format: Optional[RowFormat] = None
        self._skewed_by: Optional[SkewedBy] = None
        self._storage: Optional[Storage] = None
        self._table_properties: Optional[TableProperties] = None

    def __eq__(self, other: Table) -> bool:
        """
        This method implements the magic method so that this object may be easily
        compared to other Table objects.

        :returns: The boolean result of the comparison to the other object.
        """
        return (
            self.name,
            self.modifier,
            self.comment,
            self.partition,
            self.location,
            self.columns,
            self.clustered_by,
            self.row_format,
            self.skewed_by,
            self.storage,
            self.table_properties,
        ) == (
            other.name,
            other.modifier,
            other.comment,
            other.partition,
            other.location,
            other.columns,
            other.clustered_by,
            other.row_format,
            other.skewed_by,
            other.storage,
            other.table_properties,
        )

    def __ne__(self, other: Table) -> bool:
        """
        This method implements the magic method so that this object may be easily
        compared to other Table objects.

        :returns: The boolean result of the comparison to the other object.
        """

        return not (self == other)

    def add_column(self, column: Column) -> None:
        """
        This method acts as a helper for adding columns to the Table object.

        :param column: The Column object to add to our set of Table columns
        :returns: None
        """
        self._columns.add(column)

    @property
    def clustered_by(self) -> Optional[ClusteredBy]:
        """
        This method acts as a getter for the clustered by attr of the Table object.

        :returns: A ClusteredBy object if clustered_by is set, else None
        """
        return self._clustered_by

    @clustered_by.setter
    def clustered_by(self, clustered_by: Optional[ClusteredBy]) -> None:
        """
        This method acts as a helper for setting the location of the Table object.

        :param clustered_by: The ClusteredBy object to which to set this tables attr
        :returns: None
        """
        self._clustered_by = clustered_by

    @property
    def columns(self) -> OrderedDict[str, Column]:
        """
        This method acts as a getter for the columns of the Table object.

        :returns: An OrderedDict of columns for the table
        """
        return self._columns

    @columns.setter
    def columns(self, columns: OrderedDict[str, Column]) -> None:
        """
        This method acts as a helper for setting the columns of the Table object.

        :param location: The OrderedDict of Columns to set for the Table
        :returns: None
        """
        self._columns = columns

    @property
    def location(self) -> Optional[Location]:
        """
        This method acts as a getter for the location attr of the Table object.

        :returns: A Location object if a location is set, else None.
        """
        return self._location

    @location.setter
    def location(self, location: Location) -> None:
        """
        This method acts as a helper for setting the location of the Table object.

        :param location: The Location object to which to set this tables location
        :returns: None
        """
        self._location = location

    @property
    def row_format(self) -> Optional[RowFormat]:
        """
        This method acts as a getter for the RowFormat of the Table object.

        :returns: The RowFormat object associated with the table.
        """
        return self._row_format

    @row_format.setter
    def row_format(self, row_format: Optional[RowFormat]) -> None:
        """
        This method acts as a helper for setting the RowFormat of the Table.

        :param location: The RowFormat object to set for the Table
        :returns: None
        """
        self._row_format = row_format

    @property
    def skewed_by(self) -> Optional[SkewedBy]:
        """
        This method acts as a getter for the SkewedBy of the Table object.

        :returns: The SkewedBy object associated with the table.
        """
        return self._skewed_by

    @skewed_by.setter
    def skewed_by(self, skewed_by: Optional[SkewedBy]) -> None:
        """
        This method acts as a helper for setting the SkewedBy of the Table.

        :param location: The SkewedBy object to set for the Table
        :returns: None
        """
        self._skewed_by = skewed_by

    @property
    def storage(self) -> Optional[Storage]:
        """
        This method acts as a getter for the Storage of the Table object.

        :returns: The Storage object associated with the table.
        """
        return self._storage

    @storage.setter
    def storage(self, storage: Optional[Storage]) -> None:
        """
        This method acts as a helper for setting the Storage of the Table.

        :param location: The Storage object to set for the Table
        :returns: None
        """
        self._storage = storage

    @property
    def table_properties(self) -> Optional[TableProperties]:
        """
        This method acts as a getter for the TableProperties associated with the Table.

        :returns: The TableProperties object for this table if set, else None
        """
        return self._table_properties

    @table_properties.setter
    def table_properties(self, table_properties: Optional[TableProperties]) -> None:
        """
        This method acts as a helper for setting the TableProperties associated
        with this table.

        :param location: The TableProperties of this table
        :returns: None
        """
        self._table_properties = table_properties
