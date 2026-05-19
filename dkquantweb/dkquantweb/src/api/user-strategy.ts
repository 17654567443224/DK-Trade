import { get } from './request'

// 用户策略参数
export interface UserStrategyArgs {
  id: number
  fundAmount: number // 资金额度
  maxPositions: number
  riskPerTrade: number
  pv: string // 私有路径
  symbolSelection: number // 选股策略id
  openPosition: number // 开仓策略id
  profitLoss: number // 止盈止损策略id
  fundStrategy: number // 资金策略id
  params: Record<string, any>
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  remark: string
}

// 用户策略仓位
export interface UserStrategyPosition {
  id: number
  strategyId: number
  symbol: string
  type: string
  entryPrice: string
  sz: string
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  remark: string
}

// 用户策略订单
export interface UserStrategyOrders {
  id: number
  strategyId: number
  symbol: string
  type: string
  entryPrice: string
  price: string
  sz: string
  time: string
  pnl: string
  pnlRatio: string
  exitType: string
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  remark: string
}

// 用户策略账户
export interface UserStrategyAccount {
  id: number
  balance: string
  orderFee: string
  position: UserStrategyPosition
  orders: UserStrategyOrders
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  remark: string
}

// 绩效报告
export interface StrategyReport {
  id: number
  strategyId: number
  annualizedReturn: number // 年化收益率
  maxDrawdown: number // 最大回撤
  sharpeRatio: number // 夏普比率
  winRate: number // 胜率
  profitFactor: number // 盈亏比
  totalTrades: number // 总交易次数
  profitableTrades: number // 盈利交易次数
  lossTrades: number // 亏损交易次数
  averageProfit: number // 平均盈利
  averageLoss: number // 平均亏损
  startDate: string
  endDate: string
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  remark: string
}

// 账户信息
export interface Account {
  id: number
  name: string
  balance: number
  available: number
  frozen: number
  totalProfit: number
  totalLoss: number
  netProfit: number
  winRate: number
  profitFactor: number
  maxDrawdown: number
  sharpeRatio: number
  sortinoRatio: number
  calmarRatio: number
  owner: number
  createTime: string
  updateTime: string
}

// 持仓信息
export interface Position {
  id: number
  symbol: string
  name: string
  direction: string
  volume: number
  price: number
  cost: number
  marketValue: number
  profit: number
  profitRate: number
  owner: number
  createTime: string
  updateTime: string
}

// 订单信息
export interface Order {
  id: number
  symbol: string
  name: string
  direction: string
  type: string
  volume: number
  price: number
  status: string
  owner: number
  createTime: string
  updateTime: string
}

// 绩效报告
export interface PerformanceReport {
  id: number
  totalReturn: number
  annualReturn: number
  sharpeRatio: number
  sortinoRatio: number
  calmarRatio: number
  maxDrawdown: number
  winRate: number
  profitFactor: number
  owner: number
  createTime: string
  updateTime: string
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
 * 查询用户策略参数列表
 * @param params 查询参数
 */
export function getUserStrategyArgsList(params?: any) {
  return get<ListResponse<UserStrategyArgs>>('/system/args/list', params)
}

/**
 * 获取用户策略参数详情
 * @param id 参数ID
 */
export function getUserStrategyArgsDetail(id: number) {
  return get<DetailResponse<UserStrategyArgs>>(`/system/args/${id}`)
}

/**
 * 新增用户策略参数
 * @param data 参数数据
 */
export function addUserStrategyArgs(data: Partial<UserStrategyArgs>) {
  return get<CommonResponse>('/system/args', data)
}

/**
 * 查询用户策略仓位列表
 * @param params 查询参数
 */
export function getUserStrategyPositionList(params?: any) {
  return get<ListResponse<UserStrategyPosition>>('/system/position/list', params)
}

/**
 * 获取用户策略仓位详情
 * @param id 仓位ID
 */
export function getUserStrategyPositionDetail(id: number) {
  return get<DetailResponse<UserStrategyPosition>>(`/system/position/${id}`)
}

/**
 * 查询用户策略订单列表
 * @param params 查询参数
 */
export function getUserStrategyOrdersList(params?: any) {
  return get<ListResponse<UserStrategyOrders>>('/system/orders/list', params)
}

/**
 * 获取用户策略订单详情
 * @param id 订单ID
 */
export function getUserStrategyOrdersDetail(id: number) {
  return get<DetailResponse<UserStrategyOrders>>(`/system/orders/${id}`)
}

/**
 * 查询用户策略账户列表
 * @param params 查询参数
 */
export function getUserStrategyAccountList(params?: any) {
  return get<ListResponse<UserStrategyAccount>>('/system/account/list', params)
}

/**
 * 获取用户策略账户详情
 * @param id 账户ID
 */
export function getUserStrategyAccountDetail(id: number) {
  return get<DetailResponse<UserStrategyAccount>>(`/system/account/${id}`)
}

/**
 * 查询策略绩效报告列表
 * @param params 查询参数
 */
export function getStrategyReportList(params?: any) {
  return get<ListResponse<StrategyReport>>('/system/report/list', params)
}

/**
 * 获取策略绩效报告详情
 * @param id 报告ID
 */
export function getStrategyReportDetail(id: number) {
  return get<DetailResponse<StrategyReport>>(`/system/report/${id}`)
}

/**
 * 获取账户列表
 */
export function getAccountList(owner: number) {
  return get<ListResponse<Account>>('/strategy/account/list', { owner })
}

/**
 * 获取持仓列表
 */
export function getPositionList(owner: number) {
  return get<ListResponse<Position>>('/strategy/position/list', { owner })
}

/**
 * 获取订单列表
 */
export function getOrderList(owner: number) {
  return get<ListResponse<Order>>('/strategy/order/list', { owner })
}

/**
 * 获取绩效报告
 */
export function getPerformanceReport(owner: number) {
  return get<DetailResponse<PerformanceReport>>('/strategy/report', { owner })
}

/**
 * 获取账户余额
 * @param accountId 账户ID
 */
export function getAccount(accountId: string) {
  return get<{
    code: number;
    msg: string;
    data: {
      balance: string;
      orderFee: string;
    }
  }>(`/system/account/${accountId}`)
} 