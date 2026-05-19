import { get } from './request'

// 订单接口返回数据类型
export interface OrderData {
  id: number
  strategyId: number
  symbol: string
  direction: string
  entryPrice: number
  exitPrice: number
  quantity: number
  entryTime: string
  exitTime: string
  status: string
  profit: number
  profitRatio: number
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  [key: string]: any
}

// 订单列表查询参数
export interface OrderQuery {
  pageNum?: number
  pageSize?: number
  strategyId?: number
  symbol?: string
  direction?: string
  status?: string
  [key: string]: any
}

// 订单列表响应
export interface OrderListResponse {
  code: number
  msg: string
  total: number
  rows: OrderData[]
}

// 订单详情响应
export interface OrderDetailResponse {
  code: number
  msg: string
  data: OrderData
}

// 通用响应
export interface CommonResponse {
  code: number
  msg: string
}

/**
 * 查询订单列表
 * @param params 查询参数
 */
export function getOrderList(params: OrderQuery) {
  return get<OrderListResponse>('/system/orders/list', params)
}

/**
 * 获取订单详情
 * @param id 订单ID
 */
export function getOrderDetail(id: number) {
  return get<OrderDetailResponse>(`/system/orders/${id}`)
} 