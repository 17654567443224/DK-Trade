import request from '@/utils/request'

// 查询用户策略参数信息列表
export function listArgs(query) {
  return request({
    url: '/system/args/list',
    method: 'get',
    params: query
  })
}

// 查询用户策略参数信息详细
export function getArgs(id) {
  return request({
    url: '/system/args/' + id,
    method: 'get'
  })
}

// 新增用户策略参数信息
export function addArgs(data) {
  return request({
    url: '/system/args',
    method: 'post',
    data: data
  })
}

// 修改用户策略参数信息
export function updateArgs(data) {
  return request({
    url: '/system/args',
    method: 'put',
    data: data
  })
}

// 删除用户策略参数信息
export function delArgs(id) {
  return request({
    url: '/system/args/' + id,
    method: 'delete'
  })
}
