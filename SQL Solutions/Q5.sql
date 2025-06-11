-- Q5: Find investors who consistently top up their investment at the beginning of every month (dollar-cost
-- averaging) in 2024 for at least one of their portfolios.
use sc2207;

SELECT DISTINCT i.InvestorName, i.PhoneNumber
FROM Investor_Record ir
INNER JOIN Investor i ON ir.PhoneNumber = i.PhoneNumber
INNER JOIN PTransaction t ON ir.PortfolioID = t.PortfolioID
-- Check for topups in 2024 where the topup is made in the first week
WHERE DAY(t.PTransactionDate) <= 7 AND YEAR(t.PTransactionDate) = 2024 AND t.PTransactionType = 'TOPUP'
-- Count transaction per investor across all portfolios
GROUP BY i.PhoneNumber, i.InvestorName
HAVING COUNT(DISTINCT MONTH(t.PTransactionDate)) = 12;