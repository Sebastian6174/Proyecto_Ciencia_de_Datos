from sqlalchemy import text

def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def add_primary_key(connection, schema: str, table_name: str, key_column: str):
    constraint_name = f"pk_{table_name}"
    connection.execute(text(
        f"ALTER TABLE {quote_identifier(schema)}.{quote_identifier(table_name)} "
        f"ADD CONSTRAINT {quote_identifier(constraint_name)} "
        f"PRIMARY KEY ({quote_identifier(key_column)})"
    ))


def add_foreign_key(
    connection,
    schema: str,
    table_name: str,
    column_name: str,
    referenced_table: str,
    referenced_column: str,
):
    constraint_name = f"fk_{table_name}_{column_name}"
    connection.execute(text(
        f"ALTER TABLE {quote_identifier(schema)}.{quote_identifier(table_name)} "
        f"ADD CONSTRAINT {quote_identifier(constraint_name)} "
        f"FOREIGN KEY ({quote_identifier(column_name)}) "
        f"REFERENCES {quote_identifier(schema)}.{quote_identifier(referenced_table)} "
        f"({quote_identifier(referenced_column)})"
    ))
