import request from '@/utils/request'

// 查询止盈止损策略列表
export function listStrategy_profitLoss(query) {
  return request({
    url: '/strategy/strategy_profitLoss/list',
    method: 'get',
    params: query
  })
}

// 查询止盈止损策略详细
export function getStrategy_profitLoss(id) {
  return request({
    url: '/strategy/strategy_profitLoss/' + id,
    method: 'get'
  })
}

// 新增止盈止损策略
export function addStrategy_profitLoss(data) {
  return request({
    url: '/strategy/strategy_profitLoss',
    method: 'post',
    data: data
  })
}

// 修改止盈止损策略
export function updateStrategy_profitLoss(data) {
  return request({
    url: '/strategy/strategy_profitLoss',
    method: 'put',
    data: data
  })
}

// 删除止盈止损策略
export function delStrategy_profitLoss(id) {
  return request({
    url: '/strategy/strategy_profitLoss/' + id,
    method: 'delete'
  })
}
