import request from '@/utils/request'

// 查询策略订单信息列表
export function listOrders(query) {
  return request({
    url: '/system/orders/list',
    method: 'get',
    params: query
  })
}

// 查询策略订单信息详细
export function getOrders(id) {
  return request({
    url: '/system/orders/' + id,
    method: 'get'
  })
}

// 新增策略订单信息
export function addOrders(data) {
  return request({
    url: '/system/orders',
    method: 'post',
    data: data
  })
}

// 修改策略订单信息
export function updateOrders(data) {
  return request({
    url: '/system/orders',
    method: 'put',
    data: data
  })
}

// 删除策略订单信息
export function delOrders(id) {
  return request({
    url: '/system/orders/' + id,
    method: 'delete'
  })
}
