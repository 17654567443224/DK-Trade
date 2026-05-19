import { get, post, put, del } from './request'

// 接口响应类型定义
export interface UpdatePlanListResponse {
  code: number
  msg: string
  total: number
  rows: UpdatePlan[]
}

export interface UpdatePlanResponse {
  code: number
  msg: string
  data: UpdatePlan
}

export interface CommonResponse {
  code: number
  msg: string
  data?: any
}

// 更新计划数据类型
export interface UpdatePlan {
  id: number
  title: string
  description: string
  content?: string
  status: 'planned' | 'inProgress' | 'completed'
  progress: number
  createTime: string
  updateTime?: string
  dueDate?: string
  tags?: string | string[]
  updates?: UpdateRecord[]
}

// 更新记录类型
export interface UpdateRecord {
  id: number
  planId: number
  content: string
  updateTime: string
  type?: string
}

// 查询参数类型
export interface UpdatePlanQuery {
  page?: number
  pageSize?: number
  status?: string
  sort?: string
  keyword?: string
}

/**
 * 获取更新计划列表
 * @param params 查询参数
 */
export function getUpdatePlans(params: UpdatePlanQuery) {
  return get<UpdatePlanListResponse>('/system/updatePlan/list', params)
}

/**
 * 获取更新计划详情
 * @param id 计划ID
 */
export function getUpdatePlanDetail(id: number) {
  return get<UpdatePlanResponse>(`/system/updatePlan/${id}`)
}

/**
 * 添加更新计划
 * @param data 计划数据
 */
export function addUpdatePlan(data: Partial<UpdatePlan>) {
  return post<CommonResponse>('/system/updatePlan', data)
}

/**
 * 修改更新计划
 * @param data 计划数据
 */
export function updateUpdatePlan(data: Partial<UpdatePlan>) {
  return put<CommonResponse>('/system/updatePlan', data)
}

/**
 * 删除更新计划
 * @param id 计划ID
 */
export function deleteUpdatePlan(id: number) {
  return del<CommonResponse>(`/system/updatePlan/${id}`)
}

/**
 * 添加更新记录
 * @param data 更新记录数据
 */
export function addUpdateRecord(data: Partial<UpdateRecord>) {
  return post<CommonResponse>('/system/updatePlan/record', data)
} 