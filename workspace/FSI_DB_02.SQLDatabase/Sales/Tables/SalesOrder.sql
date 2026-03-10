CREATE TABLE [Sales].[SalesOrder] (
    [SalesOrderID]   INT              CONSTRAINT [DF_SalesOrder_SalesOrderID] DEFAULT (NEXT VALUE FOR [Sales].[OrderNumber]) NOT NULL,
    [OrderDate]      DATETIME         CONSTRAINT [DF_SalesOrder_OrderDate] DEFAULT (getdate()) NOT NULL,
    [DueDate]        DATETIME         NOT NULL,
    [ShipDate]       DATETIME         NULL,
    [Status]         TINYINT          CONSTRAINT [DF_SalesOrder_Status] DEFAULT ((1)) NOT NULL,
    [CustomerID]     INT              NOT NULL,
    [ShipMethod]     NVARCHAR (50)    NOT NULL,
    [SubTotal]       MONEY            CONSTRAINT [DF_SalesOrder_SubTotal] DEFAULT ((0.00)) NOT NULL,
    [TaxAmt]         MONEY            CONSTRAINT [DF_SalesOrder_TaxAmt] DEFAULT ((0.00)) NOT NULL,
    [Freight]        MONEY            CONSTRAINT [DF_SalesOrder_Freight] DEFAULT ((0.00)) NOT NULL,
    [Comment]        NVARCHAR (MAX)   NULL,
    [rowguid]        UNIQUEIDENTIFIER CONSTRAINT [DF_SalesOrder_rowguid] DEFAULT (newid()) NOT NULL,
    [ModifiedDate]   DATETIME         CONSTRAINT [DF_SalesOrder_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_SalesOrder_SalesOrderID] PRIMARY KEY CLUSTERED ([SalesOrderID] ASC),
    CONSTRAINT [CK_SalesOrder_DueDate] CHECK ([DueDate] >= [OrderDate]),
    CONSTRAINT [CK_SalesOrder_Freight] CHECK ([Freight] >= (0.00)),
    CONSTRAINT [CK_SalesOrder_ShipDate] CHECK ([ShipDate] >= [OrderDate] OR [ShipDate] IS NULL),
    CONSTRAINT [CK_SalesOrder_Status] CHECK ([Status] >= (0) AND [Status] <= (8)),
    CONSTRAINT [CK_SalesOrder_SubTotal] CHECK ([SubTotal] >= (0.00)),
    CONSTRAINT [CK_SalesOrder_TaxAmt] CHECK ([TaxAmt] >= (0.00)),
    CONSTRAINT [FK_SalesOrder_Customer_CustomerID] FOREIGN KEY ([CustomerID]) REFERENCES [Sales].[Customer] ([CustomerID]),
    CONSTRAINT [AK_SalesOrder_rowguid] UNIQUE NONCLUSTERED ([rowguid] ASC)
);


GO

CREATE NONCLUSTERED INDEX [IX_SalesOrder_CustomerID]
    ON [Sales].[SalesOrder]([CustomerID] ASC);


GO

