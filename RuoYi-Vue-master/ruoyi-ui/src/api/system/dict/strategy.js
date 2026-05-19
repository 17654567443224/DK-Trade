import request from '@/utils/request'

// 查询策略模板列表
export function listStrategy(query) {
  return request({
    url: '/system/strategy/list',
    method: 'get',
    params: query
  })
}

// 查询策略模板详细
export function getStrategy(id) {
  return request({
    url: '/system/strategy/' + id,
    method: 'get'
  })
}

// 新增策略模板
export function addStrategy(data) {
  return request({
    url: '/system/strategy',
    method: 'post',
    data: data
  })
}

// 修改策略模板
export function updateStrategy(data) {
  return request({
    url: '/system/strategy',
    method: 'put',
    data: data
  })
}

// 删除策略模板
export function delStrategy(id) {
  return request({
    url: '/system/strategy/' + id,
    method: 'delete'
  })
}
