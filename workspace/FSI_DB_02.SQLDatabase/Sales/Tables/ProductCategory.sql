CREATE TABLE [Sales].[ProductCategory] (
    [ProductCategoryID]       INT              IDENTITY (1, 1) NOT NULL,
    [ParentProductCategoryID] INT              NULL,
    [Name]                    NVARCHAR (50)    NOT NULL,
    [rowguid]                 UNIQUEIDENTIFIER CONSTRAINT [DF_ProductCategory_rowguid] DEFAULT (newid()) NOT NULL,
    [ModifiedDate]            DATETIME         CONSTRAINT [DF_ProductCategory_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_ProductCategory_ProductCategoryID] PRIMARY KEY CLUSTERED ([ProductCategoryID] ASC),
    CONSTRAINT [FK_ProductCategory_ProductCategory_Parent] FOREIGN KEY ([ParentProductCategoryID]) REFERENCES [Sales].[ProductCategory] ([ProductCategoryID]),
    CONSTRAINT [AK_ProductCategory_Name] UNIQUE NONCLUSTERED ([Name] ASC),
    CONSTRAINT [AK_ProductCategory_rowguid] UNIQUE NONCLUSTERED ([rowguid] ASC)
);


GO

