import app.utils.constants as const


def findStockBySql(table_name='stock_info_2021_07_31'):
    return f"""
            SELECT
                *
            FROM
                {table_name}
            WHERE 1=1
                AND (gpmc like %s or %s = '')
                AND (gpdm like %s or %s = '')
                AND (gplx = %s or %s = '')
                AND (zxj >= %s or %s is null)
                AND (zxj <= %s or %s is null)
                AND (zsz_d >= %s or %s is null)
                AND (zsz_d <= %s or %s is null) 
        """


def findGplxAll():
    return f"""
        select distinct gplx from `{const.TABLE_PREFIX}_2021_07_31`
        where 1=1
            and (gplx like %s or %s = '') 
    """


def findStockTable():
    return f"""
        SELECT
            table_name 
        FROM
            information_schema.TABLES 
        WHERE 1=1
            and table_schema = 'python_crawl' 
            AND table_name LIKE %s
            and (table_name like %s or %s = '') 
        ORDER BY table_name desc
    """

# """
#             ORDER BY
#                 cast( `公司内在价值-净利润` AS DECIMAL(20,3) ) desc
#             limit %s, %s
# """
