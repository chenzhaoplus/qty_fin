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
    print(f'get_cnt_sql: {ret}')
    return ret


def get_page_sql(request, sql):
    if not request:
        raise ValueError("request must be not null")
    form_json = request.json
    page_num = form_json['pageNum'] if form_json['pageNum'] else 1
    page_size = form_json['pageSize'] if form_json['pageSize'] else 10
    order = form_json.get('order') if form_json.get('order') else 'desc'
    sort = form_json.get('sort') if form_json.get('sort') else 'cast( `公司内在价值-净利润` AS DECIMAL(20,3) )'
    ret = f'''
        select * from ({sql}) t
        order by {sort} {order}
        limit {(page_num - 1) * page_size}, {page_size}
    '''
    print(f'get_page_sql: {ret}')
    return ret
