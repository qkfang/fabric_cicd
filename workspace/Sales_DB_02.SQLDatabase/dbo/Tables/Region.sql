CREATE TABLE [dbo].[Region] (
    [RegionID]     INT           IDENTITY (1, 1) NOT NULL,
    [Name]         NVARCHAR (50) NOT NULL,
    [CountryCode]  NCHAR (2)     NOT NULL,
    [ModifiedDate] DATETIME      CONSTRAINT [DF_Region_ModifiedDate] DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_Region_RegionID] PRIMARY KEY CLUSTERED ([RegionID] ASC),
    CONSTRAINT [AK_Region_Name] UNIQUE NONCLUSTERED ([Name] ASC)
);


GO

