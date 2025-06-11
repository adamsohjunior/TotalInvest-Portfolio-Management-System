-- CREATE DATABASE sc2207;
USE sc2207;

DECLARE @sql NVARCHAR(MAX) = N'';

-- Disable all foreign key constraints
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(f.parent_object_id)) 
               + '.' + QUOTENAME(OBJECT_NAME(f.parent_object_id)) 
               + ' DROP CONSTRAINT ' + QUOTENAME(f.name) + ';' + CHAR(13)
FROM sys.foreign_keys f;

EXEC sp_executesql @sql;

DROP TABLE IF EXISTS Investor;
CREATE TABLE Investor (
    PhoneNumber VARCHAR(15) PRIMARY KEY,
    InvestorName VARCHAR(255) NOT NULL,
    DoB DATE NOT NULL,
    Gender VARCHAR(1) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    RiskTolerance VARCHAR(4) NOT NULL,    
    AnnualIncome DECIMAL(15, 2) NOT NULL,
    Company VARCHAR(255) NOT NULL,

    CONSTRAINT chk_riskTolerance CHECK (RiskTolerance IN ('CONS', 'MODR', 'AGGR')),
    CONSTRAINT chk_gender CHECK (Gender IN ('M', 'F', 'O'))
);

CREATE INDEX idx_Investor_Name on Investor(InvestorName)
CREATE INDEX idx_Investor_Gender ON Investor(Gender)

DROP TABLE IF EXISTS Financial_Goal;
CREATE TABLE Financial_Goal (
    GoalID UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
    TargetAmount DECIMAL(15, 2) NOT NULL,
    TargetTimeline DATE NOT NULL,
    StartDate DATE NOT NULL,
    GoalType VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS Portfolio;
CREATE TABLE Portfolio (
    PortfolioID UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
    PortfolioStatus VARCHAR(7) NOT NULL,
    AnnualisedReturn DECIMAL(8, 2) NOT NULL,
    StartDate DATE NOT NULL,
    MarketValue DECIMAL(15, 2) NOT NULL,

    CONSTRAINT chk_Status CHECK (PortfolioStatus IN ('ACTIVE', 'CLOSED', 'INACTIVE')),
);

DROP TABLE IF EXISTS Investor_Record;
CREATE TABLE Investor_Record (
    RecordID UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
    PhoneNumber VARCHAR(15) NOT NULL,
    PortfolioID UNIQUEIDENTIFIER NOT NULL,
    GoalID UNIQUEIDENTIFIER,

    FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID) 
        ON DELETE CASCADE,
    FOREIGN KEY (PhoneNumber) REFERENCES Investor(PhoneNumber)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (GoalID) REFERENCES Financial_Goal(GoalID) ON DELETE SET NULL
);

CREATE INDEX idx_IR_Goal_ID ON Investor_Record(GoalID);
CREATE INDEX idx_IR_Portfolio_ID ON Investor_Record(PortfolioID);
CREATE INDEX idx_IR_Investor_PhoneNumber ON Investor_Record(PhoneNumber);

DROP TABLE IF EXISTS Asset_Allocation;
CREATE TABLE Asset_Allocation (
    PortfolioID UNIQUEIDENTIFIER NOT NULL,
    AssetType VARCHAR(5) NOT NULL,
    AllocationRatio DECIMAL(5, 2) NOT NULL,
    AllocatedValue DECIMAL(15, 2) NOT NULL,
    
    CONSTRAINT chk_AssetAlloc_Type CHECK (AssetType IN ('STOCK', 'BOND', 'FUND', 'COMM', 'CASH')),
    
    FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID) ON DELETE CASCADE,
    PRIMARY KEY (PortfolioID, AssetType)
);

DROP TABLE IF EXISTS Invested_Value;
CREATE TABLE Invested_Value (
    PortfolioID UNIQUEIDENTIFIER PRIMARY KEY,
    InvestedValueDate DATE NOT NULL,
    InvestedValue DECIMAL(15, 2) NOT NULL,

    CONSTRAINT chk_Value_Ge CHECK (InvestedValue >= 0),
    
    FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID) ON DELETE CASCADE,
);

DROP TABLE IF EXISTS Unrealised_Gain_Loss;
CREATE TABLE Unrealised_Gain_Loss (
    PortfolioID UNIQUEIDENTIFIER NOT NULL,
    UGLDate DATE NOT NULL,
    Amount DECIMAL(15, 2) NOT NULL,

    PRIMARY KEY (PortfolioID, UGLDate),
    FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID) ON DELETE CASCADE,
);

CREATE INDEX idx_UGL_PortfolioID ON Unrealised_Gain_Loss(PortfolioID)
CREATE INDEX idx_UGL_UGL_Date ON Unrealised_Gain_Loss(UGLDate)

