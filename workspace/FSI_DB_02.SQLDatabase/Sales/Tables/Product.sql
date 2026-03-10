CREATE TABLE [Sales].[Product] (
    [ProductID]         INT              IDENTITY (1, 1) NOT NULL,
    [ProductNumber]     NVARCHAR (25)    NOT NULL,
    [Name]              NVARCHAR (100)   NOT NULL,
    [ProductCategoryID] INT              NULL,
    [Color]             NVARCHAR (15)    NULL,
    [Size]              NVARCHAR (5)     NULL,
    [StandardCost]      MONEY            CONSTRAINT [DF_Product_StandardCost] DEFAULT ((0.00)) NOT NULL,
    [ListPrice]         MONEY            CONSTRAINT [DF_Product_ListPrice] DEFAULT ((0.00)) NOT NULL,
    [StockQty]          INT              CONSTRAINT [DF_Product_StockQty] DEFAULT ((0)) NOT NULL,
    [rowguid]           UNIQUEIDENTIFIER CONSTRAINT [DF_Product_rowguid] DEFAULT (newid()) NOT NULL,
    [ModifiedDate]      DATETIME         CONSTRAINT [DF_Product_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_Product_ProductID] PRIMARY KEY CLUSTERED ([ProductID] ASC),
    CONSTRAINT [CK_Product_ListPrice] CHECK ([ListPrice] >= (0.00)),
    CONSTRAINT [CK_Product_StandardCost] CHECK ([StandardCost] >= (0.00)),
    CONSTRAINT [CK_Product_StockQty] CHECK ([StockQty] >= (0)),
    CONSTRAINT [FK_Product_ProductCategory_ProductCategoryID] FOREIGN KEY ([ProductCategoryID]) REFERENCES [Sales].[ProductCategory] ([ProductCategoryID]),
    CONSTRAINT [AK_Product_ProductNumber] UNIQUE NONCLUSTERED ([ProductNumber] ASC),
    CONSTRAINT [AK_Product_rowguid] UNIQUE NONCLUSTERED ([rowguid] ASC)
);


GO

