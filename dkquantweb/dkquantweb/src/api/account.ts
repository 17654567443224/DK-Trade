import { get, post, put, del } from './request'

// 账户接口返回数据类型
export interface AccountData {
  id: number
  balance: string
  name: string
  type: string
  status: string
  createBy: string
  createTime: string
  updateBy: string
  updateTime: string
  [key: string]: any
}

// 账户列表查询参数
export interface AccountQuery {
  pageNum?: number
  pageSize?: number
  name?: string
  type?: string
  status?: string
  [key: string]: any
}

// 账户列表响应
export interface AccountListResponse {
  code: number
  msg: string
  total: number
  rows: AccountData[]
}

// 账户详情响应
export interface AccountDetailResponse {
  code: number
  msg: string
  data: AccountData
}

// 通用响应
export interface CommonResponse {
  code: number
  msg: string
}

/**
 * 查询账户列表
 * @param params 查询参数
 */
export function getAccountList(params: AccountQuery) {
  return get<AccountListResponse>('/system/account/list', params)
}

/**
 * 获取账户详情
 * @param id 账户ID
 */
export function getAccountDetail(id: number) {
  return get<AccountDetailResponse>(`/system/account/${id}`)
}

/**
 * 新增账户
 * @param data 账户数据
 */
export function addAccount(data: Partial<AccountData>) {
  return post<CommonResponse>('/system/account', data)
}

/**
 * 修改账户
 * @param data 账户数据
 */
export function updateAccount(data: Partial<AccountData>) {
  return put<CommonResponse>('/system/account', data)
}

/**
 * 删除账户
 * @param ids 账户ID，多个以逗号分隔
 */
export function deleteAccount(ids: string) {
  return del<CommonResponse>(`/system/account/${ids}`)
} 