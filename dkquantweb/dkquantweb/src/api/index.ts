// 导出策略相关 API
export * from './strategy'

// 导出量化交易相关 API，使用命名空间避免命名冲突
import * as QuantAPI from './quant'
import * as TemplatesAPI from './templates'
import * as StrategyComponentsAPI from './strategy-components'
import * as UserStrategyAPI from './user-strategy'

// 导出其他模块 API，使用命名空间避免命名冲突
import * as AccountAPI from './strategy-components'
import * as OrdersAPI from './user-strategy'
import * as ReportAPI from './user-strategy'
import * as ArgsAPI from './user-strategy'

// 导出认证相关API
import * as AuthAPI from './auth'

// 导出更新计划相关API
import * as UpdatePlanAPI from './update-plan'

// 导出请求工具
export { default as request } from './request'
export { get, post, put, del } from './request'

export {
  QuantAPI,
  TemplatesAPI,
  StrategyComponentsAPI,
  UserStrategyAPI,
  AccountAPI,
  OrdersAPI,
  ReportAPI,
  ArgsAPI,
  AuthAPI,
  UpdatePlanAPI
} 