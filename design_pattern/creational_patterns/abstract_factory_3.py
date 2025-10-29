from abc import ABC, abstractmethod

# Abstract Products: Giao diện cho DB components


class Connection(ABC):
    @abstractmethod
    def connect(self) -> str:
        pass


class QueryBuilder(ABC):
    @abstractmethod
    def build_query(self, table: str) -> str:
        pass

# Concrete Products: Cho MySQL và PostgreSQL


class MySQLConnection(Connection):
    def connect(self) -> str:
        return "Connected to MySQL database."


class PostgreSQLConnection(Connection):
    def connect(self) -> str:
        return "Connected to PostgreSQL database."


class MySQLQueryBuilder(QueryBuilder):
    def build_query(self, table: str) -> str:
        return f"SELECT * FROM {table};"  # MySQL syntax


class PostgreSQLQueryBuilder(QueryBuilder):
    def build_query(self, table: str) -> str:
        return f"SELECT * FROM \"{table}\";"  # PostgreSQL syntax (quotes)

# Abstract Factory


class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self) -> Connection:
        pass

    @abstractmethod
    def create_query_builder(self) -> QueryBuilder:
        pass

# Concrete Factories


class MySQLFactory(DatabaseFactory):
    def create_connection(self) -> Connection:
        return MySQLConnection()

    def create_query_builder(self) -> QueryBuilder:
        return MySQLQueryBuilder()


class PostgreSQLFactory(DatabaseFactory):
    def create_connection(self) -> Connection:
        return PostgreSQLConnection()

    def create_query_builder(self) -> QueryBuilder:
        return PostgreSQLQueryBuilder()

# Client: App sử dụng factory


class DataService:
    def __init__(self, factory: DatabaseFactory):
        self.factory = factory

    def perform_operation(self, table: str):
        conn = self.factory.create_connection()
        qb = self.factory.create_query_builder()
        print(conn.connect())
        print(qb.build_query(table))
        print("\n--- DB components are compatible! ---\n")

# Initialization


def main():
    db_type = "MySQL"  # Từ config
    if db_type == "MySQL":
        factory = MySQLFactory()
    elif db_type == "PostgreSQL":
        factory = PostgreSQLFactory()
    else:
        raise ValueError("Unsupported DB!")

    service = DataService(factory)
    service.perform_operation("users")


if __name__ == "__main__":
    main()
