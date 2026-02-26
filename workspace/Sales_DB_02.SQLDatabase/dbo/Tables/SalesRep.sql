CREATE TABLE [dbo].[SalesRep] (
    [SalesRepID]   INT           IDENTITY (1, 1) NOT NULL,
    [FirstName]    NVARCHAR (50) NOT NULL,
    [LastName]     NVARCHAR (50) NOT NULL,
    [Email]        NVARCHAR (100) NOT NULL,
    [RegionID]     INT           NOT NULL,
    [HireDate]     DATE          NOT NULL,
    [IsActive]     BIT           CONSTRAINT [DF_SalesRep_IsActive] DEFAULT ((1)) NOT NULL,
    [ModifiedDate] DATETIME      CONSTRAINT [DF_SalesRep_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_SalesRep_SalesRepID] PRIMARY KEY CLUSTERED ([SalesRepID] ASC),
    CONSTRAINT [AK_SalesRep_Email] UNIQUE NONCLUSTERED ([Email] ASC),
    CONSTRAINT [FK_SalesRep_Region_RegionID] FOREIGN KEY ([RegionID]) REFERENCES [dbo].[Region] ([RegionID])
);


GO

CREATE NONCLUSTERED INDEX [IX_SalesRep_RegionID]
    ON [dbo].[SalesRep]([RegionID] ASC);


GO

