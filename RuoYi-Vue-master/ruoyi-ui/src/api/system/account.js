import request from '@/utils/request'

// 查询策略账户信息列表
export function listAccount(query) {
  return request({
    url: '/system/account/list',
    method: 'get',
    params: query
  })
}

// 查询策略账户信息详细
export function getAccount(id) {
  return request({
    url: '/system/account/' + id,
    method: 'get'
  })
}

// 新增策略账户信息
export function addAccount(data) {
  return request({
    url: '/system/account',
    method: 'post',
    data: data
  })
}

// 修改策略账户信息
export function updateAccount(data) {
  return request({
    url: '/system/account',
    method: 'put',
    data: data
  })
}

// 删除策略账户信息
export function delAccount(id) {
  return request({
    url: '/system/account/' + id,
    method: 'delete'
  })
}
