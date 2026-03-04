CREATE TABLE [dbo].[SalesOrderItem] (
    [SalesOrderItemID]  INT   IDENTITY (1, 1) NOT NULL,
    [SalesOrderID]      INT   NOT NULL,
    [ProductID]         INT   NOT NULL,
    [OrderQty]          SMALLINT CONSTRAINT [DF_SalesOrderItem_OrderQty] DEFAULT ((1)) NOT NULL,
    [UnitPrice]         MONEY    NOT NULL,
    [UnitPriceDiscount] MONEY    CONSTRAINT [DF_SalesOrderItem_Discount] DEFAULT ((0.00)) NOT NULL,
    [ModifiedDate]      DATETIME CONSTRAINT [DF_SalesOrderItem_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_SalesOrderItem_SalesOrderItemID] PRIMARY KEY CLUSTERED ([SalesOrderItemID] ASC),
    CONSTRAINT [CK_SalesOrderItem_OrderQty] CHECK ([OrderQty] > (0)),
    CONSTRAINT [CK_SalesOrderItem_UnitPrice] CHECK ([UnitPrice] >= (0.00)),
    CONSTRAINT [CK_SalesOrderItem_Discount] CHECK ([UnitPriceDiscount] >= (0.00) AND [UnitPriceDiscount] <= (1.00)),
    CONSTRAINT [FK_SalesOrderItem_SalesOrder_SalesOrderID] FOREIGN KEY ([SalesOrderID]) REFERENCES [dbo].[SalesOrder] ([SalesOrderID]) ON DELETE CASCADE,
    CONSTRAINT [FK_SalesOrderItem_Product_ProductID] FOREIGN KEY ([ProductID]) REFERENCES [dbo].[Product] ([ProductID])
);


GO

CREATE NONCLUSTERED INDEX [IX_SalesOrderItem_SalesOrderID]
    ON [dbo].[SalesOrderItem]([SalesOrderID] ASC);


GO

CREATE NONCLUSTERED INDEX [IX_SalesOrderItem_ProductID]
    ON [dbo].[SalesOrderItem]([ProductID] ASC);


GO

