-- Q1: Find investors who are making on average a loss across all their portfolios in 2024.
USE sc2207;

-- Compute the avg gain loss for each Investor as CTE
WITH InvestorAvgGainLoss AS (
    SELECT i.InvestorName, i.PhoneNumber, AVG(ugl.Amount) AS AverageGainLoss
    FROM Investor_Record ir
    INNER JOIN Investor i ON ir.PhoneNumber = i.PhoneNumber
    INNER JOIN Unrealised_Gain_Loss ugl ON ir.PortfolioID = ugl.PortfolioID
    WHERE YEAR(ugl.UGLDate) = '2024'
    GROUP BY i.InvestorName, i.PhoneNumber
)

-- Select from the AverageGainLoss CTE
SELECT InvestorName, PhoneNumber, AverageGainLoss
FROM InvestorAvgGainLoss
WHERE AverageGainLoss < 0
ORDER BY AverageGainLoss ASC;