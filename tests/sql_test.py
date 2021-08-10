from app.utils.my_pymysql import UsingMysql, init_dbconfig

with UsingMysql(db_config=init_dbconfig()) as um:
    sql = """
        SELECT
            *
        FROM
            `stock_info_2021_08_06`
        WHERE
            `最新价` <= %s 
            AND `总市值-数` >= %s
            AND `公司内在价值-净利润` <> ''
            AND `公司内在价值-营收` <> ''
        ORDER BY
            cast( `公司内在价值-净利润` AS DECIMAL(20,3) ) DESC
    """
    # pymysql 不支持 %d 参数，统一用 %s
    params = [30, 500 * 100000000]
    ret = um.fetch_all(sql, params)
    print(ret)
