<template>
  <div class="user-center">
    <el-row :gutter="20">
      <!-- 左侧用户信息 -->
      <el-col :span="6">
        <el-card class="user-info-card">
          <div class="user-avatar">
            <el-avatar :size="100" :src="userInfo?.avatar" />
            <h3>{{ userInfo?.username }}</h3>
            <p class="email">{{ userInfo?.email }}</p>
          </div>
          
          <div class="account-info">
            <div class="info-item">
              <span class="label">账户余额</span>
              <span class="value">¥ {{ formatNumber(userInfo?.balance || 0) }}</span>
            </div>
            <div class="info-item">
              <span class="label">运行中策略</span>
              <span class="value">{{ runningStrategies.length }}</span>
            </div>
            <div class="info-item">
              <span class="label">总收益率</span>
              <span class="value" :class="{ 'positive': totalReturn > 0, 'negative': totalReturn < 0 }">
                {{ formatPercentage(totalReturn) }}
              </span>
            </div>
          </div>
          
          <el-button type="primary" @click="$router.push('/create-strategy')" class="create-btn">
            创建新策略
          </el-button>
        </el-card>
      </el-col>
      
      <!-- 右侧策略列表和性能指标 -->
      <el-col :span="18">
        <!-- 性能指标卡片 -->
        <el-card class="performance-card">
          <template #header>
            <div class="card-header">
              <h3>账户总览</h3>
              <el-select v-model="timeRange" placeholder="选择时间范围">
                <el-option label="最近7天" value="7d" />
                <el-option label="最近30天" value="30d" />
                <el-option label="最近90天" value="90d" />
                <el-option label="最近1年" value="1y" />
                <el-option label="全部" value="all" />
              </el-select>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="8" v-for="(metric, index) in performanceMetrics" :key="index">
              <div class="metric-card">
                <div class="metric-value" :class="{ 'positive': metric.value > 0, 'negative': metric.value < 0 }">
                  {{ formatMetricValue(metric.value, metric.format) }}
                </div>
                <div class="metric-label">{{ metric.label }}</div>
                <div class="metric-change" :class="{ 'positive': metric.change > 0, 'negative': metric.change < 0 }">
                  {{ metric.change > 0 ? '+' : '' }}{{ formatPercentage(metric.change) }}
                  <el-icon><component :is="metric.change > 0 ? 'ArrowUp' : 'ArrowDown'" /></el-icon>
                </div>
              </div>
            </el-col>
          </el-row>
          
          <!-- 收益曲线图 -->
          <div class="performance-chart" ref="performanceChart"></div>
        </el-card>
        
        <!-- 策略列表 -->
        <el-card class="strategies-card">
          <template #header>
            <div class="card-header">
              <h3>我的策略</h3>
              <el-input
                v-model="searchQuery"
                placeholder="搜索策略"
                :prefix-icon="Search"
                class="search-input"
              />
            </div>
          </template>
          
          <el-table :data="filteredStrategies" style="width: 100%">
            <el-table-column prop="name" label="策略名称" min-width="180">
              <template #default="{ row }">
                <div class="strategy-name" @click="$router.push(`/strategy/${row.id}`)">
                  {{ row.name }}
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="performance.annualReturn" label="年化收益" width="120">
              <template #default="{ row }">
                <span :class="{ 'positive': row.performance.annualReturn > 0, 'negative': row.performance.annualReturn < 0 }">
                  {{ formatPercentage(row.performance.annualReturn) }}
                </span>
              </template>
            </el-table-column>
            
            <el-table-column prop="performance.maxDrawdown" label="最大回撤" width="120">
              <template #default="{ row }">
                <span class="negative">
                  {{ formatPercentage(row.performance.maxDrawdown) }}
                </span>
              </template>
            </el-table-column>
            
            <el-table-column prop="performance.sharpeRatio" label="夏普比率" width="120">
              <template #default="{ row }">
                {{ row.performance.sharpeRatio.toFixed(2) }}
              </template>
            </el-table-column>
            
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button
                  :type="row.status === 'running' ? 'warning' : 'success'"
                  size="small"
                  @click="toggleStrategy(row)"
                >
                  {{ row.status === 'running' ? '停止' : '启动' }}
                </el-button>
                <el-button
                  type="primary"
                  size="small"
                  @click="$router.push(`/strategy/${row.id}`)"
                >
                  配置
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  @click="deleteStrategy(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { useStrategyStore } from '../stores/strategy'
import { Search, ArrowUp, ArrowDown } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from 'echarts'
import { QuantAPI, UserStrategyAPI } from '../api'

