<template>
  <div class="home-container">
    <div class="hero-section">
      <h1>量化交易平台</h1>
      <p>专业的量化策略开发与回测平台</p>
      <div class="hero-buttons">
        <el-button type="primary" size="large" @click="navigateToCreateStrategy">
          创建策略(测试中，有任何问题向我反馈)
        </el-button>
        <el-button 
          v-if="userStore.getIsAdmin" 
          type="warning" 
          size="large" 
          @click="initEngineHandler"
        >
          初始化引擎
        </el-button>
      </div>
    </div>
    
    <div class="features-section">
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="feature-card">
            <el-icon><DataAnalysis /></el-icon>
            <h3>策略开发</h3>
            <p>提供丰富的技术指标和基本面数据，轻松构建量化策略</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="feature-card">
            <el-icon><TrendCharts /></el-icon>
            <h3>回测分析(停用)</h3>
            <p>高性能回测引擎，全面评估策略表现</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="feature-card">
            <el-icon><Monitor /></el-icon>
            <h3>实盘交易</h3>
            <p>一键部署策略至实盘，支持多接口</p>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 热门策略列表 -->
    <div class="strategies-section">
      <div class="section-header">
        <h2>热门策略</h2>
        <div class="filters">
          <el-select v-model="categoryFilter" placeholder="策略分类" clearable>
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
          <el-select v-model="sortBy" placeholder="排序方式">
            <el-option label="年化收益率" value="annualReturn" />
            <el-option label="总收益率" value="totalReturn" />
            <el-option label="夏普比率" value="sharpeRatio" />
            <el-option label="最大回撤" value="maxDrawdown" />
          </el-select>
        </div>
      </div>
      
      <el-row :gutter="24" class="strategy-cards">
        <el-col :span="8" v-for="strategy in filteredStrategies" :key="strategy.id" class="strategy-col">
          <el-card class="strategy-card" @click="navigateToStrategyDetail(strategy.id)">
            <div class="strategy-header">
              <h3 class="strategy-name">{{ strategy.name }}</h3>
              <el-tag v-if="strategy.isHot" type="danger" size="small" effect="plain">热门</el-tag>
            </div>
            
            <div class="strategy-category">
              <el-tag>{{ strategy.category }}</el-tag>
            </div>
            
            <p class="strategy-description">{{ strategy.description }}</p>
            
            <div class="strategy-performance">
              <div class="performance-item">
                <span class="label">年化收益</span>
                <span class="value" :class="strategy.performance.annualReturn > 0 ? 'positive' : 'negative'">
                  {{ formatPercent(strategy.performance.annualReturn) }}
                </span>
              </div>
              <div class="performance-item">
                <span class="label">总收益</span>
                <span class="value" :class="strategy.performance.totalReturn > 0 ? 'positive' : 'negative'">
                  {{ formatPercent(strategy.performance.totalReturn) }}
                </span>
              </div>
              <div class="performance-item">
                <span class="label">最大回撤</span>
                <span class="value negative">
                  {{ formatPercent(strategy.performance.maxDrawdown) }}
                </span>
              </div>
              <div class="performance-item">
                <span class="label">夏普比率</span>
                <span class="value">
                  {{ strategy.performance.sharpeRatio.toFixed(2) }}
                </span>
              </div>
            </div>
            
            <div class="strategy-author">
              <el-avatar :size="24" :src="strategy.authorAvatar" />
              <span>{{ strategy.author }}</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <div class="load-more" v-if="strategies.length > displayLimit">
        <el-button type="primary" plain @click="loadMore">加载更多</el-button>
      </div>
    </div>
    
    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-card">
            <h2>100%</h2>
            <p>个人开发</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-card">
            <h2>内测版本</h2>
            <p>V1.0.0</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-card">
            <h2>99.9%</h2>
            <p>系统稳定性</p>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { DataAnalysis, TrendCharts, Monitor } from '@element-plus/icons-vue'
import { useStrategyStore } from '../stores/strategy'
import { useUserStore } from '../stores/user'
import { QuantAPI } from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const strategyStore = useStrategyStore()
const userStore = useUserStore()

// 添加策略绩效接口
interface StrategyPerformance {
  annualReturn: number
  totalReturn: number
  maxDrawdown: number
  sharpeRatio: number
  [key: string]: number // 添加索引签名以允许字符串索引访问
}

