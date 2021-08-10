import app.utils.constants as const


def findStockBySql():
    return f"""
            SELECT
                *
            FROM
                `{const.TABLE_PREFIX}_2021_07_31`
            WHERE 1=1
                AND (zxj <= %s or %s = '')
                AND (zsz_d >= %s or %s = '')
                AND (gpmc like %s or %s = '')
                AND (gpdm like %s or %s = '')
                AND (gplx = %s or %s = '')
        """


def findGplxAll():
    return f"""
        select distinct gplx from `{const.TABLE_PREFIX}_2021_07_31`
        where 1=1
            and (gplx like %s or %s = '') 
    """

# """
#             ORDER BY
#                 cast( `公司内在价值-净利润` AS DECIMAL(20,3) ) desc
#             limit %s, %s
# """
