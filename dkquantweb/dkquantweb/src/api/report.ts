import { get } from './request'

// 绩效报告接口返回数据类型
export interface ReportData {
  id: number
  strategyId: number
  annualizedReturn: number
  maxDrawdown: number
  sharpeRatio: number
  winRate: number
  profitFactor: number
  totalTrades: number
  profitableTrades: number
  lossTrades: number
  averageProfit: number
  averageLoss: number
  startDate: string
  endDate: string
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  [key: string]: any
}

// 绩效报告列表查询参数
export interface ReportQuery {
  pageNum?: number
  pageSize?: number
  strategyId?: number
  [key: string]: any
}

// 绩效报告列表响应
export interface ReportListResponse {
  code: number
  msg: string
  total: number
  rows: ReportData[]
}

// 绩效报告详情响应
export interface ReportDetailResponse {
  code: number
  msg: string
  data: ReportData
}

// 通用响应
export interface CommonResponse {
  code: number
  msg: string
}

/**
 * 查询绩效报告列表
 * @param params 查询参数
 */
export function getReportList(params: ReportQuery) {
  return get<ReportListResponse>('/system/report/list', params)
}

/**
 * 获取绩效报告详情
 * @param id 报告ID
 */
export function getReportDetail(id: number) {
  return get<ReportDetailResponse>(`/system/report/${id}`)
} 