const userStore = useUserStore()
const strategyStore = useStrategyStore()

const userInfo = computed(() => userStore.getUserInfo)
const searchQuery = ref('')
const timeRange = ref('30d')
const performanceChart = ref<HTMLElement | null>(null)
const loading = ref(false)

// 初始化数据
const initData = async () => {
  loading.value = true
  try {
    // 获取用户策略列表
    const strategiesRes = await QuantAPI.getStrategyList({})
    strategyStore.setUserStrategies(strategiesRes.data.list)
    
    // 获取用户账户信息
    interface AccountsResponse {
      rows: any[];
      total: number;
      code: number;
      msg: string;
    }
    
    // 获取用户账户信息
    const accountsRes = await UserStrategyAPI.getUserStrategyAccountList() as unknown as AccountsResponse;
    const accounts = accountsRes.rows || []
    
    // 获取策略绩效报告
    interface ReportsResponse {
      rows: any[];
      total: number;
      code: number;
      msg: string;
    }
    const reportsRes = await UserStrategyAPI.getStrategyReportList() as unknown as ReportsResponse;
    const reports = reportsRes.rows || []
    
    // 更新性能指标
    updatePerformanceMetrics(accounts, reports)
    
    // 初始化图表
    initPerformanceChart(reports)
  } catch (error) {
    console.error('加载用户数据失败', error)
    ElMessage.error('加载数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 更新性能指标
const updatePerformanceMetrics = (accounts: any[], reports: any[]) => {
  if (!accounts.length || !reports.length) return
  
  // 计算总资产
  const totalAssets = accounts.reduce((sum, account) => sum + account.balance, 0)
  
  // 计算累计收益
  const totalReturn = reports.length > 0 ? reports[reports.length - 1].totalReturn : 0
  
  // 计算年化收益率
  const annualReturn = reports.length > 0 ? reports[reports.length - 1].annualReturn : 0
  
  // 计算变化率（与上一期相比）
  const prevReport = reports.length > 1 ? reports[reports.length - 2] : null
  const totalReturnChange = prevReport ? (totalReturn - prevReport.totalReturn) : 0
  const annualReturnChange = prevReport ? (annualReturn - prevReport.annualReturn) : 0
  
  performanceMetrics.value = [
    {
      label: '总资产',
      value: totalAssets,
      change: totalAssets > 0 ? totalReturnChange : 0,
      format: 'currency'
    },
    {
      label: '累计收益',
      value: totalReturn,
      change: totalReturnChange,
      format: 'percentage'
    },
    {
      label: '年化收益率',
      value: annualReturn,
      change: annualReturnChange,
      format: 'percentage'
    }
  ]
}

// 运行中的策略
const runningStrategies = computed(() => {
  return strategyStore.userStrategies.filter(s => s.status === 'running')
})

// 总收益率
const totalReturn = computed(() => {
  return strategyStore.userStrategies.reduce((acc, curr) => {
    return acc + curr.performance.totalReturn
  }, 0)
})

// 性能指标
const performanceMetrics = ref([
  {
    label: '总资产',
    value: 100000,
    change: 0.15,
    format: 'currency'
  },
  {
    label: '累计收益',
    value: 0.25,
    change: 0.05,
    format: 'percentage'
  },
  {
    label: '年化收益率',
    value: 0.35,
    change: -0.02,
    format: 'percentage'
  }
])

// 过滤后的策略列表
const filteredStrategies = computed(() => {
  if (!searchQuery.value) {
    return strategyStore.userStrategies
  }
  
  const query = searchQuery.value.toLowerCase()
  return strategyStore.userStrategies.filter(s => 
    s.name.toLowerCase().includes(query) ||
    s.description.toLowerCase().includes(query)
  )
})

// 方法
const formatNumber = (num: number) => {
  return new Intl.NumberFormat('zh-CN').format(num)
}

const formatPercentage = (value: number) => {
  return `${(value * 100).toFixed(2)}%`
}

const formatMetricValue = (value: number, format: string) => {
  if (format === 'percentage') {
    return formatPercentage(value)
  } else if (format === 'currency') {
    return `¥ ${formatNumber(value)}`
  }
  return value.toFixed(2)
}

const getStatusType = (status: string) => {
  const types = {
    running: 'success',
    stopped: 'info',
    error: 'danger'
  }
  return types[status as keyof typeof types]
}

const toggleStrategy = async (strategy: any) => {
  try {
    const newStatus = strategy.status === 'running' ? 'stopped' : 'running'
    const actionName = newStatus === 'running' ? '启动' : '停止'
    
    await ElMessageBox.confirm(
      `确定要${actionName}该策略吗？`,
      `${actionName}确认`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    if (newStatus === 'running') {
      await QuantAPI.runStrategy(strategy.id)
    } else {
      await QuantAPI.stopStrategy(strategy.id)
    }
    
    await strategyStore.updateStrategyStatus(strategy.id, newStatus)
    ElMessage.success(`策略已${actionName}`)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`操作失败，请稍后重试`)
    }
  }
}

const deleteStrategy = async (strategy: any) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该策略吗？删除后无法恢复。',
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await QuantAPI.deleteStrategy(strategy.id)
    
    // 从本地状态中移除
    const newStrategies = strategyStore.userStrategies.filter(s => s.id !== strategy.id)
    strategyStore.setUserStrategies(newStrategies)
    
    ElMessage.success('策略已删除')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败，请稍后重试')
    }
  }
}

