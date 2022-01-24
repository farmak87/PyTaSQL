CREATE DEFINER=`root`@`localhost` PROCEDURE `update_cumulativeTopUP90`()
BEGIN

    WITH cte AS 
    (
		SELECT CUSTOMERID, sum(RECHARGEAMOUNT) AS CUMULLATIVE90
		FROM recharges
		WHERE RECHARGEDATETIME >= date_add(rechargedatetime, interval -90 day)
		GROUP BY CUSTOMERID
    )
	UPDATE customers as c
	inner join cte on (c.CUSTOMERID = cte.CUSTOMERID)
	SET c.CUMULATIVE90DAYS  = cte.CUMULLATIVE90
    #where c.CUMULATIVE90DAYS < CUMULATIVE30DAYS
;
END