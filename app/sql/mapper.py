findStockBySql = """
            SELECT
                *
            FROM
                `test_stock_2021_07_31`
            WHERE
                `最新价` <= %s AND `总市值-数` >= %s
                AND `公司内在价值-净利润` <> ''
                AND `公司内在价值-营收` <> ''
        """

# """
#             ORDER BY
#                 cast( `公司内在价值-净利润` AS DECIMAL(20,3) ) desc
#             limit %s, %s
# """