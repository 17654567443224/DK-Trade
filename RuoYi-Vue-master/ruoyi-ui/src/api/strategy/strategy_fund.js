import request from '@/utils/request'

// 查询资金策略列表
export function listStrategy_fund(query) {
  return request({
    url: '/strategy/strategy_fund/list',
    method: 'get',
    params: query
  })
}

// 查询资金策略详细
export function getStrategy_fund(id) {
  return request({
    url: '/strategy/strategy_fund/' + id,
    method: 'get'
  })
}

// 新增资金策略
export function addStrategy_fund(data) {
  return request({
    url: '/strategy/strategy_fund',
    method: 'post',
    data: data
  })
}

// 修改资金策略
export function updateStrategy_fund(data) {
  return request({
    url: '/strategy/strategy_fund',
    method: 'put',
    data: data
  })
}

// 删除资金策略
export function delStrategy_fund(id) {
  return request({
    url: '/strategy/strategy_fund/' + id,
    method: 'delete'
  })
}
