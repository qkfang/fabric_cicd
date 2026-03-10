CREATE TABLE [Sales].[SalesOrderLine] (
    [SalesOrderID]      INT              NOT NULL,
    [SalesOrderLineID]  INT              IDENTITY (1, 1) NOT NULL,
    [ProductID]         INT              NOT NULL,
    [OrderQty]          SMALLINT         CONSTRAINT [DF_SalesOrderLine_OrderQty] DEFAULT ((1)) NOT NULL,
    [UnitPrice]         MONEY            NOT NULL,
    [UnitPriceDiscount] MONEY            CONSTRAINT [DF_SalesOrderLine_UnitPriceDiscount] DEFAULT ((0.00)) NOT NULL,
    [rowguid]           UNIQUEIDENTIFIER CONSTRAINT [DF_SalesOrderLine_rowguid] DEFAULT (newid()) NOT NULL,
    [ModifiedDate]      DATETIME         CONSTRAINT [DF_SalesOrderLine_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_SalesOrderLine_SalesOrderID_SalesOrderLineID] PRIMARY KEY CLUSTERED ([SalesOrderID] ASC, [SalesOrderLineID] ASC),
    CONSTRAINT [CK_SalesOrderLine_OrderQty] CHECK ([OrderQty] > (0)),
    CONSTRAINT [CK_SalesOrderLine_UnitPrice] CHECK ([UnitPrice] >= (0.00)),
    CONSTRAINT [CK_SalesOrderLine_UnitPriceDiscount] CHECK ([UnitPriceDiscount] >= (0.00)),
    CONSTRAINT [FK_SalesOrderLine_Product_ProductID] FOREIGN KEY ([ProductID]) REFERENCES [Sales].[Product] ([ProductID]),
    CONSTRAINT [FK_SalesOrderLine_SalesOrder_SalesOrderID] FOREIGN KEY ([SalesOrderID]) REFERENCES [Sales].[SalesOrder] ([SalesOrderID]) ON DELETE CASCADE,
    CONSTRAINT [AK_SalesOrderLine_rowguid] UNIQUE NONCLUSTERED ([rowguid] ASC)
);


GO

CREATE NONCLUSTERED INDEX [IX_SalesOrderLine_ProductID]
    ON [Sales].[SalesOrderLine]([ProductID] ASC);


GO

