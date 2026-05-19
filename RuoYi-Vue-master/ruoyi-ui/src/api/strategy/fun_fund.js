import request from '@/utils/request'

// 查询资金方法列表
export function listFun_fund(query) {
  return request({
    url: '/strategy/fun_fund/list',
    method: 'get',
    params: query
  })
}

// 查询资金方法详细
export function getFun_fund(id) {
  return request({
    url: '/strategy/fun_fund/' + id,
    method: 'get'
  })
}

// 新增资金方法
export function addFun_fund(data) {
  return request({
    url: '/strategy/fun_fund',
    method: 'post',
    data: data
  })
}

// 修改资金方法
export function updateFun_fund(data) {
  return request({
    url: '/strategy/fun_fund',
    method: 'put',
    data: data
  })
}

// 删除资金方法
export function delFun_fund(id) {
  return request({
    url: '/strategy/fun_fund/' + id,
    method: 'delete'
  })
}
