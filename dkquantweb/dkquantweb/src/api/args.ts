import { get, post, put, del } from './request'

// 策略参数接口返回数据类型
export interface ArgsData {
  id: number
  fund: number
  maxPositions: number
  riskPerTrade: number
  params: Record<string, any>
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  [key: string]: any
}

// 策略参数列表查询参数
export interface ArgsQuery {
  pageNum?: number
  pageSize?: number
  [key: string]: any
}

// 策略参数列表响应
export interface ArgsListResponse {
  code: number
  msg: string
  total: number
  rows: ArgsData[]
}

// 策略参数详情响应
export interface ArgsDetailResponse {
  code: number
  msg: string
  data: ArgsData
}

// 通用响应
export interface CommonResponse {
  code: number
  msg: string
}

/**
 * 查询策略参数列表
 * @param params 查询参数
 */
export function getArgsList(params: ArgsQuery) {
  return get<ArgsListResponse>('/system/args/list', params)
}

/**
 * 获取策略参数详情
 * @param id 参数ID
 */
export function getArgsDetail(id: number) {
  return get<ArgsDetailResponse>(`/system/args/${id}`)
}

/**
 * 新增策略参数
 * @param data 参数数据
 */
export function addArgs(data: Partial<ArgsData>) {
  return post<CommonResponse>('/system/args', data)
}

/**
 * 修改策略参数
 * @param data 参数数据
 */
export function updateArgs(data: Partial<ArgsData>) {
  return put<CommonResponse>('/system/args', data)
}

/**
 * 删除策略参数
 * @param ids 参数ID，多个以逗号分隔
 */
export function deleteArgs(ids: string) {
  return del<CommonResponse>(`/system/args/${ids}`)
} 