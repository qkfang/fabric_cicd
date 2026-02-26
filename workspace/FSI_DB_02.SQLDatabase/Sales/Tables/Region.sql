CREATE TABLE [Sales].[Region] (
    [RegionID]     INT              IDENTITY (1, 1) NOT NULL,
    [RegionCode]   NVARCHAR (10)    NOT NULL,
    [RegionName]   NVARCHAR (100)   NOT NULL,
    [Country]      NVARCHAR (60)    NOT NULL,
    [rowguid]      UNIQUEIDENTIFIER CONSTRAINT [DF_Region_rowguid] DEFAULT (newid()) NOT NULL,
    [ModifiedDate] DATETIME         CONSTRAINT [DF_Region_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_Region_RegionID] PRIMARY KEY CLUSTERED ([RegionID] ASC),
    CONSTRAINT [AK_Region_RegionCode] UNIQUE NONCLUSTERED ([RegionCode] ASC),
    CONSTRAINT [AK_Region_rowguid] UNIQUE NONCLUSTERED ([rowguid] ASC)
);


GO

