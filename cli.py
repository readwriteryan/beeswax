#!/usr/bin/env python3

import click

from src.beeswax import Beeswax


@click.command()
@click.option(
    "--old",
    "-o",
    type=str,
    required=True,
    help="The filepath to the file containing the old create table statement",
)
@click.option(
    "--new",
    "-n",
    type=str,
    required=True,
    help="The filepath to the file containing the new create table statement",
)
def beeswax(old: str, new: str) -> bool:
    with open(old) as f:
        old_create_table = f.read()

    with open(new) as f:
        new_create_table = f.read()

    diff = Beeswax.get_hql_diff(
        Beeswax.get_table(old_create_table), Beeswax.get_table(new_create_table)
    )
    for statement in diff:
        print(statement)


if __name__ == "__main__":
    exit(0 if beeswax() else 1)
