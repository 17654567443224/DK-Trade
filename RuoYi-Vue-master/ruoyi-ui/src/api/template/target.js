import request from '@/utils/request'

// 查询指标列表
export function listTarget(query) {
  return request({
    url: '/template/target/list',
    method: 'get',
    params: query
  })
}

// 查询指标详细
export function getTarget(id) {
  return request({
    url: '/template/target/' + id,
    method: 'get'
  })
}

// 新增指标
export function addTarget(data) {
  return request({
    url: '/template/target',
    method: 'post',
    data: data
  })
}

// 修改指标
export function updateTarget(data) {
  return request({
    url: '/template/target',
    method: 'put',
    data: data
  })
}

// 删除指标
export function delTarget(id) {
  return request({
    url: '/template/target/' + id,
    method: 'delete'
  })
}