const initPerformanceChart = (reports: any[] = []) => {
  if (!performanceChart.value) return
  
  const chart = echarts.init(performanceChart.value)
  
  // 如果没有实际数据，使用模拟数据
  let dates = []
  let values = []
  
  if (reports.length > 0) {
    // 使用实际数据
    dates = reports.map(report => report.date)
    values = reports.map(report => report.netValue)
  } else {
    // 使用模拟数据
    dates = Array.from({ length: 30 }, (_, i) => {
      const date = new Date()
      date.setDate(date.getDate() - (29 - i))
      return date.toISOString().split('T')[0]
    })
    
    values = Array.from({ length: 30 }, (_, i) => {
      return (1 + Math.random() * 0.1) ** i
    })
  }
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const date = params[0].axisValue
        const value = params[0].data
        return `${date}<br/>净值：${value.toFixed(4)}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: {
      type: 'value',
      scale: true
    },
    series: [{
      name: '账户净值',
      type: 'line',
      data: values,
      smooth: true,
      showSymbol: false,
      lineStyle: {
        width: 2,
        color: '#409EFF'
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(64,158,255,0.3)' },
          { offset: 1, color: 'rgba(64,158,255,0.1)' }
        ])
      }
    }]
  }
  
  chart.setOption(option)
  
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

// 生命周期钩子
onMounted(() => {
  initData()
})
</script>

<style scoped lang="scss">
.user-center {
  padding: 20px;
  
  .user-info-card {
    .user-avatar {
      text-align: center;
      padding: 20px 0;
      
      h3 {
        margin: 10px 0 5px;
      }
      
      .email {
        color: #909399;
        font-size: 14px;
      }
    }
    
    .account-info {
      margin: 20px 0;
      
      .info-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 15px;
        
        .label {
          color: #909399;
        }
        
        .value {
          font-weight: 500;
        }
      }
    }
    
    .create-btn {
      width: 100%;
    }
  }
  
  .performance-card {
    margin-bottom: 20px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      h3 {
        margin: 0;
      }
    }
    
    .metric-card {
      text-align: center;
      padding: 20px;
      border-radius: 8px;
      background-color: #f8f9fa;
      margin-bottom: 20px;
      
      .metric-value {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 5px;
      }
      
      .metric-label {
        color: #909399;
        margin-bottom: 5px;
      }
      
      .metric-change {
        font-size: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
      }
    }
    
    .performance-chart {
      height: 300px;
      margin-top: 20px;
    }
  }
  
  .strategies-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      h3 {
        margin: 0;
      }
      
      .search-input {
        width: 200px;
      }
    }
    
    .strategy-name {
      color: #409EFF;
      cursor: pointer;
      
      &:hover {
        text-decoration: underline;
      }
    }
  }
  
  .positive {
    color: #67c23a;
  }
  
  .negative {
    color: #f56c6c;
  }
}
</style> 