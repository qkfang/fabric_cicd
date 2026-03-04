-- seed_data.sql
-- Sample data for Sales_DB_02 (development / testing only).
-- Run this script once against a freshly created Sales_DB_02 database
-- to populate reference and transactional tables with realistic data.
-- ─────────────────────────────────────────────────────────────────────

-- ── Regions ──────────────────────────────────────────────────────────
SET IDENTITY_INSERT [dbo].[Region] ON;
INSERT INTO [dbo].[Region] ([RegionID], [Name], [CountryCode])
VALUES
    (1, 'North America - West',  'US'),
    (2, 'North America - East',  'US'),
    (3, 'North America - Central', 'US'),
    (4, 'Canada',                'CA'),
    (5, 'Europe - West',         'GB'),
    (6, 'Europe - Central',      'DE'),
    (7, 'Asia Pacific',          'AU');
SET IDENTITY_INSERT [dbo].[Region] OFF;
GO

-- ── Sales Representatives ─────────────────────────────────────────────
SET IDENTITY_INSERT [dbo].[SalesRep] ON;
INSERT INTO [dbo].[SalesRep] ([SalesRepID], [FirstName], [LastName], [Email], [RegionID], [HireDate])
VALUES
    (1,  'Mia',     'Torres',   'mia.torres@contoso.com',   1, '2019-03-10'),
    (2,  'Noah',    'Chen',     'noah.chen@contoso.com',    2, '2020-07-15'),
    (3,  'Olivia',  'Patel',    'olivia.patel@contoso.com', 3, '2018-11-01'),
    (4,  'Liam',    'Müller',   'liam.muller@contoso.com',  6, '2021-01-20'),
    (5,  'Emma',    'Smith',    'emma.smith@contoso.com',   5, '2017-06-05');
SET IDENTITY_INSERT [dbo].[SalesRep] OFF;
GO

-- ── Customers ─────────────────────────────────────────────────────────
SET IDENTITY_INSERT [dbo].[Customer] ON;
INSERT INTO [dbo].[Customer] ([CustomerID], [FirstName], [LastName], [CompanyName], [Email], [Phone], [RegionID])
VALUES
    (1,  'Alice',   'Chen',     'Tailspin Traders',     'alice.chen@tailspin.com',       '206-555-0201', 1),
    (2,  'Bob',     'Patel',    'Northwind Traders',    'bob.patel@northwind.com',        '425-555-0202', 2),
    (3,  'Carol',   'Smith',    'Fabrikam Inc',         'carol.smith@fabrikam.com',       '253-555-0203', 3),
    (4,  'David',   'Kim',      'Contoso Electronics',  'david.kim@contoso-elec.com',     '360-555-0204', 1),
    (5,  'Eva',     'Johnson',  'Adventure Works',      'eva.johnson@adventure.com',      '509-555-0205', 2),
    (6,  'Frank',   'Lopez',    'Fourth Coffee',        'frank.lopez@fourthcoffee.com',   '206-555-0206', 4),
    (7,  'Grace',   'Williams', 'Proseware Inc',        'grace.williams@proseware.com',   '425-555-0207', 5),
    (8,  'Henry',   'Brown',    'Woodgrove Bank',       'henry.brown@woodgrove.com',      '253-555-0208', 6),
    (9,  'Iris',    'Davis',    'Lucerne Publishing',   'iris.davis@lucerne.com',         '360-555-0209', 5),
    (10, 'James',   'Wilson',   'Graphic Design Inst',  'james.wilson@graphicdesign.com', '509-555-0210', 7);
SET IDENTITY_INSERT [dbo].[Customer] OFF;
GO

-- ── Products ─────────────────────────────────────────────────────────
SET IDENTITY_INSERT [dbo].[Product] ON;
INSERT INTO [dbo].[Product] ([ProductID], [Name], [SKU], [Category], [UnitPrice])
VALUES
    (1,  'Touring-1000 Blue, 60',     'BK-T79U-60',  'Bikes',       '2384.07'),
    (2,  'Road-650 Red, 62',          'BK-R68R-62',  'Bikes',        '782.99'),
    (3,  'Mountain-500 Silver, 52',   'BK-M18S-52',  'Bikes',        '539.99'),
    (4,  'HL Mountain Frame Black 38','FR-M94B-38',  'Components',   '1349.60'),
    (5,  'ML Road Frame Red 48',      'FR-R72R-48',  'Components',    '594.83'),
    (6,  'HL Crankset',               'CS-6583',     'Components',    '404.99'),
    (7,  'HL Mountain Seat/Saddle',   'SE-M940',     'Accessories',   '138.60'),
    (8,  'Classic Vest, M',           'VE-C304-M',   'Clothing',       '63.50'),
    (9,  'Long-Sleeve Logo Jersey, L','LJ-0192-L',   'Clothing',       '49.99'),
    (10, 'Water Bottle - 30 oz.',     'WB-H098',     'Accessories',     '4.99');
