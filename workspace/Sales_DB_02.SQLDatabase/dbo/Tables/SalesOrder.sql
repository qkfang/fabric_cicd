CREATE TABLE [dbo].[SalesOrder] (
    [SalesOrderID]  INT              IDENTITY (1, 1) NOT NULL,
    [CustomerID]    INT              NOT NULL,
    [SalesRepID]    INT              NULL,
    [OrderDate]     DATETIME         CONSTRAINT [DF_SalesOrder_OrderDate] DEFAULT (getdate()) NOT NULL,
    [DueDate]       DATETIME         NOT NULL,
    [ShipDate]      DATETIME         NULL,
    [Status]        TINYINT          CONSTRAINT [DF_SalesOrder_Status] DEFAULT ((1)) NOT NULL,
    [SubTotal]      MONEY            CONSTRAINT [DF_SalesOrder_SubTotal] DEFAULT ((0.00)) NOT NULL,
    [TaxAmt]        MONEY            CONSTRAINT [DF_SalesOrder_TaxAmt] DEFAULT ((0.00)) NOT NULL,
    [Freight]       MONEY            CONSTRAINT [DF_SalesOrder_Freight] DEFAULT ((0.00)) NOT NULL,
    [Comment]       NVARCHAR (MAX)   NULL,
    [ModifiedDate]  DATETIME         CONSTRAINT [DF_SalesOrder_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_SalesOrder_SalesOrderID] PRIMARY KEY CLUSTERED ([SalesOrderID] ASC),
    CONSTRAINT [CK_SalesOrder_DueDate] CHECK ([DueDate] >= [OrderDate]),
    CONSTRAINT [CK_SalesOrder_Status] CHECK ([Status] >= (0) AND [Status] <= (8)),
    CONSTRAINT [CK_SalesOrder_SubTotal] CHECK ([SubTotal] >= (0.00)),
    CONSTRAINT [CK_SalesOrder_TaxAmt] CHECK ([TaxAmt] >= (0.00)),
    CONSTRAINT [CK_SalesOrder_Freight] CHECK ([Freight] >= (0.00)),
    CONSTRAINT [FK_SalesOrder_Customer_CustomerID] FOREIGN KEY ([CustomerID]) REFERENCES [dbo].[Customer] ([CustomerID]),
    CONSTRAINT [FK_SalesOrder_SalesRep_SalesRepID] FOREIGN KEY ([SalesRepID]) REFERENCES [dbo].[SalesRep] ([SalesRepID])
);


GO

CREATE NONCLUSTERED INDEX [IX_SalesOrder_CustomerID]
    ON [dbo].[SalesOrder]([CustomerID] ASC);


GO

CREATE NONCLUSTERED INDEX [IX_SalesOrder_SalesRepID]
    ON [dbo].[SalesOrder]([SalesRepID] ASC);


GO

CREATE NONCLUSTERED INDEX [IX_SalesOrder_OrderDate]
    ON [dbo].[SalesOrder]([OrderDate] ASC);


GO

