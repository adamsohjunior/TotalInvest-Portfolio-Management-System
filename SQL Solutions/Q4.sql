-- Q4: What is the top three most popular first financial goals for investors in 2024?
USE sc2207;

SELECT TOP (3) fg.GoalType, COUNT(*) AS Count
FROM Investor_Record ir
INNER JOIN Financial_Goal fg ON ir.GoalID = fg.GoalID
WHERE fg.StartDate = (
    SELECT MIN(fg2.StartDate)
    FROM Investor_Record ir2
    INNER JOIN Financial_Goal fg2 ON ir2.GoalID = fg2.GoalID
    WHERE ir2.PhoneNumber = ir.PhoneNumber
)
GROUP BY GoalType
ORDER BY COUNT(*) DESC;