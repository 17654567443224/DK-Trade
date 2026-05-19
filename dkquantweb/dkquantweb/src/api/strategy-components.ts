import { get, post } from './request'

// 策略组件基础接口
export interface StrategyComponent {
  id: number
  owner: number
  fileName: string
  className: string
  funName: string
  classArgs: Record<string, any>
  funArgs: Record<string, any>
  classArgsDes: Record<string, any>
  funArgsDes: Record<string, any>
  cnClassName: string
  cnFunName: string
}

// 通用响应
export interface CommonResponse {
  code: number
  msg: string
}

// 详情响应
export interface DetailResponse<T> {
  code: number
  msg: string
  data: T
}

/**
 * 获取选股策略信息
 */
export function getSymbolSelectionDetail(id: number) {
  return get<DetailResponse<StrategyComponent>>(`/strategy/strategy_selection/${id}`)
}

/**
 * 获取选股策略功能
 */
export function getSymbolSelectionFunction(symbolSelectionId: number) {
  return post<DetailResponse<StrategyComponent>>('/strategy/fun_selection', { symbolSelectionId })
}

/**
 * 获取开仓策略信息
 */
export function getOpenPositionDetail(id: number) {
  return get<DetailResponse<StrategyComponent>>(`/strategy/strategy_position/${id}`)
}

/**
 * 获取开仓策略功能
 */
export function getOpenPositionFunction(symbolSelectionId: number) {
  return post<DetailResponse<StrategyComponent>>('/strategy/fun_position', { symbolSelectionId })
}

/**
 * 获取止盈止损策略信息
 */
export function getProfitLossDetail(id: number) {
  return get<DetailResponse<StrategyComponent>>(`/strategy/strategy_profitLoss/${id}`)
}

/**
 * 获取止盈止损策略功能
 */
export function getProfitLossFunction(profitLossId: number) {
  return post<DetailResponse<StrategyComponent>>('/strategy/fun_profitLoss', { profitLossId })
}

/**
 * 获取资金策略信息
 */
export function getFundDetail(id: number) {
  return get<DetailResponse<StrategyComponent>>(`/strategy/strategy_fund/${id}`)
}

/**
 * 获取资金策略功能
 */
export function getFundFunction(fundId: number) {
  return post<DetailResponse<StrategyComponent>>('/strategy/fun_fund', { fundId })
}

/**
 * 获取私有路径策略
 */
export function getPrivateStrategy(pvId: number) {
  return get<DetailResponse<StrategyComponent>>(`/strategy/strategy_pv/${pvId}`)
} 