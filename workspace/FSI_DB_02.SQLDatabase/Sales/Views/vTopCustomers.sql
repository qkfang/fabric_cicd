CREATE VIEW [Sales].[vTopCustomers]
WITH SCHEMABINDING
AS
-- Returns total revenue and order count per customer, enabling top-N reporting.
SELECT
    c.[CustomerID],
    c.[FirstName] + ' ' + c.[LastName]  AS [CustomerName],
    c.[CompanyName],
    r.[RegionName],
    COUNT_BIG(DISTINCT so.[SalesOrderID])       AS [TotalOrders],
    SUM(so.[SubTotal])                          AS [TotalRevenue]
FROM [Sales].[Customer]    c
JOIN [Sales].[SalesOrder]  so ON c.[CustomerID]  = so.[CustomerID]
LEFT JOIN [Sales].[Region] r  ON c.[RegionID]    = r.[RegionID]
GROUP BY c.[CustomerID], c.[FirstName], c.[LastName], c.[CompanyName], r.[RegionName];


GO

