-- Q3: Find the monthly average unrealized gain/loss of portfolios for each month in 2024
USE sc2207;

SELECT 
    i.InvestorName, i.PhoneNumber, ir.PortfolioID, 
    MONTH(ugl.uglDate) AS Month,
    AVG(ugl.Amount) AS AverageUnrealizedGainLoss
FROM Investor_Record ir 
INNER JOIN Investor i ON ir.PhoneNumber = i.PhoneNumber
INNER JOIN Unrealised_Gain_Loss ugl ON ir.PortfolioID = ugl.PortfolioID
GROUP BY i.InvestorName, i.PhoneNumber, ir.PortfolioID, MONTH(ugl.UGLDate)
ORDER BY Month ASC;