CREATE VIEW [Sales].[vSalesByCategory]
WITH SCHEMABINDING
AS
-- Returns total units sold and revenue rolled up by product category.
SELECT
    pc.[Name]                           AS [Category],
    COUNT_BIG(DISTINCT sol.[SalesOrderID]) AS [TotalOrders],
    SUM(sol.[OrderQty])                 AS [UnitsSold],
    SUM(sol.[UnitPrice] * sol.[OrderQty] * (1 - sol.[UnitPriceDiscount])) AS [NetRevenue]
FROM [Sales].[ProductCategory]   pc
JOIN [Sales].[Product]           p   ON pc.[ProductCategoryID] = p.[ProductCategoryID]
JOIN [Sales].[SalesOrderLine]    sol ON p.[ProductID]           = sol.[ProductID]
GROUP BY pc.[Name];


GO

