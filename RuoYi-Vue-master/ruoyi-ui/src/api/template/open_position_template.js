import request from '@/utils/request'

// 查询开仓策略模板列表
export function listOpen_position_template(query) {
  return request({
    url: '/template/open_position_template/list',
    method: 'get',
    params: query
  })
}

// 查询开仓策略模板详细
export function getOpen_position_template(id) {
  return request({
    url: '/template/open_position_template/' + id,
    method: 'get'
  })
}

// 新增开仓策略模板
export function addOpen_position_template(data) {
  return request({
    url: '/template/open_position_template',
    method: 'post',
    data: data
  })
}

// 修改开仓策略模板
export function updateOpen_position_template(data) {
  return request({
    url: '/template/open_position_template',
    method: 'put',
    data: data
  })
}

// 删除开仓策略模板
export function delOpen_position_template(id) {
  return request({
    url: '/template/open_position_template/' + id,
    method: 'delete'
  })
}
