import request from '@/utils/request'

// 查询测试用列表
export function listTest(query) {
  return request({
    url: '/test/test/list',
    method: 'get',
    params: query
  })
}

// 查询测试用详细
export function getTest(id) {
  return request({
    url: '/test/test/' + id,
    method: 'get'
  })
}

// 新增测试用
export function addTest(data) {
  return request({
    url: '/test/test',
    method: 'post',
    data: data
  })
}

// 修改测试用
export function updateTest(data) {
  return request({
    url: '/test/test',
    method: 'put',
    data: data
  })
}

// 删除测试用
export function delTest(id) {
  return request({
    url: '/test/test/' + id,
    method: 'delete'
  })
}
