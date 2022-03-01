#!/usr/bin/env python3

from typing import List

from src.diff.table_diff import TableDiff
from src.hql.hql_statement import HQLStatement
from src.parser.hql_parser import HQLParser
from src.model.table import Table


class Beeswax:
    """
    This class implements the entry point for the Beeswax system
    """

    @classmethod
    def get_table(cls, hql: str) -> Table:
        """
        This function takes an HQL CREATE TABLE statement and returns a Table object

        :return The Table object generated from the create table statement
        """
        return HQLParser().parse_create_table(hql)

    @classmethod
    def get_hql_diff(cls, old: Table, new: Table) -> List[str]:
        """
        This class returns the list of HQL statements to modify the supplied
        old table into the new table.

        :param old: The table from which we are generating a diff
        :param new: The table against which to generate a diff
        :return: The list of HQL statements required to migrate the old to new
        """
        return HQLStatement.from_diff(new, TableDiff.diff(old, new))