// 扩展显示用的策略接口
interface DisplayStrategy {
  id: number
  name: string
  category: string
  description: string
  author: string
  authorAvatar: string
  isHot: boolean
  performance: StrategyPerformance
}

const strategies = ref<DisplayStrategy[]>([])
const categoryFilter = ref('')
const sortBy = ref('annualReturn')
const displayLimit = ref(6)
const categories = computed(() => strategyStore.getCategories)

// 获取策略列表
const fetchStrategies = async () => {
  try {
    // 调用实际的API获取策略列表数据，只传入owner参数
    const res = await QuantAPI.getStrategyList({
      owner: 1 // 1表示公开策略
    })
    
    if (res.code === 200 && res.rows) {
      // 处理返回的策略数据
      strategies.value = res.rows.map(item => ({
        id: item.id,
        name: item.strategyName || '未命名策略',
        category: item.remark ? item.remark.split('-')[0] : '未分类',
        description: item.remark || '暂无描述',
        author: item.createBy || '免费策略',
        authorAvatar: '', // 头像可能需要另外获取
        isHot: true, // 假设首页展示的都是热门策略
        performance: {
          // 初始化性能数据为0
          annualReturn: 0,
          totalReturn: 0,
          maxDrawdown: 0,
          sharpeRatio: 0
        }
      }))
      
      // 获取每个策略的绩效指标
      await fetchPerformanceData()
    }
  } catch (error) {
    console.error('获取策略列表失败', error)
    // 如果API调用失败，使用空数组
    strategies.value = []
  }
}

// 获取策略的绩效指标
const fetchPerformanceData = async () => {
  for (const strategy of strategies.value) {
    try {
      // 由于首页展示的策略可能没有accountId和owner，
      // 我们只传递策略ID，并使用API中的默认参数
      const perfRes = await QuantAPI.getStrategyPerformance(strategy.id)
      
      if (perfRes && perfRes.data) {
        // 解析JSON字符串，处理可能是字符串的情况
        let perfData
        try {
          // 如果data是字符串，尝试解析JSON
          perfData = typeof perfRes.data === 'string' ? JSON.parse(perfRes.data) : perfRes.data
        } catch (e) {
          console.error('解析策略绩效数据失败:', e)
          perfData = perfRes.data
        }
        
        // 安全地更新绩效数据，提供默认值以防数据缺失
        // 注意后端返回的字段名使用下划线命名法，需要映射到驼峰命名法
        strategy.performance = {
          // 年化收益率 (annualized_return -> annualReturn)
          annualReturn: typeof perfData.annualized_return === 'number' ? perfData.annualized_return : 0,
          
          // 总收益率 (total_pnlRatio -> totalReturn)
          totalReturn: typeof perfData.total_pnlRatio === 'number' ? perfData.total_pnlRatio : 0,
          
          // 最大回撤 (max_drawdown -> maxDrawdown)
          maxDrawdown: typeof perfData.max_drawdown === 'number' ? perfData.max_drawdown : 0,
          
          // 夏普比率 (sharpe_ratio -> sharpeRatio)
          sharpeRatio: typeof perfData.sharpe_ratio === 'number' ? perfData.sharpe_ratio : 0
        }
        
        // 添加对应的sortBy字段
        if (sortBy.value === 'annualReturn') {
          strategy.performance.annualReturn = typeof perfData.annualized_return === 'number' ? perfData.annualized_return : 0
        } else if (sortBy.value === 'totalReturn') {
          strategy.performance.totalReturn = typeof perfData.total_pnlRatio === 'number' ? perfData.total_pnlRatio : 0
        } else if (sortBy.value === 'maxDrawdown') {
          strategy.performance.maxDrawdown = typeof perfData.max_drawdown === 'number' ? perfData.max_drawdown : 0
        } else if (sortBy.value === 'sharpeRatio') {
          strategy.performance.sharpeRatio = typeof perfData.sharpe_ratio === 'number' ? perfData.sharpe_ratio : 0
        }
      }
    } catch (error) {
      console.error(`获取策略 ${strategy.id} 的绩效指标失败`, error)
    }
  }
}

onMounted(() => {
  fetchStrategies()
})

