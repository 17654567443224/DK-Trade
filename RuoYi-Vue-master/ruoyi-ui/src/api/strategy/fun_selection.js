import request from '@/utils/request'

// 查询选股方法列表
export function listFun_selection(query) {
  return request({
    url: '/strategy/fun_selection/list',
    method: 'get',
    params: query
  })
}

// 查询选股方法详细
export function getFun_selection(id) {
  return request({
    url: '/strategy/fun_selection/' + id,
    method: 'get'
  })
}

// 新增选股方法
export function addFun_selection(data) {
  return request({
    url: '/strategy/fun_selection',
    method: 'post',
    data: data
  })
}

// 修改选股方法
export function updateFun_selection(data) {
  return request({
    url: '/strategy/fun_selection',
    method: 'put',
    data: data
  })
}

// 删除选股方法
export function delFun_selection(id) {
  return request({
    url: '/strategy/fun_selection/' + id,
    method: 'delete'
  })
}
