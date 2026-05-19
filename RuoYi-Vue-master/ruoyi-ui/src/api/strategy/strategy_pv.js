import request from '@/utils/request'

// 查询私有策略列表
export function listStrategy_pv(query) {
  return request({
    url: '/strategy/strategy_pv/list',
    method: 'get',
    params: query
  })
}

// 查询私有策略详细
export function getStrategy_pv(id) {
  return request({
    url: '/strategy/strategy_pv/' + id,
    method: 'get'
  })
}

// 新增私有策略
export function addStrategy_pv(data) {
  return request({
    url: '/strategy/strategy_pv',
    method: 'post',
    data: data
  })
}

// 修改私有策略
export function updateStrategy_pv(data) {
  return request({
    url: '/strategy/strategy_pv',
    method: 'put',
    data: data
  })
}

// 删除私有策略
export function delStrategy_pv(id) {
  return request({
    url: '/strategy/strategy_pv/' + id,
    method: 'delete'
  })
}
