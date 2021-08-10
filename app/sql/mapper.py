import app.utils.constants as const


def findStockBySql():
    return f"""
        SELECT
            *
        FROM
            `{const.TABLE_PREFIX}_2021_07_31`
        WHERE
            (`最新价` <= %s or %s = '')
            AND (`总市值-数` >= %s or %s = '')
            AND (`股票名称` like %s or %s = '')
            AND (`股票代码` like %s or %s = '')
            AND (`股票类型` = %s or %s = '')
    """

# """
#             ORDER BY
#                 cast( `公司内在价值-净利润` AS DECIMAL(20,3) ) desc
#             limit %s, %s
# """
