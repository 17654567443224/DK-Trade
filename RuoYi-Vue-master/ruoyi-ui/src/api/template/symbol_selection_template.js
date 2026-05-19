import request from '@/utils/request'

// 查询选股策略模板列表
export function listSymbol_selection_template(query) {
  return request({
    url: '/template/symbol_selection_template/list',
    method: 'get',
    params: query
  })
}

// 查询选股策略模板详细
export function getSymbol_selection_template(id) {
  return request({
    url: '/template/symbol_selection_template/' + id,
    method: 'get'
  })
}

// 新增选股策略模板
export function addSymbol_selection_template(data) {
  return request({
    url: '/template/symbol_selection_template',
    method: 'post',
    data: data
  })
}

// 修改选股策略模板
export function updateSymbol_selection_template(data) {
  return request({
    url: '/template/symbol_selection_template',
    method: 'put',
    data: data
  })
}

// 删除选股策略模板
export function delSymbol_selection_template(id) {
  return request({
    url: '/template/symbol_selection_template/' + id,
    method: 'delete'
  })
}
