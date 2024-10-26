# SQL Quick Reference

## 1. Basic SQL Commands
- **`SELECT`**: Retrieve data from a database.
- **`INSERT INTO`**: Add new records to a table.
- **`UPDATE`**: Modify existing records.
- **`DELETE`**: Remove records from a table.
- **`CREATE TABLE`**: Define a new table.
- **`ALTER TABLE`**: Modify an existing table (add, drop, modify columns).
- **`DROP TABLE`**: Delete a table.

## 2. Clauses
- **`WHERE`**: Filter records based on conditions.
- **`ORDER BY`**: Sort result set (ascending/descending).
- **`GROUP BY`**: Group rows with the same values.
- **`HAVING`**: Filter groups based on aggregate functions.
- **`LIMIT`**: Limit the number of records returned.
- **`DISTINCT`**: Remove duplicate values in the result set.

## 3. Joins
- **`INNER JOIN`**: Returns records with matching values in both tables.
- **`LEFT JOIN` (or LEFT OUTER JOIN)**: Returns all records from the left table and matched records from the right table.
- **`RIGHT JOIN` (or RIGHT OUTER JOIN)**: Returns all records from the right table and matched records from the left table.
- **`FULL OUTER JOIN`**: Returns all records when there is a match in either table.
- **`CROSS JOIN`**: Cartesian product of both tables.

## 4. Aggregate Functions
- **`COUNT()`**: Number of rows.
- **`SUM()`**: Sum of values.
- **`AVG()`**: Average value.
- **`MIN()` & `MAX()`**: Minimum and maximum values.

## 5. Constraints
- **`PRIMARY KEY`**: Unique identifier for each row; cannot be null.
- **`FOREIGN KEY`**: Enforces a link between two tables.
- **`UNIQUE`**: Ensures all values in a column are different.
- **`NOT NULL`**: Ensures a column cannot have a NULL value.
- **`CHECK`**: Ensures that all values in a column satisfy a specific condition.
- **`DEFAULT`**: Provides a default value for a column.

## 6. Indexes
- **`CREATE INDEX`**: Speeds up retrieval of rows by creating an index on specified columns.
- **`UNIQUE INDEX`**: Ensures all values in the index are unique.

## 7. Subqueries
- A query inside another query, used in `SELECT`, `WHERE`, and `FROM` clauses.
- **Correlated Subquery**: Refers to columns from the outer query.
- **Non-Correlated Subquery**: Independent and can be executed alone.

## 8. Common Table Expressions (CTEs)
- **Syntax**: `WITH cte_name AS (SELECT ...)`
- Temporary result set that can be referenced within a `SELECT`, `INSERT`, `UPDATE`, or `DELETE`.

## 9. Window Functions
- Used with `OVER` clause to perform calculations across a set of rows related to the current row.
- **Examples**: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`, `LEAD()`, `LAG()`, `SUM()`, `AVG()`.

## 10. Transactions
- **`BEGIN TRANSACTION`**: Start a transaction.
- **`COMMIT`**: Save all changes.
- **`ROLLBACK`**: Revert changes to the last commit.
- **ACID Properties**: Atomicity, Consistency, Isolation, Durability.

## 11. Data Types
- **Integer**: `INT`, `SMALLINT`, `TINYINT`, `BIGINT`.
- **Floating Point**: `FLOAT`, `DOUBLE`, `DECIMAL`.
- **Date/Time**: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`.
- **String**: `CHAR`, `VARCHAR`, `TEXT`.

## 12. Advanced Topics
- **Views**: Virtual tables created by a query (`CREATE VIEW`).
- **Stored Procedures**: Stored SQL code to perform operations.
- **Triggers**: Automatic actions triggered by table events (e.g., `AFTER INSERT`).

These notes cover SQL basics and provide a solid foundation for further SQL exploration!