DROP TABLE IF EXISTS PTransaction
CREATE TABLE PTransaction (
    TransactionID UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
    PTransactionType VARCHAR(8) NOT NULL,
    PTransactionDate DATE NOT NULL,
    Unit INT,
    PricePerUnit DECIMAL(10, 2) NOT NULL,
    PortfolioID UNIQUEIDENTIFIER NOT NULL,
    
    CONSTRAINT chk_Type CHECK (PTransactionType in ('BUY', 'SELL', 'TOPUP', 'WITHDRAW', 'FEE')),
    CONSTRAINT chk_Unit_PTrans_Ge CHECK (Unit >= 0),
    
    FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID) ON DELETE CASCADE,
);

CREATE INDEX idx_PTransaction_PTransactionDate ON PTransaction(PTransactionDate)

DROP TABLE IF EXISTS Owned_Assets;
CREATE TABLE Owned_Assets (
    OwnedAssetID UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
    Unit INT NOT NULL DEFAULT 0,
    PortfolioID UNIQUEIDENTIFIER NOT NULL,
    PurchasePrice DECIMAL(10, 2) NOT NULL,
    
    CONSTRAINT chk_Unit_OwnedA_Ge CHECK (Unit >= 0),
    
    FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID) ON DELETE CASCADE,
);

CREATE INDEX idx_Owned_Assets_PortfolioID ON Owned_Assets(PortfolioID)

DROP TABLE IF EXISTS Asset;
CREATE TABLE Asset (
    AssetID INT IDENTITY(1,1) PRIMARY KEY,
    AssetName VARCHAR(255) NOT NULL,
    Code VARCHAR(10) NOT NULL,
    AssetType VARCHAR(5) NOT NULL,

    CONSTRAINT chk_AssetType CHECK (AssetType in ('STOCK', 'BOND', 'FUND', 'COMM', 'CASH')),
);

DROP TABLE IF EXISTS Stock;
CREATE TABLE Stock (
    AssetID INT PRIMARY KEY,
    EBITDA DECIMAL(15, 2) NOT NULL,
    PERatio DECIMAL(5, 2) NOT NULL,
    EarningPerShare DECIMAL(5, 2) NOT NULL,

    FOREIGN KEY (AssetID) REFERENCES Asset(AssetID) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Bond;
CREATE TABLE Bond (
    AssetID INT PRIMARY KEY,
    InterestRate DECIMAL(5, 2) NOT NULL,
    MaturityDate DATE NOT NULL,

    FOREIGN KEY (AssetID) REFERENCES Asset(AssetID) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Fund;
CREATE TABLE Fund (
    AssetID INT PRIMARY KEY,
    ExpenseRatio DECIMAL(5, 2) NOT NULL,
    DividendYield DECIMAL(5, 2) NOT NULL,

    FOREIGN KEY (AssetID) REFERENCES Asset(AssetID) ON DELETE CASCADE
);

DROP TABLE IF EXISTS AssetPrice;
CREATE TABLE AssetPrice (
    AssetID INT,
    MarketPrice DECIMAL(10, 2) NOT NULL,
    AssetDate DATE NOT NULL,

    PRIMARY KEY (AssetID, AssetDate),
    FOREIGN KEY (AssetID) REFERENCES Asset(AssetID) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Bought_Asset_From;
CREATE TABLE Bought_Asset_From (
    OwnedAssetID UNIQUEIDENTIFIER NOT NULL,
    AssetID INT NOT NULL,
    AssetBroker VARCHAR(255) NOT NULL,
    
    FOREIGN KEY (OwnedAssetID) REFERENCES Owned_Assets(OwnedAssetID) ON DELETE CASCADE,
    FOREIGN KEY (AssetID) REFERENCES Asset(AssetID) ON DELETE SET NULL,

    PRIMARY KEY (OwnedAssetID, AssetID)
);

DROP TABLE IF EXISTS Fee_Rate_History;
CREATE TABLE Fee_Rate_History (
    FeeType VARCHAR(5) NOT NULL,
    Rate DECIMAL(10, 2) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,

    CONSTRAINT chk_FeeType CHECK (FeeType in ('TRANS', 'MGMT')),
    CONSTRAINT chk_End_Ge_Start CHECK (EndDate >= StartDate),

    PRIMARY KEY (FeeType, StartDate)
);

-- Create unique filtered index to ensure that only one TRANS and one MGMT fee
-- record can have NULL end date.
CREATE UNIQUE INDEX UX_OneNullEndDate ON Fee_Rate_History (FeeType)
WHERE EndDate IS NULL;