import request from '@/utils/request'

// 查询资金策略模板列表
export function listFund_template(query) {
  return request({
    url: '/template/fund_template/list',
    method: 'get',
    params: query
  })
}

// 查询资金策略模板详细
export function getFund_template(id) {
  return request({
    url: '/template/fund_template/' + id,
    method: 'get'
  })
}

// 新增资金策略模板
export function addFund_template(data) {
  return request({
    url: '/template/fund_template',
    method: 'post',
    data: data
  })
}

// 修改资金策略模板
export function updateFund_template(data) {
  return request({
    url: '/template/fund_template',
    method: 'put',
    data: data
  })
}

// 删除资金策略模板
export function delFund_template(id) {
  return request({
    url: '/template/fund_template/' + id,
    method: 'delete'
  })
}
