import request from '@/utils/request'

// 查询策略绩效指标列表
export function listReport(query) {
  return request({
    url: '/system/report/list',
    method: 'get',
    params: query
  })
}

// 查询策略绩效指标详细
export function getReport(id) {
  return request({
    url: '/system/report/' + id,
    method: 'get'
  })
}

// 新增策略绩效指标
export function addReport(data) {
  return request({
    url: '/system/report',
    method: 'post',
    data: data
  })
}

// 修改策略绩效指标
export function updateReport(data) {
  return request({
    url: '/system/report',
    method: 'put',
    data: data
  })
}

// 删除策略绩效指标
export function delReport(id) {
  return request({
    url: '/system/report/' + id,
    method: 'delete'
  })
}
