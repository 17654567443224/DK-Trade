import request from '@/utils/request'

// 查询止盈止损方法列表
export function listFun_profitLoss(query) {
  return request({
    url: '/strategy/fun_profitLoss/list',
    method: 'get',
    params: query
  })
}

// 查询止盈止损方法详细
export function getFun_profitLoss(id) {
  return request({
    url: '/strategy/fun_profitLoss/' + id,
    method: 'get'
  })
}

// 新增止盈止损方法
export function addFun_profitLoss(data) {
  return request({
    url: '/strategy/fun_profitLoss',
    method: 'post',
    data: data
  })
}

// 修改止盈止损方法
export function updateFun_profitLoss(data) {
  return request({
    url: '/strategy/fun_profitLoss',
    method: 'put',
    data: data
  })
}

// 删除止盈止损方法
export function delFun_profitLoss(id) {
  return request({
    url: '/strategy/fun_profitLoss/' + id,
    method: 'delete'
  })
}
