#!/usr/bin/env python3

from typing import Any, Dict, List, Optional

from src.exceptions.exceptions import UnsafeOperationException
from src.model.clustered_by import ClusteredBy
from src.model.column import Column
from src.model.location import Location
from src.model.row_format import RowFormat
from src.model.skewed_by import SkewedBy
from src.model.storage import Storage
from src.model.table import Table
from src.model.table_properties import TableProperties


class HQLStatement:
    """
    This class is used as a helper function for generating HQL statements
    """

    @classmethod
    def from_diff(cls, table: Table, diff: Dict[str, Any]) -> List[str]:
        """
        This method returns the set of HQL statements generated from a TableDiff

        :returns: A list of HQL statements generated from the TableDiff
        """

        statements = []
        if "partition" in diff:
            raise UnsafeOperationException(
                "Hive does not support direction modifications of partitions columns. "
                "Please see DRE team member for assistance."
            )

        if "columns" in diff:
            columns = diff.get("columns")
            if "added" in columns:
                statements.append(HQLStatement.add_columns(table, columns.get("added")))
            for column in columns.get("changed"):
                statements.append(HQLStatement.change_column(table, column))

        if "clustered_by" in diff:
            statements.append(
                HQLStatement.set_clustered_by(table, diff.get("clustered_by"))
            )

        if "location" in diff:
            statements.append(HQLStatement.set_location(table, diff.get("location")))

        if "modifier" in diff:
            statements.append(HQLStatement.set_modifier(table, diff.get("modifier")))

        if "row_format" in diff:
            statements.append(
                HQLStatement.set_row_format(table, diff.get("row_format"))
            )

        if "skewed_by" in diff:
            statements.append(HQLStatement.set_skewed_by(table, diff.get("skewed_by")))

        if "storage" in diff:
            statements.append(HQLStatement.set_storage(table, diff.get("storage")))

        if "table_properties" in diff:
            statements.append(
                HQLStatement.set_table_properties(table, diff.get("table_properties"))
            )

        return statements

    @classmethod
    def add_columns(cls, table: Table, columns: List[Column]) -> str:
        """
        This method returns the HQL for adding a column to a hive table

        :returns: The HQL for adding the column to the supplied table
        """
        column_list = ", ".join([f"{c}" for c in columns])
        return f"ALTER TABLE `{table.name}` ADD COLUMNS ({column_list});"

    @classmethod
    def change_column(cls, table: Table, column: Column) -> str:
        """
        This method returns the HQL for changing a column of a hive table

        :returns: The HQL for changing the column on the supplied table
        """
        return f"ALTER TABLE `{table.name}` CHANGE COLUMN `{column.name}` {column};"

    @classmethod
    def set_clustered_by(cls, table: Table, clustered_by: ClusteredBy) -> str:
        """
        This method returns the HQL for setting clustered_by on a hive table

        :returns: The HQL for setting the clustered_by setting of the supplied table
        """
        return f"ALTER TABLE `{table.name}` SET {clustered_by};"

    @classmethod
    def set_modifier(cls, table: Table, modifier: Optional[str]) -> str:
        """
        This method returns the HQL for changing the location of a hive table

        :returns: The HQL for changing the location of the supplied table
        """
        external = "'TRUE'" if modifier == "EXTERNAL" else "'FALSE'"
        properties = TableProperties([["'EXTERNAL'", external]])
        return f"ALTER TABLE `{table.name}` SET {properties};"

    @classmethod
    def set_location(cls, table: Table, location: Location) -> str:
        """
        This method returns the HQL for changing the location of a hive table

        :returns: The HQL for changing the location of the supplied table
        """
        return f"ALTER TABLE `{table.name}` SET {location};"

    @classmethod
    def set_row_format(cls, table: Table, row_format: RowFormat) -> str:
        """
        This method returns the HQL for changing the row format of a hive table

        :returns: The HQL for changing the row format of the supplied table
        """
        return f"ALTER TABLE `{table.name}` SET {row_format};"

    @classmethod
    def set_skewed_by(cls, table: Table, skewed_by: SkewedBy) -> str:
        """
        This method returns the HQL for changing the skewed by setting of a hive table

        :returns: The HQL for changing the skewed by setting of the supplied table
        """
        return f"ALTER TABLE `{table.name}` SET {skewed_by};"

    @classmethod
    def set_storage(cls, table: Table, storage: Storage) -> str:
        """
        This method returns the HQL for changing the storage of a hive table

        :returns: The HQL for changing the storage settings of the supplied table
        """
        return f"ALTER TABLE `{table.name}` SET {storage};"

    @classmethod
    def set_table_properties(
        cls, table: Table, table_properties: TableProperties
    ) -> str:
        """
        This method returns the HQL for changing the table properties of a hive table

        :returns: The HQL for changing the table properties of the supplied table
        """
        return f"ALTER TABLE `{table.name}` SET {table_properties};"
