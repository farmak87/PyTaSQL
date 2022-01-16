call pytasql.dates4join; --when used in Tableau, this part of code to be pasted in the "Initial SQL"

SELECT d4j.PDate as pDate,
	   d4j.CDate as cDate,
	   CASE 
			WHEN x.pAmount is null THEN AVG(x.pAmount) over (partition by d4j.PDate order by d4j.PDate, d4j.CDate rows unbounded preceding)
			ELSE x.pAmount
		END as pAmount,
        CASE
			WHEN x.cAmount is null THEN 0
            ELSE x.cAmount 
		END AS cAmount,
        CASE 
			WHEN x.collDay IS NULL THEN MAX(x.collDay) OVER (partition by d4j.PDate order by d4j.PDate, d4j.CDate rows unbounded preceding) + 1
            ELSE x.collDay
		END collDay,
		CASE 
			WHEN x.CumulativeCollection IS NULL THEN MAX(x.CumulativeCollection) OVER (partition by d4j.PDate order by d4j.PDate, d4j.CDate rows unbounded preceding)
            ELSE x.CumulativeCollection
		END CumulativeCollection,
		CASE 
			WHEN x.CumulativePercentage IS NULL THEN MAX(x.CumulativePercentage) OVER (partition by d4j.PDate order by d4j.PDate, d4j.CDate rows unbounded preceding)
            ELSE x.CumulativePercentage
		END CumulativePercentage
        
FROM 	
(SELECT 
	cc.pDate as pDate,
	dd.cDate as cDate,
	cc.pAmount as pAmount,
	dd.cAmount as cAmount,
	datediff(dd.cDate, cc.pDate) AS collDay,
	dd.cAmount/cc.pAmount as percentage,
	sum(dd.cAmount) over (partition by cc.pDate order by dd.cDate) as CumulativeCollection,
	sum(dd.cAmount/cc.pAmount) over (partition by cc.pDate order by dd.cDate) as CumulativePercentage
FROM 
(SELECT 
	CAST(LOANDATETIME AS DATE) as pDate,
	SUM(LOANAMOUNT) AS pAmount
FROM 
	loanprovisionservice c 
WHERE
	c.RESULTCODE in (0)
GROUP BY 
	CAST(LOANDATETIME AS DATE)
) cc
JOIN 
(
SELECT
	CAST(c.LOANDATETIME AS DATE) as pDate,
	CAST(d.COLLECTIONDATETIME AS DATE) as cDate,
	SUM(d.LOANAMOUNT) as cAmount
FROM
	loanprovisionservice c
JOIN loancollectionservice d ON
	c.DEBTID = d.DEBTID
WHERE
	c.RESULTCODE in (0) AND 
	d.RESULTCODE in (1)
GROUP BY 
	cast(c.LOANDATETIME as date),
	cast(d.COLLECTIONDATETIME as date)
) dd 
ON cc.pDate = dd.pDate
WHERE 
	dd.cDate >= cc.pDate
) x
right join 
Dates4Join d4j
on x.pDate = d4j.PDate
and x.cDate = d4j.CDate

