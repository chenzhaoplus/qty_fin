SELECT
	*
FROM
	`test_stock_2021_07_14`
WHERE
	cast( `最新价` AS DECIMAL(20, 3) ) <= 30 AND cast( `总市值-数` AS DECIMAL(20, 3) ) >= 500 * 100000000
	AND `公司内在价值-净利润` <> ''
	AND `公司内在价值-营收` <> ''
-- 	AND `股票类型` = '保险'
ORDER BY
-- 	cast( `公司内在价值-营收` AS DECIMAL(20,3) ) DESC
	cast( `公司内在价值-净利润` AS DECIMAL(20,3) ) DESC
--	cast( `净资产收益率-ROE` AS DECIMAL(20,3) ) DESC
;