// 当分类过滤器变化时重新获取数据
watch(categoryFilter, () => {
  fetchStrategies()
})

// 过滤和排序策略
const filteredStrategies = computed(() => {
  let result = [...strategies.value]
  
  // 应用分类过滤
  if (categoryFilter.value) {
    result = result.filter(s => s.category === categoryFilter.value)
  }
  
  // 应用排序
  const field = sortBy.value as keyof StrategyPerformance
  if (field === 'maxDrawdown') {
    // 最大回撤是越小越好
    result.sort((a, b) => a.performance[field] - b.performance[field])
  } else {
    // 其他指标是越大越好
    result.sort((a, b) => b.performance[field] - a.performance[field])
  }
  
  // 限制显示数量
  return result.slice(0, displayLimit.value)
})

// 格式化百分比
const formatPercent = (value: number) => {
  return (value * 100).toFixed(2) + '%'
}

// 加载更多策略
const loadMore = () => {
  displayLimit.value += 6
}

// 导航到策略详情
const navigateToStrategyDetail = (id: number) => {
  router.push(`/strategy/${id}`)
}

// 导航到创建策略页面
const navigateToCreateStrategy = () => {
  if (userStore.isLoggedIn) {
    router.push('/create-strategy')
  } else {
    router.push('/login?redirect=/create-strategy')
  }
}

// 初始化引擎处理函数
const initEngineHandler = async () => {
  try {
    const res = await QuantAPI.initEngine()
    if (res.code === 200) {
      ElMessage.success('引擎初始化成功')
    } else {
      ElMessage.error(res.msg || '引擎初始化失败')
    }
  } catch (error) {
    console.error('初始化引擎失败', error)
    ElMessage.error('初始化引擎失败，请检查服务器状态')
  }
}
</script>

<style scoped lang="scss">
.home-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 60px 0;
  
  h1 {
    font-size: 48px;
    margin-bottom: 20px;
    color: #303133;
  }
  
  p {
    font-size: 20px;
    color: #606266;
    margin-bottom: 30px;
  }
  
  .hero-buttons {
    display: flex;
    justify-content: center;
    gap: 16px;
  }
}

.features-section {
  margin: 60px 0;
  
  .feature-card {
    text-align: center;
    padding: 30px;
    border-radius: 8px;
    background-color: #f5f7fa;
    height: 100%;
    
    .el-icon {
      font-size: 48px;
      color: #409eff;
      margin-bottom: 20px;
    }
    
    h3 {
      font-size: 20px;
      margin-bottom: 15px;
      color: #303133;
    }
    
    p {
      color: #606266;
      line-height: 1.6;
    }
  }
}

.strategies-section {
  margin: 60px 0;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      font-size: 24px;
      color: #303133;
      margin: 0;
    }
    
    .filters {
      display: flex;
      gap: 16px;
    }
  }
  
  .strategy-cards {
    margin-bottom: 30px;
  }
  
  .strategy-col {
    margin-bottom: 24px;
  }
  
  .strategy-card {
    height: 100%;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    .strategy-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      
      .strategy-name {
        font-size: 18px;
        margin: 0;
        color: #303133;
      }
    }
    
    .strategy-category {
      margin-bottom: 10px;
    }
    
    .strategy-description {
      color: #606266;
      margin-bottom: 15px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
      line-height: 1.5;
      height: 3em;
    }
    
    .strategy-performance {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      margin-bottom: 15px;
      
      .performance-item {
        display: flex;
        flex-direction: column;
        
        .label {
          font-size: 12px;
          color: #909399;
        }
        
        .value {
          font-size: 16px;
          font-weight: 500;
          
          &.positive {
            color: #67c23a;
          }
          
          &.negative {
            color: #f56c6c;
          }
        }
      }
    }
    
    .strategy-author {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #909399;
      font-size: 14px;
    }
  }
  
  .load-more {
    text-align: center;
    margin-top: 20px;
  }
}

.stats-section {
  margin: 60px 0;
  
  .stat-card {
    text-align: center;
    padding: 30px;
    border-radius: 8px;
    background-color: #409eff;
    color: white;
    
    h2 {
      font-size: 36px;
      margin-bottom: 10px;
    }
    
    p {
      font-size: 16px;
      opacity: 0.9;
    }
  }
}
</style> 