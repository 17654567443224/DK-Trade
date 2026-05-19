import request from '@/utils/request'

// 查询开仓策略列表
export function listStrategy_position(query) {
  return request({
    url: '/strategy/strategy_position/list',
    method: 'get',
    params: query
  })
}

// 查询开仓策略详细
export function getStrategy_position(id) {
  return request({
    url: '/strategy/strategy_position/' + id,
    method: 'get'
  })
}

// 新增开仓策略
export function addStrategy_position(data) {
  return request({
    url: '/strategy/strategy_position',
    method: 'post',
    data: data
  })
}

// 修改开仓策略
export function updateStrategy_position(data) {
  return request({
    url: '/strategy/strategy_position',
    method: 'put',
    data: data
  })
}

// 删除开仓策略
export function delStrategy_position(id) {
  return request({
    url: '/strategy/strategy_position/' + id,
    method: 'delete'
  })
}
