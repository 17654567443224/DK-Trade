import request from '@/utils/request'

// 查询选股策略列表
export function listStrategy_selection(query) {
  return request({
    url: '/strategy/strategy_selection/list',
    method: 'get',
    params: query
  })
}

// 查询选股策略详细
export function getStrategy_selection(id) {
  return request({
    url: '/strategy/strategy_selection/' + id,
    method: 'get'
  })
}

// 新增选股策略
export function addStrategy_selection(data) {
  return request({
    url: '/strategy/strategy_selection',
    method: 'post',
    data: data
  })
}

// 修改选股策略
export function updateStrategy_selection(data) {
  return request({
    url: '/strategy/strategy_selection',
    method: 'put',
    data: data
  })
}

// 删除选股策略
export function delStrategy_selection(id) {
  return request({
    url: '/strategy/strategy_selection/' + id,
    method: 'delete'
  })
}
