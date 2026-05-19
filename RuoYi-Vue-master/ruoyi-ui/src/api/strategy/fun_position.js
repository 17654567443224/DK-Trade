import request from '@/utils/request'

// 查询开仓方法列表
export function listFun_position(query) {
  return request({
    url: '/strategy/fun_position/list',
    method: 'get',
    params: query
  })
}

// 查询开仓方法详细
export function getFun_position(id) {
  return request({
    url: '/strategy/fun_position/' + id,
    method: 'get'
  })
}

// 新增开仓方法
export function addFun_position(data) {
  return request({
    url: '/strategy/fun_position',
    method: 'post',
    data: data
  })
}

// 修改开仓方法
export function updateFun_position(data) {
  return request({
    url: '/strategy/fun_position',
    method: 'put',
    data: data
  })
}

// 删除开仓方法
export function delFun_position(id) {
  return request({
    url: '/strategy/fun_position/' + id,
    method: 'delete'
  })
}
