-- Q6: Find the most popular financial goals for investors working in the same company and whose age is
-- between 30 to 40 years old.
USE sc2207;

WITH RankedGoals AS (
    SELECT 
        i2.Company, 
        fg2.GoalType, 
        COUNT(*) AS GoalCount,
        RANK() OVER (PARTITION BY i2.Company ORDER BY COUNT(*) DESC) AS RankNum
    FROM Financial_Goal fg2
    JOIN Investor_Record ir2 ON fg2.GoalID = ir2.GoalID
    JOIN Investor i2 ON ir2.PhoneNumber = i2.PhoneNumber
    WHERE DATEDIFF(YEAR, i2.DoB, GETDATE()) BETWEEN 30 AND 40
    GROUP BY i2.Company, fg2.GoalType
)

SELECT Company, GoalType, GoalCount
FROM RankedGoals
WHERE RankNum = 1
ORDER BY GoalCount DESC;


