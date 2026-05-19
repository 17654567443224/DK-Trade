import axios from 'axios'
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

// 配置选项接口
interface RequestOptions {
  silent?: boolean // 是否静默处理错误（不显示错误提示）
}

// 创建 axios 实例
const service: AxiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8080', // API 请求的基础路径，直接连接到8080端口
  timeout: 10000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 在发送请求之前做些什么
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 打印请求信息到控制台，便于调试
    console.log(`[API请求] ${config.method?.toUpperCase()} ${config.url}`, config)
    
    return config
  },
  (error) => {
    // 对请求错误做些什么
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const res = response.data
    const config = response.config as any // 包含自定义选项
    
    // 打印响应信息到控制台，便于调试
    console.log(`[API响应] ${response.config.method?.toUpperCase()} ${response.config.url}`, res)
    
    // 如果返回的状态码不是200，说明接口请求失败
    // 这里可以根据后端的错误码进行不同的处理
    if (res.code !== 200) {
      // 只有在非静默模式下才显示错误提示
      if (!config.silent) {
        ElMessage({
          message: res.msg || '系统错误',
          type: 'error',
          duration: 5 * 1000
        })
      }
      
      // 401: 未登录或token过期
      if (res.code === 401) {
        // 处理登出逻辑
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
      
      return Promise.reject(new Error(res.msg || '系统错误'))
    } else {
      return res
    }
  },
  (error) => {
    console.error('响应错误:', error)
    
    const config = error.config as any // 包含自定义选项
    const silent = config && config.silent
    
    // 处理特定的错误情况
    if (error.response) {
      const { status, data, config } = error.response
      
      console.error(`[API错误] ${config.method?.toUpperCase()} ${config.url} 状态: ${status}`, data)
      
      // 处理回测引擎连接错误
      if (status === 500 && data.msg && data.msg.includes('Connection refused')) {
        if (!silent) {
          ElMessage({
            message: '回测引擎服务未启动，请联系管理员启动服务后再试',
            type: 'error',
            duration: 7 * 1000
          })
        }
        return Promise.reject(new Error('回测引擎服务未启动'))
      }
    }
    
    // 通用错误处理，只有在非静默模式下才显示错误提示
    if (!silent) {
      ElMessage({
        message: error.message || '请求失败',
        type: 'error',
        duration: 5 * 1000
      })
    }
    return Promise.reject(error)
  }
)

// 扩展axios的配置类型
declare module 'axios' {
  interface AxiosRequestConfig {
    silent?: boolean
  }
}

// 封装 GET 请求
export function get<T>(url: string, params?: any, options?: RequestOptions): Promise<T> {
  return service.get(url, { params, silent: options?.silent })
}

// 封装 POST 请求
export function post<T>(url: string, data?: any, options?: RequestOptions): Promise<T> {
  return service.post(url, data, { silent: options?.silent })
}

// 封装 PUT 请求
export function put<T>(url: string, data?: any, options?: RequestOptions): Promise<T> {
  return service.put(url, data, { silent: options?.silent })
}

// 封装 DELETE 请求
export function del<T>(url: string, params?: any, options?: RequestOptions): Promise<T> {
  return service.delete(url, { params, silent: options?.silent })
}

export default service 