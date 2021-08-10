from app.utils.my_pymysql import UsingMysql, init_dbconfig

with UsingMysql(db_config=init_dbconfig()) as um:
    sql = """
        SELECT
            *
        FROM
            `stock_info_2021_08_06`
        WHERE
            zxj <= %s 
            AND zsz_d >= %s
            AND gsnzjz_jlr <> ''
            AND gsnzjz_ys <> ''
        ORDER BY
            cast( gsnzjz_jlr AS DECIMAL(20,3) ) DESC
    """
    # pymysql 不支持 %d 参数，统一用 %s
    params = [30, 500 * 100000000]
    ret = um.fetch_all(sql, params)
    print(ret)
