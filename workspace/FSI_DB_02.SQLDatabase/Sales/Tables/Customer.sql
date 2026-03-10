CREATE TABLE [Sales].[Customer] (
    [CustomerID]   INT              IDENTITY (1, 1) NOT NULL,
    [FirstName]    NVARCHAR (50)    NOT NULL,
    [LastName]     NVARCHAR (50)    NOT NULL,
    [CompanyName]  NVARCHAR (128)   NULL,
    [EmailAddress] NVARCHAR (100)   NULL,
    [Phone]        NVARCHAR (25)    NULL,
    [RegionID]     INT              NULL,
    [rowguid]      UNIQUEIDENTIFIER CONSTRAINT [DF_Customer_rowguid] DEFAULT (newid()) NOT NULL,
    [ModifiedDate] DATETIME         CONSTRAINT [DF_Customer_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_Customer_CustomerID] PRIMARY KEY CLUSTERED ([CustomerID] ASC),
    CONSTRAINT [FK_Customer_Region_RegionID] FOREIGN KEY ([RegionID]) REFERENCES [Sales].[Region] ([RegionID]),
    CONSTRAINT [AK_Customer_rowguid] UNIQUE NONCLUSTERED ([rowguid] ASC)
);


GO

CREATE NONCLUSTERED INDEX [IX_Customer_EmailAddress]
    ON [Sales].[Customer]([EmailAddress] ASC);


GO

CREATE NONCLUSTERED INDEX [IX_Customer_RegionID]
    ON [Sales].[Customer]([RegionID] ASC);


GO

