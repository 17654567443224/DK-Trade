import { get } from './request'

// 模板基础接口
export interface Template {
  id: number
  fileName: string
  className: string
  funName: string
  classArgs: Record<string, any>
  funArgs: Record<string, any>
  classArgsDes: Record<string, any>
  funArgsDes: Record<string, any>
  cnClassName: string
  cnFunName: string
  owner: number
}

// 选股策略模板
export interface SymbolSelectionTemplate {
  id: number
  name: string
  description: string
  className: string
  args: Record<string, any>
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  remark: string
}

// 开仓策略模板
export interface OpenPositionTemplate {
  id: number
  name: string
  description: string
  className: string
  args: Record<string, any>
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  remark: string
}

// 止盈止损策略模板
export interface ProfitLossTemplate {
  id: number
  name: string
  description: string
  className: string
  args: Record<string, any>
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  remark: string
}

// 资金策略模板
export interface FundTemplate {
  id: number
  name: string
  description: string
  className: string
  args: Record<string, any>
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  remark: string
}

// 指标方法
export interface TargetMethod {
  id: number
  methodName: string
  parameters: Record<string, any>
  parametersDes: Record<string, any>
  owner: number
}

// 通用响应
export interface CommonResponse {
  code: number
  msg: string
}

// 列表响应
export interface ListResponse<T> {
  code: number
  msg: string
  total: number
  rows: T[]
}

// 详情响应
export interface DetailResponse<T> {
  code: number
  msg: string
  data: T
}

/**
 * 查询选股策略模板列表
 */
export function getSymbolSelectionTemplates(owner: number = 1) {
  return get<ListResponse<Template>>('/template/symbol_selection_template/list', { owner })
}

/**
 * 查询开仓策略模板列表
 */
export function getOpenPositionTemplates(owner: number = 1) {
  return get<ListResponse<Template>>('/template/open_position_template/list', { owner })
}

/**
 * 查询止盈止损策略模板列表
 */
export function getProfitLossTemplates(owner: number = 1) {
  return get<ListResponse<Template>>('/template/profit_loss_template/list', { owner })
}

/**
 * 查询资金策略模板列表
 */
export function getFundTemplates(owner: number = 1) {
  return get<ListResponse<Template>>('/template/fund_template/list', { owner })
}

/**
 * 获取目标方法列表
 */
export function getTargetMethods(owner: number = 1) {
  return get<ListResponse<TargetMethod>>('/template/target/list', { owner })
}

export default {
  getSymbolSelectionTemplates,
  getOpenPositionTemplates,
  getProfitLossTemplates,
  getFundTemplates,
  getTargetMethods
} 