SET IDENTITY_INSERT [dbo].[Product] OFF;
GO

-- ── Sales Orders ──────────────────────────────────────────────────────
SET IDENTITY_INSERT [dbo].[SalesOrder] ON;
INSERT INTO [dbo].[SalesOrder] ([SalesOrderID], [CustomerID], [SalesRepID], [OrderDate], [DueDate], [SubTotal], [TaxAmt], [Freight], [Status])
VALUES
    (1,  1, 1, '2024-01-05', '2024-01-19', 3444.26,  275.54,  86.11, 5),
    (2,  1, 1, '2024-03-12', '2024-03-26', 2384.07,  190.73,  59.60, 5),
    (3,  2, 2, '2024-02-08', '2024-02-22', 2097.97,  167.84,  52.45, 5),
    (4,  3, 3, '2024-02-20', '2024-03-05', 1109.92,   88.79,  27.75, 5),
    (5,  3, 3, '2024-04-01', '2024-04-15', 2026.92,  162.15,  50.67, 5),
    (6,  4, 1, '2024-03-18', '2024-04-01', 1549.27,  123.94,  38.73, 5),
    (7,  5, 2, '2024-05-07', '2024-05-21', 3733.67,  298.69,  93.34, 5),
    (8,  6, 3, '2024-05-15', '2024-05-29',  829.86,   66.39,  20.75, 5),
    (9,  7, 4, '2024-06-03', '2024-06-17', 1126.82,   90.15,  28.17, 5),
    (10, 8, 4, '2024-06-22', '2024-07-06', 2384.07,  190.73,  59.60, 5),
    (11, 9, 5, '2024-07-11', '2024-07-25',  490.26,   39.22,  12.26, 5),
    (12, 10,5, '2024-08-04', '2024-08-18',  959.89,   76.79,  24.00, 5),
    (13, 1, 1, '2024-09-02', '2024-09-16', 3666.19,  293.30,  91.65, 5),
    (14, 2, 2, '2024-10-14', '2024-10-28', 2576.61,  206.13,  64.42, 5),
    (15, 5, 2, '2024-11-20', '2024-12-04', 1354.79,  108.38,  33.87, 4);
SET IDENTITY_INSERT [dbo].[SalesOrder] OFF;
GO

-- ── Sales Order Items ─────────────────────────────────────────────────
SET IDENTITY_INSERT [dbo].[SalesOrderItem] ON;
INSERT INTO [dbo].[SalesOrderItem] ([SalesOrderItemID], [SalesOrderID], [ProductID], [OrderQty], [UnitPrice], [UnitPriceDiscount])
VALUES
    (1,  1,  1, 1, 2384.07, 0.00),
    (2,  1,  2, 1,  782.99, 0.00),
    (3,  1,  7, 2,  138.60, 0.00),
    (4,  2,  1, 1, 2384.07, 0.00),
    (5,  3,  2, 2,  782.99, 0.00),
    (6,  3,  6, 1,  404.99, 0.00),
    (7,  3,  8, 2,   63.50, 0.00),
    (8,  4,  3, 2,  539.99, 0.00),
    (9,  4, 10, 6,    4.99, 0.00),
    (10, 5,  4, 1, 1349.60, 0.05),
    (11, 5,  5, 1,  594.83, 0.00),
    (12, 5,  9, 3,   49.99, 0.00),
    (13, 6,  2, 1,  782.99, 0.00),
    (14, 6,  5, 1,  594.83, 0.00),
    (15, 6,  8, 3,   63.50, 0.10),
    (16, 7,  1, 1, 2384.07, 0.00),
    (17, 7,  4, 1, 1349.60, 0.00),
    (18, 8,  3, 1,  539.99, 0.00),
    (19, 8,  9, 5,   49.99, 0.00),
    (20, 8, 10, 8,    4.99, 0.00),
    (21, 9,  5, 1,  594.83, 0.00),
    (22, 9,  6, 1,  404.99, 0.00),
    (23, 9,  8, 2,   63.50, 0.00),
    (24,10,  1, 1, 2384.07, 0.00),
    (25,11,  9, 4,   49.99, 0.00),
    (26,11, 10,20,    4.99, 0.00),
    (27,11,  8, 3,   63.50, 0.00),
    (28,12,  2, 1,  782.99, 0.00),
    (29,12,  8, 2,   63.50, 0.00),
    (30,12, 10,10,    4.99, 0.00),
    (31,13,  1, 1, 2384.07, 0.00),
    (32,13,  4, 1, 1349.60, 0.05),
    (33,14,  2, 2,  782.99, 0.00),
    (34,14,  5, 1,  594.83, 0.00),
    (35,14,  7, 3,  138.60, 0.00),
    (36,15,  3, 2,  539.99, 0.00),
    (37,15,  9, 4,   49.99, 0.00),
    (38,15, 10,15,    4.99, 0.00);
SET IDENTITY_INSERT [dbo].[SalesOrderItem] OFF;
GO
