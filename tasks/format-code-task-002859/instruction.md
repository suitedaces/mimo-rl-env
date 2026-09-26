Inaccurate sql generation for DATEPART in T-SQL
In TSQL queries while reading DATEPART function seems to be converted to FORMAT function, which would work fine but 'quarter' does not seem to be part of [format types](https://learn.microsoft.com/en-us/dotnet/standard/base-types/custom-date-and-time-format-strings). 
Code snippet:
`quarter_query = """
SELECT
    YEAR(sale_date) AS Year,
    DATEPART(QUARTER, sale_date) AS Quarter,
    SUM(sale_price) AS QuarterlySales
FROM
    Sales_AI
GROUP BY
    YEAR(sale_date),
    DATEPART(QUARTER, sale_date)
ORDER BY
    Year, Quarter
"""
print(parse_one(quarter_query, 'tsql').sql(dialect='tsql'))
`
Output: `"SELECT YEAR(sale_date) AS Year, FORMAT(CAST(sale_date AS DATETIME2), 'quarter') AS Quarter, SUM(sale_price) AS QuarterlySales FROM Sales_AI GROUP BY YEAR(sale_date), FORMAT(CAST(sale_date AS DATETIME2), 'quarter') ORDER BY Year, Quarter"`
Worked fine when time period was month. 
Would also like to know if there are any resources for creating a custom dialect to let datepart stay as datepart after parsing.
