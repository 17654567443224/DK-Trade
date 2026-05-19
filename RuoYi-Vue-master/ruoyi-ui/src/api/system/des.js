import request from '@/utils/request'

// 查询策略描述列表
export function listDes(query) {
  return request({
    url: '/system/des/list',
    method: 'get',
    params: query
  })
}

// 查询策略描述详细
export function getDes(id) {
  return request({
    url: '/system/des/' + id,
    method: 'get'
  })
}

// 新增策略描述
export function addDes(data) {
  return request({
    url: '/system/des',
    method: 'post',
    data: data
  })
}

// 修改策略描述
export function updateDes(data) {
  return request({
    url: '/system/des',
    method: 'put',
    data: data
  })
}

// 删除策略描述
export function delDes(id) {
  return request({
    url: '/system/des/' + id,
    method: 'delete'
  })
}
