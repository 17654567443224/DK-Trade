import { get, post, put, del } from './request'

// 策略接口返回数据类型
export interface StrategyData {
  id: number
  name: string
  category: string
  description: string
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  status: string
  [key: string]: any
}

// 策略列表查询参数
export interface StrategyQuery {
  pageNum?: number
  pageSize?: number
  name?: string
  category?: string
  status?: string
  [key: string]: any
}

// 策略列表响应
export interface StrategyListResponse {
  code: number
  msg: string
  total: number
  rows: StrategyData[]
}

// 策略详情响应
export interface StrategyDetailResponse {
  code: number
  msg: string
  data: StrategyData
}

// 通用响应
export interface CommonResponse {
  code: number
  msg: string
}

/**
 * 查询策略列表
 * @param params 查询参数
 */
export function getStrategyList(params: StrategyQuery) {
  return get<StrategyListResponse>('/system/strategy/list', params)
}

/**
 * 获取策略详情
 * @param id 策略ID
 */
export function getStrategyDetail(id: number) {
  return get<StrategyDetailResponse>(`/system/strategy/${id}`)
}

/**
 * 新增策略
 * @param data 策略数据
 */
export function addStrategy(data: Partial<StrategyData>) {
  return post<CommonResponse>('/system/strategy', data)
}

/**
 * 修改策略
 * @param data 策略数据
 */
export function updateStrategy(data: Partial<StrategyData>) {
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
 * 运行策略
 * @param data 运行参数
 */
export function runStrategy(data: { id: number, accountId: number | null, owner: number | null }) {
  return post<CommonResponse>('/system/strategy/runStrategy', data)
}

/**
 * 回测策略
 * @param data 回测参数
 */
export function backTestStrategy(data: { id: number, start: string, end: string, interval: string }) {
  return post<CommonResponse>('/system/strategy/backTesting', data)
}

/**
 * 获取策略绩效指标
 * @param data 查询参数
 */
export function getStrategyPerformance(data: { id: number, accountId?: number, owner?: number }) {
  // 确保owner有默认值
  const params = {
    id: data.id,
    owner: data.owner || 1,
    accountId: data.accountId
  }
  return post<any>('/system/strategy/operationInformation', params)
}

/**
 * 查询正在运行的策略
 * @param data 查询参数
 */
export function getRunningStrategies(data: { id: number, accountId: number, owner: number }) {
  return post<any>('/system/strategy/runningStrategies', data)
}

/**
 * 移除策略
 * @param data 移除参数
 */
export function removeStrategy(data: { id: number, accountId: number | null, owner: number | null }) {
  return post<CommonResponse>('/system/strategy/removeStrategy', data)
}

/**
 * 添加策略
 * @param data 添加参数
 */
export function addStrategyToAccount(data: { id: number, accountId: number | null, owner: number | null }) {
  return post<CommonResponse>('/system/strategy/addStrategy', data)
}

/**
 * 初始化引擎
 */
export function initEngine() {
  return get<CommonResponse>('/system/strategy/initEngine')
} 