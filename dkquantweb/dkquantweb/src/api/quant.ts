import { get, post, put, del } from './request'

// 策略接口返回数据类型
export interface Strategy {
  id: number
  strategyName: string
  owner: number
  accountId: number
  maxPosition: number
  argsId: number
  delFlag: string
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  remark: string
}

// 策略业务对象
export interface StrategyBO {
  id: number
  owner: number
  accountId: number
}

// 回测业务对象
export interface BackTestingBO {
  id: number
  symbol: string
  interval: string
  start: string
  end: string
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
 * 查询策略列表
 * @param params 查询参数
 */
export function getStrategyList(params?: any) {
  return get<ListResponse<Strategy>>('/system/strategy/list', params)
}

/**
 * 获取策略详情
 * @param id 策略ID
 */
export function getStrategyDetail(id: number) {
  return get<DetailResponse<Strategy>>(`/system/strategy/${id}`)
}

/**
 * 新增策略
 * @param data 策略数据
 */
export function addStrategy(data: Partial<Strategy>) {
  return post<CommonResponse>('/system/strategy', data)
}

/**
 * 修改策略
 * @param data 策略数据
 */
export function updateStrategy(data: Partial<Strategy>) {
  return put<CommonResponse>('/system/strategy', data)
}

/**
 * 删除策略
 * @param ids 策略ID，多个以逗号分隔
 */
export function deleteStrategy(ids: string) {
  return del<CommonResponse>(`/system/strategy/${ids}`)
}

/**
 * 初始化引擎
 */
export function initEngine() {
  return get<CommonResponse>('/system/strategy/initEngine')
}

/**
 * 添加策略到账户
 * @param data 策略业务对象
 */
export function addStrategyToAccount(data: StrategyBO) {
  return post<CommonResponse>('/system/strategy/addStrategy', data)
}

/**
 * 运行策略
 * @param data 策略业务对象
 */
export function runStrategy(data: StrategyBO) {
  return post<CommonResponse>('/system/strategy/runStrategy', data)
}

/**
 * 移除策略
 * @param data 策略业务对象
 */
export function removeStrategy(data: StrategyBO) {
  return post<CommonResponse>('/system/strategy/removeStrategy', data)
}

/**
 * 获取绩效指标
 * @param strategyId 策略ID
 * @param owner 归属（默认为1）
 * @param accountId 本金账户ID
 */
export function getStrategyPerformance(strategyId: number, accountId?: number, owner: number = 1) {
  return post<any>('/system/strategy/operationInformation', { 
    id: strategyId,
    owner,
    accountId
  })
}

/**
 * 回测策略
 * @param data 回测业务对象
 */
export function backTestStrategy(data: BackTestingBO) {
  return post<CommonResponse>('/system/strategy/backTesting', data)
}

/**
 * 查询正在运行的策略
 * @param strategyId 策略ID
 */
export function getRunningStrategies(strategyId: number) {
  return post<{ code: number; message: string; data: number[] }>('/system/strategy/runningStrategies', { id: strategyId })
} 