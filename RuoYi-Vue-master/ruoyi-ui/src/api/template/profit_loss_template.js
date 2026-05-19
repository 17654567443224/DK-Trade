import request from '@/utils/request'

// 查询止盈止损策略模板列表
export function listProfit_loss_template(query) {
  return request({
    url: '/template/profit_loss_template/list',
    method: 'get',
    params: query
  })
}

// 查询止盈止损策略模板详细
export function getProfit_loss_template(id) {
  return request({
    url: '/template/profit_loss_template/' + id,
    method: 'get'
  })
}

// 新增止盈止损策略模板
export function addProfit_loss_template(data) {
  return request({
    url: '/template/profit_loss_template',
    method: 'post',
    data: data
  })
}

// 修改止盈止损策略模板
export function updateProfit_loss_template(data) {
  return request({
    url: '/template/profit_loss_template',
    method: 'put',
    data: data
  })
}

// 删除止盈止损策略模板
export function delProfit_loss_template(id) {
  return request({
    url: '/template/profit_loss_template/' + id,
    method: 'delete'
  })
}
