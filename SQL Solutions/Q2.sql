-- Q2: Find investors who are seeing an annualized return of more than 10% from their portfolios in 2024.
USE sc2207;

SELECT DISTINCT i.InvestorName, i.PhoneNumber, p.AnnualisedReturn
FROM Investor_Record ir
INNER JOIN Investor i ON ir.PhoneNumber = i.PhoneNumber
INNER JOIN Portfolio p ON ir.PortfolioID = p.PortfolioID
WHERE p.AnnualisedReturn > 10;

