-- Q7: Are male investors in their 20s making more money from their investments than their female
-- counterparts in 2024?
USE sc2207;

SELECT i.Gender, AVG(ugl.Amount) AS AverageGainLoss
FROM Investor_Record ir
INNER JOIN Investor i ON i.PhoneNumber = ir.PhoneNumber
INNER JOIN Unrealised_Gain_Loss ugl ON ugl.PortfolioID = ir.PortfolioID
AND YEAR(ugl.UGLDate) = '2024'
WHERE i.Gender IN ('M', 'F')
AND DATEDIFF(YEAR, i.DOB, GETDATE()) BETWEEN 20 AND 29
GROUP BY i.Gender;