CREATE TABLE [dbo].[Customer] (
    [CustomerID]   INT            IDENTITY (1, 1) NOT NULL,
    [FirstName]    NVARCHAR (50)  NOT NULL,
    [LastName]     NVARCHAR (50)  NOT NULL,
    [CompanyName]  NVARCHAR (128) NULL,
    [Email]        NVARCHAR (100) NOT NULL,
    [Phone]        NVARCHAR (25)  NULL,
    [RegionID]     INT            NULL,
    [ModifiedDate] DATETIME       CONSTRAINT [DF_Customer_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_Customer_CustomerID] PRIMARY KEY CLUSTERED ([CustomerID] ASC),
    CONSTRAINT [AK_Customer_Email] UNIQUE NONCLUSTERED ([Email] ASC),
    CONSTRAINT [FK_Customer_Region_RegionID] FOREIGN KEY ([RegionID]) REFERENCES [dbo].[Region] ([RegionID])
);


GO

CREATE NONCLUSTERED INDEX [IX_Customer_Email]
    ON [dbo].[Customer]([Email] ASC);


GO

CREATE NONCLUSTERED INDEX [IX_Customer_RegionID]
    ON [dbo].[Customer]([RegionID] ASC);


GO

