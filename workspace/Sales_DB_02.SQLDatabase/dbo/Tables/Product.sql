CREATE TABLE [dbo].[Product] (
    [ProductID]    INT            IDENTITY (1, 1) NOT NULL,
    [Name]         NVARCHAR (100) NOT NULL,
    [SKU]          NVARCHAR (25)  NOT NULL,
    [Category]     NVARCHAR (50)  NULL,
    [UnitPrice]    MONEY          CONSTRAINT [DF_Product_UnitPrice] DEFAULT ((0.00)) NOT NULL,
    [IsActive]     BIT            CONSTRAINT [DF_Product_IsActive] DEFAULT ((1)) NOT NULL,
    [ModifiedDate] DATETIME       CONSTRAINT [DF_Product_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_Product_ProductID] PRIMARY KEY CLUSTERED ([ProductID] ASC),
    CONSTRAINT [AK_Product_SKU] UNIQUE NONCLUSTERED ([SKU] ASC),
    CONSTRAINT [CK_Product_UnitPrice] CHECK ([UnitPrice] >= (0.00))
);


GO

CREATE NONCLUSTERED INDEX [IX_Product_Category]
    ON [dbo].[Product]([Category] ASC);


GO

