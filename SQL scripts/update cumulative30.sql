    WITH cte AS 
    (
		SELECT CUSTOMERID, sum(RECHARGEAMOUNT) AS CUMULLATIVE30
		FROM recharges
		WHERE RECHARGEDATETIME >= date_add(rechargedatetime, interval -30 day)
		GROUP BY CUSTOMERID
    )
UPDATE customers as c
inner join cte on (c.CUSTOMERID = cte.CUSTOMERID)
SET c.CUMULATIVE30DAYS  = cte.CUMULLATIVE30

    
    
    