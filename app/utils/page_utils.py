from flask import current_app as cur_app

import app.utils.constants as const


def get_page_params(request, sql):
    if not request:
        raise ValueError("request must be not null")
    form_json = request.json
    page_num = form_json['pageNum'] if form_json['pageNum'] else 1
    page_size = form_json['pageSize'] if form_json['pageSize'] else 10
    # order = form_json['order'] if form_json['order'] else 'desc'
    # sort = form_json['sort'] if form_json['sort'] else 'id'
    return [(page_num - 1) * page_size, page_size]


def get_cnt_sql(sql, cnt_key='count(1)'):
    ret = f'''
        select {cnt_key} from ({sql}) t
    '''
    # log.log_info(f'get_cnt_sql: {ret}')
    return ret


def get_page_sql(request, sql):
    if not request:
        raise ValueError("request must not be null")
    form_json = request.json
    page_num = form_json['pageNum'] if form_json['pageNum'] else 1
    page_size = form_json['pageSize'] if form_json['pageSize'] else 10
    order = form_json.get('order') if form_json.get('order') else 'desc'
    # sort = form_json.get('sort') if form_json.get('sort') else f'cast( {const.gsnzjz_jlr[1]} AS DECIMAL(20,3) )'
    sort = form_json.get('sort') if form_json.get('sort') else const.gsnzjz_jlr[1]
    sort = sort + '_d' if sort in [const.zsz[1], const.zys[1], const.zlr[1], const.jlr[1], const.zzc[1], const.zfz[1],
                                   const.gdqyhj[1]] else sort
    ret = f'''
        select * from ({sql}) t
        order by {sort} {order}
        limit {(page_num - 1) * page_size}, {page_size}
    '''
    cur_app.logger.info(f'get_page_sql: {ret}')
    return ret
