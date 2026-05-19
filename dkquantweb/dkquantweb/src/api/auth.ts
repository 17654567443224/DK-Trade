import { get, post } from './request'

// 接口类型定义
interface LoginParams {
  username: string
  password: string
  code: string
  uuid: string
}

interface CaptchaResponse {
  code: number
  msg: string
  captchaEnabled: boolean
  uuid: string
  img: string
}

interface UserInfo {
  id: number
  username: string
  email: string
  balance: number
  avatar: string
  admin?: boolean
}

// 响应类型定义
interface LoginResponse {
  code: number
  msg: string
  token: string
  admin?: boolean
}

// 获取验证码
export function getCaptchaImage(): Promise<CaptchaResponse> {
  return get<CaptchaResponse>('/captchaImage')
}

// 登录接口
export function login(data: LoginParams): Promise<LoginResponse> {
  return post<LoginResponse>('/login', data)
}

// 获取用户信息接口
export function getUserInfo(silent: boolean = false): Promise<{
  code: number
  msg: string
  data: UserInfo
}> {
  return get<{
    code: number
    msg: string
    data: UserInfo
  }>('/system/user/info', undefined, { silent })
}

// 退出登录接口
export function logout(): Promise<{
  code: number
  msg: string
}> {
  return post<{
    code: number
    msg: string
  }>('/logout')
} 