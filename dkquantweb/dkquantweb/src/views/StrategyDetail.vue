<template>
  <div class="strategy-detail">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <template v-else>
      <!-- 策略基本信息 -->
      <div class="strategy-header">
        <div class="strategy-title">
          <h1>{{ strategy?.name }}</h1>
          <div class="strategy-tags">
            <el-tag>{{ strategy?.category }}</el-tag>
            <el-tag type="success" v-if="strategy?.status === 'running'">运行中</el-tag>
            <el-tag type="info" v-else-if="strategy?.status === 'stopped'">已停止</el-tag>
            <el-tag type="danger" v-else-if="strategy?.status === 'error'">错误</el-tag>
          </div>
        </div>
        
        <div class="strategy-actions">
          <el-button 
            :type="strategy?.status === 'running' ? 'warning' : 'success'"
            @click="toggleStrategy"
          >
            {{ strategy?.status === 'running' ? '停止' : '启动' }}
          </el-button>
          <el-button type="primary" @click="editStrategy">编辑策略</el-button>
          <el-button type="danger" @click="deleteStrategy">删除策略</el-button>
        </div>
      </div>
      
      <el-descriptions class="strategy-info" :column="3" border>
        <el-descriptions-item label="创建者">{{ strategy?.author }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(strategy?.createTime) }}</el-descriptions-item>
        <el-descriptions-item label="最后更新时间">{{ formatDate(strategy?.updateTime) }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="3">{{ strategy?.description }}</el-descriptions-item>
      </el-descriptions>
      
      <!-- 绩效指标 -->
      <el-card class="performance-card">
        <template #header>
          <div class="card-header">
            <h2>性能指标</h2>
            <el-select v-model="timeRange" placeholder="时间范围">
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
              <div class="metric-value" :class="getValueClass(metric)">
                {{ formatMetricValue(metric.value, metric.format) }}
              </div>
              <div class="metric-label">{{ metric.label }}</div>
              <div class="metric-info" v-if="metric.info">{{ metric.info }}</div>
            </div>
          </el-col>
        </el-row>
        
        <!-- 净值曲线图 -->
        <div class="chart-container">
          <div class="performance-chart" ref="performanceChart"></div>
        </div>
      </el-card>
      
      <!-- 账户信息 -->
      <el-card class="account-card">
        <template #header>
          <div class="card-header">
            <h2>账户信息</h2>
          </div>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="初始资金">¥ {{ formatNumber(account?.initialBalance) }}</el-descriptions-item>
          <el-descriptions-item label="当前资金">¥ {{ formatNumber(account?.balance) }}</el-descriptions-item>
          <el-descriptions-item label="盈亏金额">
            <span :class="getValueClass(account?.pnl)">
              ¥ {{ formatNumber(account?.pnl) }}
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="盈亏比例">
            <span :class="getValueClass(account?.pnlRatio)">
              {{ formatPercentage(account?.pnlRatio) }}
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="交易费用">¥ {{ formatNumber(account?.orderFee) }}</el-descriptions-item>
          <el-descriptions-item label="总交易次数">{{ account?.totalTrades }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
      
      <!-- 当前持仓 -->
      <el-card class="positions-card">
        <template #header>
          <div class="card-header">
            <h2>当前持仓</h2>
          </div>
        </template>
        
        <el-table :data="positions" style="width: 100%" v-if="positions.length > 0">
          <el-table-column prop="symbol" label="股票代码" />
          <el-table-column prop="name" label="股票名称" />
          <el-table-column prop="type" label="持仓类型">
            <template #default="{ row }">
              <el-tag :type="row.type === 'long' ? 'success' : 'danger'">
                {{ row.type === 'long' ? '多头' : '空头' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="entryPrice" label="入场价格">
            <template #default="{ row }">
              ¥ {{ formatNumber(row.entryPrice) }}
            </template>
          </el-table-column>
          <el-table-column prop="currentPrice" label="当前价格">
            <template #default="{ row }">
              ¥ {{ formatNumber(row.currentPrice) }}
            </template>
          </el-table-column>
          <el-table-column prop="size" label="持仓数量" />
          <el-table-column prop="pnl" label="浮动盈亏">
            <template #default="{ row }">
              <span :class="getValueClass(row.pnl)">
                {{ formatNumber(row.pnl) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="pnlRatio" label="盈亏比例">
            <template #default="{ row }">
              <span :class="getValueClass(row.pnlRatio)">
                {{ formatPercentage(row.pnlRatio) }}
              </span>
            </template>
          </el-table-column>
        </el-table>
        
        <el-empty description="暂无持仓数据" v-else />
      </el-card>
      
      <!-- 交易记录 -->
      <el-card class="orders-card">
        <template #header>
          <div class="card-header">
            <h2>交易记录</h2>
            <el-input
              v-model="orderSearch"
              placeholder="搜索股票代码"
              :prefix-icon="Search"
              class="order-search"
            />
          </div>
        </template>
        
        <el-table :data="filteredOrders" style="width: 100%" v-if="orders.length > 0">
          <el-table-column prop="time" label="交易时间" width="180">
            <template #default="{ row }">
              {{ formatDateTime(row.time) }}
            </template>
          </el-table-column>
          <el-table-column prop="symbol" label="股票代码" width="100" />
          <el-table-column prop="name" label="股票名称" width="120" />
          <el-table-column prop="type" label="交易类型" width="100">
            <template #default="{ row }">
              <el-tag :type="row.type === 'buy' ? 'success' : 'danger'">
                {{ row.type === 'buy' ? '买入' : '卖出' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="price" label="价格" width="100">
            <template #default="{ row }">
              ¥ {{ formatNumber(row.price) }}
            </template>
          </el-table-column>
          <el-table-column prop="size" label="数量" width="100" />
          <el-table-column prop="amount" label="金额" width="120">
            <template #default="{ row }">
              ¥ {{ formatNumber(row.price * row.size) }}
            </template>
          </el-table-column>
          <el-table-column prop="pnl" label="盈亏" width="100">
            <template #default="{ row }">
              <span :class="getValueClass(row.pnl)" v-if="row.type === 'sell'">
                {{ formatNumber(row.pnl) }}
              </span>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="pnlRatio" label="盈亏比例" width="100">
            <template #default="{ row }">
              <span :class="getValueClass(row.pnlRatio)" v-if="row.type === 'sell'">
                {{ formatPercentage(row.pnlRatio) }}
              </span>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="exitType" label="出场类型" width="120">
            <template #default="{ row }">
              <el-tag type="info" v-if="row.type === 'sell'">
                {{ row.exitType }}
              </el-tag>
              <span v-else>-</span>
            </template>
          </el-table-column>
        </el-table>
        
        <el-empty description="暂无交易记录" v-else />
        
        <div class="pagination" v-if="orders.length > 0">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="orders.length"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
      
      <!-- 策略配置面板 -->
      <el-card class="strategy-config-card">
        <template #header>
          <div class="card-header">
            <h2>策略配置</h2>
            <el-button type="primary" @click="showConfigPanel = !showConfigPanel">
              {{ showConfigPanel ? '隐藏配置面板' : '展开配置面板' }}
            </el-button>
          </div>
        </template>
        
        <div v-if="showConfigPanel">
          <el-form ref="strategyFormRef" :model="strategyForm" label-position="top" class="strategy-form">
            <!-- 基本信息 -->
            <div class="form-section">
              <h3>基本信息</h3>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="策略名称">
                    <el-input v-model="strategy.name" placeholder="请输入策略名称" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="本金">
                    <el-input-number
                      v-model="strategyForm.position.size"
                      :min="1000"
                      :step="1000"
                      style="width: 100%"
                    >
                      <template #prefix>¥</template>
                    </el-input-number>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item label="最大持仓数量">
                <el-input-number
                  v-model="strategyForm.position.maxPositions"
                  :min="1"
                  :max="100"
                  style="width: 100%"
                />
              </el-form-item>
              
              <el-form-item label="杠杆">
                <el-input-number
                  v-model="strategyForm.lever"
                  :min="1"
                  :step="1"
                  :precision="0"
                  :default-value="50"
                  style="width: 100%"
                />
              </el-form-item>
            </div>

            <!-- 选股策略 -->
            <div class="form-section">
              <h3>选股策略</h3>
              <el-form-item label="选股模板">
                <el-select
                  v-model="strategyForm.stockSelectionTemplateId"
                  placeholder="请选择选股模板"
                  style="width: 100%"
                >
                  <el-option
                    v-for="template in uniqueSymbolSelectionTemplates"
                    :key="template.id"
                    :label="template.cnClassName"
                    :value="template.id"
                  />
                </el-select>
              </el-form-item>
              
              <!-- 显示选股模板参数 -->
              <div v-if="!isFixedSymbolTemplate && strategyForm.stockSelectionTemplateId && getTemplateParams(strategyForm.stockSelectionTemplateId).length > 0" class="params-container">
                <el-row :gutter="20">
                  <el-col 
                    :span="8" 
                    v-for="(param, index) in getTemplateParams(strategyForm.stockSelectionTemplateId)" 
                    :key="index"
                  >
                    <div class="param-config">
                      <div class="param-label">
                        <span class="param-name">{{ param.label || param.name }}</span>
                        <el-tooltip :content="param.description || param.label || '参数说明'" placement="top">
                          <el-icon><InfoFilled /></el-icon>
                        </el-tooltip>
                      </div>
                      
                      <!-- 根据参数类型显示不同的输入组件 -->
                      <template v-if="param.type === 'number'">
                        <el-input-number
                          v-model="strategyForm.stockSelection.templateParams[param.name]"
                          :placeholder="param.label || param.name"
                          style="width: 100%"
                        />
                      </template>
                      <template v-else-if="param.type === 'boolean'">
                        <el-switch
                          v-model="strategyForm.stockSelection.templateParams[param.name]"
                          active-text="是"
                          inactive-text="否"
                        />
                      </template>
                      <template v-else>
                        <el-input
                          v-model="strategyForm.stockSelection.templateParams[param.name]"
                          :placeholder="param.label || param.name"
                          style="width: 100%"
                        />
                      </template>
                    </div>
                  </el-col>
                </el-row>
              </div>
              
              <!-- 固定交易对选择区域 -->
              <div v-if="isFixedSymbolTemplate" class="form-section">
                <el-form-item label="交易对列表">
                  <div class="symbol-list">
                    <div v-for="(symbol, index) in symbols" :key="index" class="symbol-item">
                      <el-input 
                        v-model="symbols[index]" 
                        placeholder="请输入交易对" 
                        class="symbol-input"
                      />
                      <el-button 
                        type="danger" 
                        size="small" 
                        icon="Delete" 
                        @click="removeSymbol(index)"
                        class="symbol-delete-btn"
                      />
                    </div>
                    <el-button 
                      type="primary" 
                      @click="addSymbol" 
                      class="add-symbol-btn"
                    >
                      添加交易对
                    </el-button>
                  </div>
                </el-form-item>
              </div>
              
              <!-- 选股方法 -->
              <el-form-item v-if="stockSelectionMethods && stockSelectionMethods.length > 0" label="选股方式">
                <el-select
                  v-model="strategyForm.stockSelectionMethod"
                  placeholder="请选择选股方式(可选)"
                  style="width: 100%"
                >
                  <el-option
                    v-for="method in stockSelectionMethods"
                    :key="method.className"
                    :label="getMethodDisplayName(method)"
                    :value="method.funName"
                  />
                </el-select>
              </el-form-item>
              
              <!-- 显示选股方法参数，仅当有选股方法且选股方法有参数时才显示 -->
              <div v-if="strategyForm.stockSelectionMethod && stockSelectionMethods && stockSelectionMethods.length > 0 && getIndicatorParams(strategyForm.stockSelectionMethod).length > 0" class="params-container">
                <div>
                  <div class="debug-info" style="margin-bottom: 10px; font-size: 12px; color: #999;">
                  </div>
                  <el-row :gutter="20">
                    <el-col 
                      :span="8" 
                      v-for="(param, index) in getIndicatorParams(strategyForm.stockSelectionMethod)" 
                      :key="index"
                    >
                      <!-- 参数配置内容保持不变 -->
                      <div class="param-config">
                        <div class="param-label">
                          <span class="param-name">{{ param.label || param.name }}</span>
                          <el-tooltip :content="param.description || param.label || '参数说明'" placement="top">
                            <el-icon><InfoFilled /></el-icon>
                          </el-tooltip>
                        </div>
                        
                        <!-- 根据参数类型显示不同的输入组件 -->
                        <template v-if="param.type === 'number'">
                          <el-input-number
                            v-model="strategyForm.stockSelection.params[strategyForm.stockSelectionMethod][param.name]"
                            :placeholder="param.label || param.name"
                            style="width: 100%"
                          />
                        </template>
                        <template v-else-if="param.type === 'boolean'">
                          <el-switch
                            v-model="strategyForm.stockSelection.params[strategyForm.stockSelectionMethod][param.name]"
                            active-text="是"
                            inactive-text="否"
                          />
                        </template>
                        <template v-else>
                          <el-input
                            v-model="strategyForm.stockSelection.params[strategyForm.stockSelectionMethod][param.name]"
                            :placeholder="param.label || param.name"
                            style="width: 100%"
                          />
                        </template>
                      </div>
                    </el-col>
                  </el-row>
                  <div v-if="getIndicatorParams(strategyForm.stockSelectionMethod).length === 0" class="empty-params">
                    该方法无需配置参数
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 止盈止损策略 -->
            <div class="form-section">
              <h3>止盈止损策略</h3>
              <el-form-item label="止盈止损模板">
                <el-select
                  v-model="strategyForm.stopLoss.templateId"
                  placeholder="请选择止盈止损模板"
                  style="width: 100%"
                >
                  <el-option
                    v-for="template in profitLossTemplates"
                    :key="template.id"
                    :label="template.cnClassName"
                    :value="template.id"
                  />
                </el-select>
              </el-form-item>
              
              <!-- 显示止盈止损模板参数 -->
              <div v-if="strategyForm.stopLoss.templateId && getTemplateParams(strategyForm.stopLoss.templateId, 'exit').length > 0" class="params-container">
                <el-row :gutter="20">
                  <el-col 
                    :span="8" 
                    v-for="(param, index) in getTemplateParams(strategyForm.stopLoss.templateId, 'exit')" 
                    :key="index"
                  >
                    <div class="param-config">
                      <div class="param-label">
                        <span class="param-name">{{ param.label || param.name }}</span>
                        <el-tooltip :content="param.description || param.label || '参数说明'" placement="top">
                          <el-icon><InfoFilled /></el-icon>
                        </el-tooltip>
                      </div>
                      
                      <!-- 根据参数类型显示不同的输入组件 -->
                      <template v-if="param.type === 'number'">
                        <el-input-number
                          v-model="strategyForm.stopLoss.params[param.name]"
                          :placeholder="param.label || param.name"
                          style="width: 100%"
                        />
                      </template>
                      <template v-else-if="param.type === 'boolean'">
                        <el-switch
                          v-model="strategyForm.stopLoss.params[param.name]"
                          active-text="是"
                          inactive-text="否"
                        />
                      </template>
                      <template v-else>
                        <el-input
                          v-model="strategyForm.stopLoss.params[param.name]"
                          :placeholder="param.label || param.name"
                          style="width: 100%"
                        />
                      </template>
                    </div>
                  </el-col>
                </el-row>
              </div>
              
              <!-- 止盈止损方法 -->
              <el-form-item v-if="stopLossMethods && stopLossMethods.length > 0" label="止盈止损方式">
                <el-select
                  v-model="strategyForm.stopLossMethod"
                  placeholder="请选择止盈止损方式"
                  style="width: 100%"
                >
                  <el-option
                    v-for="method in stopLossMethods"
                    :key="method.className"
                    :label="getMethodDisplayName(method)"
                    :value="method.funName"
                  />
                </el-select>
              </el-form-item>
              
              <!-- 显示止盈止损方法参数，仅当有止盈止损方法且方法有参数时才显示 -->
              <div v-if="strategyForm.stopLossMethod && stopLossMethods && stopLossMethods.length > 0 && getIndicatorParams(strategyForm.stopLossMethod, 'exit').length > 0" class="params-container">
                <div>
                  <div class="debug-info" style="margin-bottom: 10px; font-size: 12px; color: #999;">
                  </div>
                  <el-row :gutter="20">
                    <el-col 
                      :span="8" 
                      v-for="(param, index) in getIndicatorParams(strategyForm.stopLossMethod, 'exit')" 
                      :key="index"
                    >
                      <div class="param-config">
                        <div class="param-label">
                          <span class="param-name">{{ param.label || param.name }}</span>
                          <el-tooltip :content="param.description || param.label || '参数说明'" placement="top">
                            <el-icon><InfoFilled /></el-icon>
                          </el-tooltip>
                        </div>
                        
                        <!-- 根据参数类型显示不同的输入组件 -->
                        <template v-if="param.type === 'number'">
                          <el-input-number
                            v-model="strategyForm.stopLoss.methodParams[param.name]"
                            :placeholder="param.label || param.name"
                            style="width: 100%"
                          />
                        </template>
                        <template v-else-if="param.type === 'boolean'">
                          <el-switch
                            v-model="strategyForm.stopLoss.methodParams[param.name]"
                            active-text="是"
                            inactive-text="否"
                          />
                        </template>
                        <template v-else>
                          <el-input
                            v-model="strategyForm.stopLoss.methodParams[param.name]"
                            :placeholder="param.label || param.name"
                            style="width: 100%"
                          />
                        </template>
                      </div>
                    </el-col>
                  </el-row>
                  <div v-if="getIndicatorParams(strategyForm.stopLossMethod, 'exit').length === 0" class="empty-params">
                    该方法无需配置参数
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 资金策略 -->
            <div class="form-section">
              <h3>资金策略</h3>
              <el-form-item label="资金管理模板">
                <el-select
                  v-model="strategyForm.position.templateId"
                  placeholder="请选择资金管理模板"
                  style="width: 100%"
                >
                  <el-option
                    v-for="template in positionTemplates"
                    :key="template.id"
                    :label="template.cnClassName"
                    :value="template.id"
                  />
                </el-select>
              </el-form-item>
              
              <!-- 显示资金管理模板参数 -->
              <div v-if="strategyForm.position.templateId && getTemplateParams(strategyForm.position.templateId, 'fund').length > 0" class="params-container">
                <el-row :gutter="20">
                  <el-col 
                    :span="8" 
                    v-for="(param, index) in getTemplateParams(strategyForm.position.templateId, 'fund')" 
                    :key="index"
                  >
                    <div class="param-config">
                      <div class="param-label">
                        <span class="param-name">{{ param.label || param.name }}</span>
                        <el-tooltip :content="param.description || param.label || '参数说明'" placement="top">
                          <el-icon><InfoFilled /></el-icon>
                        </el-tooltip>
                      </div>
                      
                      <!-- 根据参数类型显示不同的输入组件 -->
                      <template v-if="param.type === 'number'">
                        <el-input-number
                          v-model="strategyForm.position.params[param.name]"
                          :placeholder="param.label || param.name"
                          style="width: 100%"
                        />
                      </template>
                      <template v-else-if="param.type === 'boolean'">
                        <el-switch
                          v-model="strategyForm.position.params[param.name]"
                          active-text="是"
                          inactive-text="否"
                        />
                      </template>
                      <template v-else>
                        <el-input
                          v-model="strategyForm.position.params[param.name]"
                          :placeholder="param.label || param.name"
                          style="width: 100%"
                        />
                      </template>
                    </div>
                  </el-col>
                </el-row>
              </div>
              
              <!-- 资金管理方法 -->
              <el-form-item v-if="positionMethods && positionMethods.length > 0" label="资金管理方式">
                <el-select
                  v-model="strategyForm.positionMethod"
                  placeholder="请选择资金管理方式"
                  style="width: 100%"
                >
                  <el-option
                    v-for="method in positionMethods"
                    :key="method.className"
                    :label="getMethodDisplayName(method)"
                    :value="method.funName"
                  />
                </el-select>
              </el-form-item>
              
              <!-- 显示资金管理方法参数，仅当有资金管理方法且方法有参数时才显示 -->
              <div v-if="strategyForm.positionMethod && positionMethods && positionMethods.length > 0 && getIndicatorParams(strategyForm.positionMethod, 'fund').length > 0" class="params-container">
                <div>
                  <div class="debug-info" style="margin-bottom: 10px; font-size: 12px; color: #999;">
                  </div>
                  <el-row :gutter="20">
                    <el-col 
                      :span="8" 
                      v-for="(param, index) in getIndicatorParams(strategyForm.positionMethod, 'fund')" 
                      :key="index"
                    >
                      <div class="param-config">
                        <div class="param-label">
                          <span class="param-name">{{ param.label || param.name }}</span>
                          <el-tooltip :content="param.description || param.label || '参数说明'" placement="top">
                            <el-icon><InfoFilled /></el-icon>
                          </el-tooltip>
                        </div>
                        
                        <!-- 根据参数类型显示不同的输入组件 -->
                        <template v-if="param.type === 'number'">
                          <el-input-number
                            v-model="strategyForm.position.methodParams[param.name]"
                            :placeholder="param.label || param.name"
                            style="width: 100%"
                          />
                        </template>
                        <template v-else-if="param.type === 'boolean'">
                          <el-switch
                            v-model="strategyForm.position.methodParams[param.name]"
                            active-text="是"
                            inactive-text="否"
                          />
                        </template>
                        <template v-else>
                          <el-input
                            v-model="strategyForm.position.methodParams[param.name]"
                            :placeholder="param.label || param.name"
                            style="width: 100%"
                          />
                        </template>
                      </div>
                    </el-col>
                  </el-row>
                  <div v-if="getIndicatorParams(strategyForm.positionMethod, 'fund').length === 0" class="empty-params">
                    该方法无需配置参数
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 提交按钮 -->
            <div class="form-actions">
              <el-button type="primary" @click="saveStrategyConfig" :loading="savingConfig">
                保存配置
              </el-button>
            </div>
          </el-form>
        </div>
      </el-card>
      
      <!-- 回测面板 -->
      <el-card class="backtest-card">
        <template #header>
          <div class="card-header">
            <h2>策略回测</h2>
            <el-button type="primary" @click="showBacktest = !showBacktest">
              {{ showBacktest ? '隐藏回测面板' : '展开回测面板' }}
            </el-button>
          </div>
        </template>
        
        <div v-if="showBacktest">
          <el-alert
            type="warning"
            :closable="false"
            show-icon
            title="回测功能暂时不可用"
            description="该功能正在维护中，请稍后再试或联系管理员了解更多信息。"
            style="margin-bottom: 20px;"
          />
          <el-form :model="backtestForm" label-width="120px" class="backtest-form">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="开始日期">
                  <el-date-picker 
                    v-model="backtestForm.start" 
                    type="date" 
                    placeholder="选择开始日期"
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD"
                    style="width: 100%"
                    disabled
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="结束日期">
                  <el-date-picker 
                    v-model="backtestForm.end" 
                    type="date" 
                    placeholder="选择结束日期"
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD"
                    style="width: 100%"
                    disabled
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="时间间隔">
                  <el-select v-model="backtestForm.interval" style="width: 100%" disabled>
                    <el-option label="每日" value="daily" />
                    <el-option label="每周" value="weekly" />
                    <el-option label="每月" value="monthly" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item>
              <el-tooltip content="回测功能暂时不可用" placement="top">
                <el-button type="primary" disabled>
                开始回测
              </el-button>
              </el-tooltip>
            </el-form-item>
          </el-form>
          
          <div v-if="backtestResult" class="backtest-result">
            <h3>回测结果</h3>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="最终余额">{{ formatNumber(backtestResult.finalBalance) }}</el-descriptions-item>
              <el-descriptions-item label="最大回撤">{{ formatPercentage(backtestResult.maxDrawdown) }}</el-descriptions-item>
              <el-descriptions-item label="胜率">{{ formatPercentage(backtestResult.winRate) }}</el-descriptions-item>
              <el-descriptions-item label="最大盈利">{{ formatNumber(backtestResult.maxProfit) }}</el-descriptions-item>
              <el-descriptions-item label="最大亏损">{{ formatNumber(backtestResult.maxLoss) }}</el-descriptions-item>
              <el-descriptions-item label="交易总数">{{ backtestResult.totalTrades }}</el-descriptions-item>
              <el-descriptions-item label="夏普比率">{{ formatNumber(backtestResult.sharpeRatio) }}</el-descriptions-item>
              <el-descriptions-item label="年化收益率">{{ formatPercentage(backtestResult.annualizedReturn) }}</el-descriptions-item>
              <el-descriptions-item label="总收益率">{{ formatPercentage(backtestResult.totalPnlratio) }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </div>
      </el-card>
    </template>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, onMounted, watch, unref, markRaw } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, InfoFilled, Delete } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { QuantAPI, UserStrategyAPI, TemplatesAPI } from '../api'
import { get } from '@/api/request'
import { ListResponse } from '@/api/user-strategy'

const route = useRoute()
const router = useRouter()

// 状态变量
const loading = ref(true)
const strategy = ref<any>(null)
const account = ref<any>(null)
const positions = ref<any[]>([])
const orders = ref<any[]>([])
const timeRange = ref('30d')
const orderSearch = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const performanceChart = ref<HTMLElement | null>(null)

// 回测相关状态
const showBacktest = ref(false)
const backtestLoading = ref(false)
const backtestForm = ref({
  start: '',
  end: '',
  interval: 'daily'
})
const backtestResult = ref<any>(null)

// 策略配置相关状态
const showConfigPanel = ref(false)
const savingConfig = ref(false)
const strategyFormRef = ref<any>(null)
const symbols = ref<string[]>([])

// 模板和方法数据
const symbolSelectionTemplates = ref<any[]>([])
const profitLossTemplates = ref<any[]>([])
const positionTemplates = ref<any[]>([])

// 策略表单数据
const strategyForm = ref({
  strategyName: '',
  lever: 50,
  stockSelectionTemplateId: '',
  stockSelectionMethod: '',
  stockSelection: {
    templateParams: {} as Record<string, any>,
    params: {} as Record<string, Record<string, any>>
  },
  stopLossMethod: '',
  stopLoss: {
    templateId: '',
    params: {} as Record<string, any>,
    methodParams: {} as Record<string, any>,
    method: '' // 添加 method 字段
  },
  positionMethod: '',
  position: {
    templateId: '',
    size: 10000,
    maxPositions: 5,
    params: {} as Record<string, any>,
    methodParams: {} as Record<string, any>,
    method: '' // 添加 method 字段
  }
})

// 性能指标
const performanceMetrics = ref([
  { label: '总收益率', value: 0, format: 'percentage', positive: true },
  { label: '年化收益率', value: 0, format: 'percentage', positive: true },
  { label: '最大回撤', value: 0, format: 'percentage', positive: false },
  { label: '夏普比率', value: 0, format: 'number', positive: true, info: '年化收益率与波动率之比' },
  { label: '盈亏比', value: 0, format: 'number', positive: true, info: '平均盈利/平均亏损' },
  { label: '胜率', value: 0, format: 'percentage', positive: true }
])

// 过滤订单
const filteredOrders = computed(() => {
  if (!orderSearch.value) {
    return orders.value.slice(
      (currentPage.value - 1) * pageSize.value, 
      currentPage.value * pageSize.value
    )
  }
  
  const filtered = orders.value.filter(order => 
    order.symbol.toLowerCase().includes(orderSearch.value.toLowerCase()) ||
    (order.name && order.name.toLowerCase().includes(orderSearch.value.toLowerCase()))
  )
  
  return filtered.slice(
    (currentPage.value - 1) * pageSize.value, 
    currentPage.value * pageSize.value
  )
})

// 判断是否为固定交易对模板
const isFixedSymbolTemplate = computed(() => {
  if (!strategyForm.value.stockSelectionTemplateId) return false
  
  const selectedTemplate = symbolSelectionTemplates.value.find(
    t => t.id === strategyForm.value.stockSelectionTemplateId
  )
  if (!selectedTemplate) return false
  
  return selectedTemplate.cnClassName === '固定交易对'
})

// 参数接口定义
interface IndicatorParameter {
  name: string
  label: string
  description: string
  type: string
  defaultValue: any
}

// 过滤出唯一的选股模板（按描述或类名去重）
const uniqueSymbolSelectionTemplates = computed(() => {
  // 用于跟踪已处理的模板描述
  const processedDescriptions = new Set();
  const processedClassNames = new Set();
  
  // 筛选结果数组
  const uniqueTemplates: any[] = [];
  
  // 遍历所有模板
  symbolSelectionTemplates.value.forEach(template => {
    // 优先使用描述作为唯一键
    if (template.className && !processedDescriptions.has(template.className)) {
      processedDescriptions.add(template.className);
      uniqueTemplates.push(template);
    }
    // 如果没有描述，则使用类名
    else if (template.className && !processedClassNames.has(template.className) && !template.className) {
      processedClassNames.add(template.className);
      uniqueTemplates.push(template);
    }
    // 如果既没有描述也没有类名，则使用ID作为唯一标识
    else if (!template.className && !template.className && 
             !uniqueTemplates.some(t => t.id === template.id)) {
      uniqueTemplates.push(template);
    }
  });
  
  return uniqueTemplates;
});

// 检测参数类型
const detectParamType = (name: string, value: any): string => {
  // 根据参数值自动检测类型
  if (typeof value === 'number' || value === '0' || !isNaN(Number(value))) {
    return 'number'
  } else if (typeof value === 'boolean' || value === 'true' || value === 'false') {
    return 'boolean'
  }
  
  // 根据参数名称推测类型
  if (name.toLowerCase().includes('percent') || 
      name.toLowerCase().includes('ratio') || 
      name.toLowerCase().includes('rate') || 
      name.toLowerCase().includes('amount') || 
      name.toLowerCase().includes('size') || 
      name.toLowerCase().includes('price') ||
      name.toLowerCase().includes('period') || 
      name.toLowerCase().includes('days')) {
    return 'number'
  }
  
  if (name.toLowerCase().includes('enable') || 
      name.toLowerCase().includes('active') || 
      name.toLowerCase().includes('is') || 
      name.toLowerCase().includes('has') || 
      name.toLowerCase().includes('use')) {
    return 'boolean'
  }
  
  return 'string'
}

// 获取模板参数
function getTemplateParams(templateId: any, type: string = 'stock'): IndicatorParameter[] {
  if (!templateId) {
    return []
  }
  
  // 如果传入的是对象而不是ID
  if (typeof templateId === 'object' && templateId.id) {
    templateId = templateId.id
  }
  
  // 根据类型选择不同的模板集合
  let templates;
  if (type === 'entry') {
    templates = positionTemplates.value // 在StrategyDetail中使用positionTemplates代替openPositionTemplates
  } else if (type === 'stock') {
    templates = symbolSelectionTemplates.value
  } else if (type === 'exit') {
    templates = profitLossTemplates.value
  } else if (type === 'fund') {
    templates = positionTemplates.value
  } else {
    templates = symbolSelectionTemplates.value // 默认使用选股模板
  }
  
  // 查找匹配的模板
  const template = templates.find((t: any) => t.id === templateId)
  
  console.log('找到模板:', template, '类型:', type, '模板ID:', templateId)
  
  // 如果在API返回中找到了模板定义，则使用API返回的参数描述
  if (template) {
    // 打印模板的相关参数
    console.log('模板的参数信息:', {
      classArgs: template.classArgs,
      classArgsDes: template.classArgsDes,
      funArgs: template.funArgs,
      funArgsDes: template.funArgsDes
    })
    
    // 初始化参数数组
    let params: IndicatorParameter[] = []
    
    // 确保classArgsDes是有效对象
    const hasClassArgsDes = template.classArgsDes && 
                          typeof template.classArgsDes === 'object' && 
                          !Array.isArray(template.classArgsDes) && 
                          Object.keys(template.classArgsDes).length > 0;
    
    // 确保funArgsDes是有效对象
    const hasFunArgsDes = template.funArgsDes && 
                        typeof template.funArgsDes === 'object' && 
                        !Array.isArray(template.funArgsDes) && 
                        Object.keys(template.funArgsDes).length > 0;
    
    console.log('参数检查:', { hasClassArgsDes, hasFunArgsDes });
    
    // 对于模板，优先使用classArgsDes，表示选股模板的参数
    if (hasClassArgsDes) {
      console.log('使用classArgsDes参数描述，键有:', Object.keys(template.classArgsDes))
      // 将类参数描述转换为参数数组
      params = Object.entries(template.classArgsDes).map(([name, des]) => {
        // 查找参数默认值
        let defaultValue = ''
        
        // 如果存在类参数，则从中获取默认值
        if (template.classArgs && 
            typeof template.classArgs === 'object' && 
            !Array.isArray(template.classArgs) && 
            template.classArgs[name] !== undefined) {
          defaultValue = template.classArgs[name]
          console.log(`参数[${name}]默认值:`, defaultValue)
        }
        
        // 检测参数类型
        const paramType = detectParamType(name, defaultValue)
        
        return {
          name,
          label: des as string || name,
          description: des as string || name,
          type: paramType,
          defaultValue,
        }
      })
    }
    console.log('提取的参数:', params)
    return params
  }
  
  console.log('未找到模板，返回空参数数组')
  return []
}

// 从方法对象中提取参数
function extractMethodParams(method: any): IndicatorParameter[] {
  // 初始化参数数组
  let params: IndicatorParameter[] = []
  
  // 调试方法的参数描述
  console.log('方法的参数描述:', {
    funArgsDes: method.funArgsDes ? Object.keys(method.funArgsDes) : '无',
    classArgsDes: method.classArgsDes ? Object.keys(method.classArgsDes) : '无'
  })
  
  // 优先使用函数参数描述
  if (method.funArgsDes && 
      typeof method.funArgsDes === 'object' && 
      !Array.isArray(method.funArgsDes) && 
      Object.keys(method.funArgsDes).length > 0) {
    
    console.log('使用方法的funArgsDes')
    // 将函数参数描述转换为参数数组
    params = Object.entries(method.funArgsDes).map(([name, des]) => {
      // 查找参数默认值
      let defaultValue = ''
      
      // 如果存在函数参数，则从中获取默认值
      if (method.funArgs && method.funArgs[name] !== undefined) {
        defaultValue = method.funArgs[name]
      }
      
      // 检测参数类型
      const paramType = detectParamType(name, defaultValue)
      
      return {
        name,
        label: des as string || name,
        description: des as string || name,
        type: paramType,
        defaultValue,
      }
    })
  }

  console.log('方法参数数量:', params.length)
  return params
}

// 获取指标参数
function getIndicatorParams(methodName: string, methodType: string = 'stock'): IndicatorParameter[] {
  console.log(`查找方法 ${methodName} 的参数，类型: ${methodType}`);
  
  // 如果方法名为空，则返回空数组
  if (!methodName) {
    console.log('方法名为空，返回空数组');
    return [];
  }
  
  // 根据类型选择不同的方法集合
  let methods;
  if (methodType === 'stock') {
    const stockMethodsList = stockSelectionMethods.value;  // 使用计算属性但不修改
    methods = stockMethodsList;
    console.log(`选股方法数量: ${methods.length}`);
  } else if (methodType === 'exit') {
    const stopLossMethodsList = stopLossMethods.value;  // 使用计算属性但不修改
    methods = stopLossMethodsList;
    console.log(`止损方法数量: ${methods.length}`);
  } else if (methodType === 'entry' || methodType === 'fund') {
    const positionMethodsList = positionMethods.value;  // 使用计算属性但不修改
    methods = positionMethodsList;
    console.log(`仓位方法数量: ${methods.length}`);
  } else {
    console.log(`未知方法类型: ${methodType}，返回空数组`);
    return [];
  }
  
  // 遍历方法列表，查找匹配的方法
  for (const method of methods) {
    if (method.funName === methodName) {
      console.log(`找到匹配方法 ${methodName}，准备返回参数`);
      
      // 检查方法是否有params属性
      if (method.params && Array.isArray(method.params)) {
        console.log(`方法 ${methodName} 的参数:`, method.params);
        return method.params;
      }
      
      // 如果没有params属性，尝试使用convertArgsToParams转换
      if (method.funArgs) {
        console.log(`使用funArgs和funArgsDes生成方法 ${methodName} 的参数`);
        return convertArgsToParams(method.funArgs, method.funArgsDes);
      }
      
      console.log(`方法 ${methodName} 没有可用参数，返回空数组`);
      return [];
    }
  }
  
  // 打印所有可用方法名称，帮助排查问题
  console.log(`方法 ${methodName} 未找到，可用的方法有:`, methods.map(m => m.funName));
  
  // 如果没找到匹配的方法，则返回空数组
  return [];
}

// 获取方法显示名称（按优先级：中文名称 > 方法名称 > 类名称）
function getMethodDisplayName(method: any): string {
  if (!method) return '未知方法'
  
  console.log('获取方法显示名称:', method)
  
  // 优先使用cnFunName作为显示
  if (method.cnFunName) return method.cnFunName

  return "无需选择"
}

// 获取模板名称
const getTemplateName = (template: any) => {
  return template.cnClassName || template.className || '未命名模板'
}

// 获取模板描述
const getTemplateDescription = (template: any) => {
  if (!template) return ''
  return template.description || template.fileName || template.name || '未知模板'
}

// 获取方法名称（显示中文名称）
const getMethodName = (className: string): string => {
  if (!className) return '未找到方法'
  
  // 使用symbolSelectionTemplates
  const methods = symbolSelectionTemplates.value;
  
  const method = methods.find((m: any) => m.className === className)
  if (!method) return ""
  
  // 优先使用cnFunName，其次是funName
  return method.cnFunName || ""
}

// 获取方法描述
const getMethodDescription = (className: string): string => {
  if (!className) return ''
  
  // 使用symbolSelectionTemplates
  const methods = symbolSelectionTemplates.value;
  
  const method = methods.find((m: any) => m.className === className)
  if (!method) return ""
  
  // 构建一个更详细的描述，使用中文名称
  const classNameText = method.cnClassName
  const funNameText = method.cnFunName
  
  return `${classNameText} - ${funNameText}`
}

// 辅助函数：使用多种匹配策略查找方法
const findMethodByName = (methodName: string, methodsList: any[]) => {
  if (!methodName || !methodsList || !Array.isArray(methodsList) || methodsList.length === 0) {
    return null;
  }
  
  console.log(`尝试查找方法: ${methodName}, 可用方法数量: ${methodsList.length}`);
  
  // 尝试直接使用funName匹配
  let method = methodsList.find(m => m.funName === methodName);
  if (method) {
    console.log(`通过funName找到方法: ${method.funName}`);
    return method;
  }
  
  // 尝试使用cnFunName匹配
  method = methodsList.find(m => m.cnFunName === methodName);
  if (method) {
    console.log(`通过cnFunName找到方法: ${method.funName}`);
    return method;
  }
  
  // 尝试使用不区分大小写的funName匹配
  if (typeof methodName === 'string') {
    const lowerMethodName = methodName.toLowerCase();
    method = methodsList.find(m => m.funName && m.funName.toLowerCase() === lowerMethodName);
    if (method) {
      console.log(`通过不区分大小写的funName找到方法: ${method.funName}`);
      return method;
    }
  }
  
  console.log(`未找到匹配的方法: ${methodName}`);
  return null;
}

// 保存策略配置
const saveStrategyConfig = async () => {
  if (!strategy.value || !strategy.value.id) {
    ElMessage.error('策略信息不完整，无法保存')
    return
  }
  
  savingConfig.value = true
  
  try {
    // 转换参数类型
    convertAllParamsTypes();
    
    // 定义转换方法名称的函数 - 使用中文名称来获取真实的方法名
    const convertMethodName = (cnMethodName: string, methodList: any[]): string => {
      if (!cnMethodName || !methodList || methodList.length === 0) return cnMethodName;
      
      const method = methodList.find(m => m.cnFunName === cnMethodName);
      if (method && method.funName) {
        console.log(`转换方法名: ${cnMethodName} -> ${method.funName}`);
        return method.funName;
      }
      
      return cnMethodName;
    };
    
    // 转换各个方法名
    const stockSelectionFunName = convertMethodName(strategyForm.value.stockSelectionMethod, stockSelectionMethods.value);
    const stopLossFunName = convertMethodName(strategyForm.value.stopLossMethod, stopLossMethods.value);
    const positionFunName = convertMethodName(strategyForm.value.positionMethod, positionMethods.value);
    
    // 准备策略数据
    const extraData = {
      // 选股策略
      stockSelectionTemplateId: strategyForm.value.stockSelectionTemplateId,
      stockSelectionMethod: stockSelectionFunName, // 使用转换后的方法名
      stockSelectionParams: strategyForm.value.stockSelection.templateParams,
      stockSelectionMethodParams: strategyForm.value.stockSelectionMethod && strategyForm.value.stockSelection.params[strategyForm.value.stockSelectionMethod] ? 
                              strategyForm.value.stockSelection.params[strategyForm.value.stockSelectionMethod] : {},
      
      // 止盈止损策略
      stopLossTemplateId: strategyForm.value.stopLoss.templateId,
      stopLossMethod: stopLossFunName, // 使用转换后的方法名
      stopLossParams: strategyForm.value.stopLoss.params,
      stopLossMethodParams: strategyForm.value.stopLoss.methodParams,
      
      // 资金管理策略
      positionTemplateId: strategyForm.value.position.templateId,
      positionMethod: positionFunName, // 使用转换后的方法名
      positionParams: strategyForm.value.position.params,
      positionMethodParams: strategyForm.value.position.methodParams,
      capital: strategyForm.value.position.size,
      maxPositions: strategyForm.value.position.maxPositions,
      lever: strategyForm.value.lever.toString() // 添加杠杆值，转换为字符串
    }
    
    // 如果是固定交易对模板，把交易对数组放入templateParams
    if (isFixedSymbolTemplate.value && symbols.value.length > 0) {
      extraData.stockSelectionParams = {
        ...strategyForm.value.stockSelection.templateParams,
        symbols: symbols.value.filter(s => s.trim() !== '') // 过滤掉空白交易对
      }
    }
    
    // 构建提交数据
    const updateData = {
      id: strategy.value.id,
      strategyName: strategy.value.name,
      description: strategy.value.description,
      remark: JSON.stringify(extraData),
      parameters: {
        stockSelection: strategyForm.value.stockSelectionTemplateId || undefined,
        stopLoss: strategyForm.value.stopLoss.templateId || undefined,
        position: strategyForm.value.position.templateId || undefined
      }
    }
    
    console.log('保存策略配置:', updateData);
    
    await QuantAPI.updateStrategy(updateData)
    ElMessage.success('策略配置保存成功')
    
    // 重新加载策略数据
    await fetchStrategyData()
  } catch (error) {
    console.error('保存策略配置失败', error)
    ElMessage.error('保存策略配置失败，请重试')
  } finally {
    savingConfig.value = false
  }
}

// 转换表单中所有参数的数据类型
const convertAllParamsTypes = () => {
  // 辅助函数：转换对象中的参数类型
  const convertObjectParams = (paramsObj: Record<string, any>) => {
    if (!paramsObj || typeof paramsObj !== 'object') return;
    
    // 遍历对象的所有属性
    Object.keys(paramsObj).forEach(key => {
      const value = paramsObj[key];
      
      // 处理数字字符串
      if (typeof value === 'string' && !isNaN(Number(value))) {
        paramsObj[key] = parseFloat(value);
      }
      // 处理布尔值字符串
      else if (typeof value === 'string' && (value.toLowerCase() === 'true' || value.toLowerCase() === 'false')) {
        paramsObj[key] = value.toLowerCase() === 'true';
      }
      // 递归处理嵌套对象
      else if (value && typeof value === 'object' && !Array.isArray(value)) {
        convertObjectParams(value);
      }
    });
  };
  
  // 转换选股模板参数
  convertObjectParams(strategyForm.value.stockSelection.templateParams);
  
  // 转换选股方法参数
  if (strategyForm.value.stockSelectionMethod && strategyForm.value.stockSelection.params[strategyForm.value.stockSelectionMethod]) {
    convertObjectParams(strategyForm.value.stockSelection.params[strategyForm.value.stockSelectionMethod]);
  }
  
  // 转换止盈止损参数
  convertObjectParams(strategyForm.value.stopLoss.params);
  convertObjectParams(strategyForm.value.stopLoss.methodParams);
  
  // 转换资金管理参数
  convertObjectParams(strategyForm.value.position.params);
  convertObjectParams(strategyForm.value.position.methodParams);
  
  console.log('参数类型转换完成');
}

// 加载策略方法和模板
const loadTemplatesAndMethods = async () => {
  try {
    console.log('开始加载策略模板和方法')
    
    // 加载选股模板
    const symbolRes = await TemplatesAPI.getSymbolSelectionTemplates()
    if (symbolRes?.code === 200) {
      symbolSelectionTemplates.value = symbolRes.rows || []
      
      // 处理模板参数
      symbolSelectionTemplates.value.forEach(template => {
        // 确保类参数为对象格式
        if (typeof template.classArgs === 'string') {
          try {
            template.classArgs = JSON.parse(template.classArgs)
          } catch (e) {
            console.error('解析classArgs失败:', e)
            template.classArgs = {}
          }
        }
        
        // 确保类参数描述为对象格式
        if (typeof template.classArgsDes === 'string') {
          try {
            template.classArgsDes = JSON.parse(template.classArgsDes)
          } catch (e) {
            console.error('解析classArgsDes失败:', e)
            template.classArgsDes = {}
          }
        }
        
        // 确保函数参数为对象格式
        if (typeof template.funArgs === 'string') {
          try {
            template.funArgs = JSON.parse(template.funArgs)
          } catch (e) {
            console.error('解析funArgs失败:', e)
            template.funArgs = {}
          }
        }
        
        // 确保函数参数描述为对象格式
        if (typeof template.funArgsDes === 'string') {
          try {
            template.funArgsDes = JSON.parse(template.funArgsDes)
          } catch (e) {
            console.error('解析funArgsDes失败:', e)
            template.funArgsDes = {}
          }
        }
      })
    }
    
    // 删除直接赋值的代码，由计算属性自动计算
    // stockSelectionMethods.value = symbolSelectionTemplates.value
    //   .filter(template => template.funName) // 只保留有funName的模板
    //   .map(template => ({
    //     className: template.className,
    //     cnClassName: template.cnClassName,
    //     funName: template.funName,
    //     cnFunName: template.cnFunName,
    //     funArgs: template.funArgs,
    //     funArgsDes: template.funArgsDes,
    //     classArgs: template.classArgs,
    //     classArgsDes: template.classArgsDes,
    //     params: convertArgsToParams(template.funArgs, template.funArgsDes)
    //   }))
    
    // 加载止盈止损模板
    const stopLossRes = await TemplatesAPI.getProfitLossTemplates()
    if (stopLossRes?.code === 200) {
      profitLossTemplates.value = stopLossRes.rows || []
      
      // 处理模板参数
      profitLossTemplates.value.forEach(template => {
        // 确保类参数为对象格式
        if (typeof template.classArgs === 'string') {
          try {
            template.classArgs = JSON.parse(template.classArgs)
          } catch (e) {
            console.error('解析classArgs失败:', e)
            template.classArgs = {}
          }
        }
        
        // 确保类参数描述为对象格式
        if (typeof template.classArgsDes === 'string') {
          try {
            template.classArgsDes = JSON.parse(template.classArgsDes)
          } catch (e) {
            console.error('解析classArgsDes失败:', e)
            template.classArgsDes = {}
          }
        }
        
        // 确保函数参数为对象格式
        if (typeof template.funArgs === 'string') {
          try {
            template.funArgs = JSON.parse(template.funArgs)
          } catch (e) {
            console.error('解析funArgs失败:', e)
            template.funArgs = {}
          }
        }
        
        // 确保函数参数描述为对象格式
        if (typeof template.funArgsDes === 'string') {
          try {
            template.funArgsDes = JSON.parse(template.funArgsDes)
          } catch (e) {
            console.error('解析funArgsDes失败:', e)
            template.funArgsDes = {}
          }
        }
      })
    }
    
    // 删除直接赋值的代码，由计算属性自动计算
    // stopLossMethods.value = profitLossTemplates.value
    //   .filter(template => template.funName) // 只保留有funName的模板
    //   .map(template => ({
    //     className: template.className,
    //     cnClassName: template.cnClassName,
    //     funName: template.funName, // 确保保存funName
    //     cnFunName: template.cnFunName,
    //     funArgs: template.funArgs,
    //     funArgsDes: template.funArgsDes,
    //     classArgs: template.classArgs,
    //     classArgsDes: template.classArgsDes,
    //     params: convertArgsToParams(template.funArgs, template.funArgsDes)
    //   }))
    
    // 加载资金管理模板
    const positionRes = await TemplatesAPI.getFundTemplates()
    if (positionRes?.code === 200) {
      positionTemplates.value = positionRes.rows || []
      
      // 处理模板参数
      positionTemplates.value.forEach(template => {
        // 确保类参数为对象格式
        if (typeof template.classArgs === 'string') {
          try {
            template.classArgs = JSON.parse(template.classArgs)
          } catch (e) {
            console.error('解析classArgs失败:', e)
            template.classArgs = {}
          }
        }
        
        // 确保类参数描述为对象格式
        if (typeof template.classArgsDes === 'string') {
          try {
            template.classArgsDes = JSON.parse(template.classArgsDes)
          } catch (e) {
            console.error('解析classArgsDes失败:', e)
            template.classArgsDes = {}
          }
        }
        
        // 确保函数参数为对象格式
        if (typeof template.funArgs === 'string') {
          try {
            template.funArgs = JSON.parse(template.funArgs)
          } catch (e) {
            console.error('解析funArgs失败:', e)
            template.funArgs = {}
          }
        }
        
        // 确保函数参数描述为对象格式
        if (typeof template.funArgsDes === 'string') {
          try {
            template.funArgsDes = JSON.parse(template.funArgsDes)
          } catch (e) {
            console.error('解析funArgsDes失败:', e)
            template.funArgsDes = {}
          }
        }
      })
    }
    
    // 删除直接赋值的代码，由计算属性自动计算
    // positionMethods.value = positionTemplates.value
    //   .filter(template => template.funName) // 只保留有funName的模板
    //   .map(template => ({
    //     className: template.className,
    //     cnClassName: template.cnClassName,
    //     funName: template.funName, // 确保保存funName
    //     cnFunName: template.cnFunName,
    //     funArgs: template.funArgs,
    //     funArgsDes: template.funArgsDes,
    //     classArgs: template.classArgs,
    //     classArgsDes: template.classArgsDes,
    //     params: convertArgsToParams(template.funArgs, template.funArgsDes)
    //   }))
    
    // 确保参数对象初始化
    const stockSelectionMethodsList = stockSelectionMethods.value;  // 使用计算属性的值
    stockSelectionMethodsList.forEach(method => {
      if (method.funName) {
        if (!strategyForm.value.stockSelection.params) {
          strategyForm.value.stockSelection.params = {};
        }
        strategyForm.value.stockSelection.params[method.funName] = strategyForm.value.stockSelection.params[method.funName] || {};
      }
    });
    
    console.log('成功加载模板和方法数据', {
      symbolSelectionTemplates: symbolSelectionTemplates.value.length,
      stockSelectionMethods: stockSelectionMethods.value.length,
      profitLossTemplates: profitLossTemplates.value.length,
      stopLossMethods: stopLossMethods.value.length,
      positionTemplates: positionTemplates.value.length,
      positionMethods: positionMethods.value.length
    })
  } catch (error) {
    console.error('加载策略模板和方法失败', error)
    ElMessage.warning('加载策略模板和方法失败')
  }
}

// 将参数转换为数组格式
const convertArgsToParams = (args: any, argsDes: any) => {
  console.log('convertArgsToParams 输入:', {args, argsDes});
  
  if (!args) {
    console.log('args 为空，返回空数组');
    return [];
  }
  
  // 确保args是对象
  if (typeof args === 'string') {
    try {
      args = JSON.parse(args);
    } catch (e) {
      console.error('无法解析args字符串:', e);
      args = {};
    }
  }
  
  // 确保argsDes是对象
  if (typeof argsDes === 'string') {
    try {
      argsDes = JSON.parse(argsDes);
    } catch (e) {
      console.error('无法解析argsDes字符串:', e);
      argsDes = {};
    }
  }
  
  // 如果args不是对象或是空数组，则返回空数组
  if (!args || typeof args !== 'object' || (Array.isArray(args) && args.length === 0)) {
    console.log('args 不是有效对象，返回空数组');
    return [];
  }
  
  // 如果argsDes不是对象，创建一个空对象作为默认值
  if (!argsDes || typeof argsDes !== 'object') {
    argsDes = {};
  }
  
  const params: any[] = [];
  
  try {
    Object.keys(args).forEach(key => {
      const paramValue = args[key];
      const paramDescription = argsDes[key] || key;
      
      // 确定参数类型
      let paramType = 'string';
      if (typeof paramValue === 'number') {
        paramType = 'number';
      } else if (typeof paramValue === 'boolean') {
        paramType = 'boolean';
      }
      
      console.log(`添加参数 ${key}:`, {value: paramValue, type: paramType, description: paramDescription});
      
      params.push({
        name: key,
        label: paramDescription,
        description: paramDescription,
        defaultValue: paramValue,
        type: paramType
      });
    });
  } catch (error) {
    console.error('处理参数时出错:', error);
  }
  
  console.log('convertArgsToParams 输出 params:', params);
  return params;
}

// 加载策略配置
const loadStrategyConfig = async () => {
  try {
    const strategyId = parseInt(route.params.id as string)
    const response = await QuantAPI.getStrategyDetail(strategyId)
    if (response.code === 200 && response.data) {
      const strategy = response.data
      // 加载策略名称
      strategyForm.value.strategyName = strategy.strategyName
      // 加载杠杆值
      strategyForm.value.lever = 50 // 默认值为 50
      // 加载选股模板
      if (strategy.remark) {
        const extraData = JSON.parse(strategy.remark)
        if (extraData.stockSelectionTemplateId) {
          strategyForm.value.stockSelectionTemplateId = extraData.stockSelectionTemplateId
          // 加载选股方法
          if (extraData.stockSelectionMethod) {
            strategyForm.value.stockSelectionMethod = extraData.stockSelectionMethod
          }
          // 加载选股参数
          if (extraData.stockSelection) {
            strategyForm.value.stockSelection = extraData.stockSelection
          }
        }
        // ... existing code ...
      }
    }
  } catch (error) {
    console.error('加载策略配置失败:', error)
    ElMessage.error('加载策略配置失败')
  }
}

// 获取策略数据
const fetchStrategyData = async () => {
  const strategyId = parseInt(route.params.id as string)
  if (isNaN(strategyId)) {
    ElMessage.error('无效的策略ID')
    router.push('/user')
    return
  }
  
  loading.value = true
  
  try {
    // 获取策略详情
    const strategyRes = await QuantAPI.getStrategyDetail(strategyId)
    strategy.value = strategyRes.data
    
    // 检查策略是否在运行
    try {
      const runningStrategiesRes = await QuantAPI.getRunningStrategies(strategyId)
      if (runningStrategiesRes.code === 200 && runningStrategiesRes.data && runningStrategiesRes.data.includes(strategyId)) {
        strategy.value.status = 'running'
      } else {
        strategy.value.status = 'stopped'
      }
    } catch (error) {
      console.error('获取策略运行状态失败:', error)
      strategy.value.status = 'stopped'
    }
    
    // 获取账户信息
    const accountRes = await get<ListResponse<any>>(`/system/account/${strategy.value.accountId}`)
    if (accountRes.rows && accountRes.rows.length > 0) {
      account.value = accountRes.rows[0]
    }
    
    // 获取持仓信息
    const positionsRes = await UserStrategyAPI.getUserStrategyPositionList({ strategyId })
    positions.value = positionsRes.rows || []
    
    // 获取订单记录
    const ordersRes = await UserStrategyAPI.getUserStrategyOrdersList({ strategyId })
    orders.value = ordersRes.rows || []
    
    // 获取性能报告
    const reportRes = await UserStrategyAPI.getStrategyReportList({ strategyId })
    if (reportRes.rows && reportRes.rows.length > 0) {
      updatePerformanceMetrics(reportRes.rows[0])
    }
    
    // 加载策略配置
    loadStrategyConfig()
    
    // 初始化图表
    initPerformanceChart()
  } catch (error) {
    console.error('获取策略数据失败', error)
    ElMessage.error('获取策略数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 更新性能指标
const updatePerformanceMetrics = (report: any) => {
  if (!report) return
  
  performanceMetrics.value = [
    { 
      label: '总收益率', 
      value: report.totalReturn || 0, 
      format: 'percentage', 
      positive: true 
    },
    { 
      label: '年化收益率', 
      value: report.annualizedReturn || 0, 
      format: 'percentage', 
      positive: true 
    },
    { 
      label: '最大回撤', 
      value: report.maxDrawdown || 0, 
      format: 'percentage', 
      positive: false 
    },
    { 
      label: '夏普比率', 
      value: report.sharpeRatio || 0, 
      format: 'number', 
      positive: true, 
      info: '年化收益率与波动率之比' 
    },
    { 
      label: '盈亏比', 
      value: report.profitFactor || 0, 
      format: 'number', 
      positive: true, 
      info: '平均盈利/平均亏损' 
    },
    { 
      label: '胜率', 
      value: report.winRate || 0, 
      format: 'percentage', 
      positive: true 
    }
  ]
}

// 图表初始化
const initPerformanceChart = async () => {
  if (!performanceChart.value || !strategy.value?.accountId) return
  
  try {
    // 获取初始资金
    const res = await UserStrategyAPI.getAccount(strategy.value.accountId.toString())
    const initialBalance = parseFloat(res.data.balance)
    
    // 按日期对订单进行处理
    const ordersByDate = new Map<string, number>()
    orders.value.forEach(order => {
      const date = new Date(order.time).toISOString().split('T')[0]
      const pnl = parseFloat(order.pnl || '0')
      ordersByDate.set(date, (ordersByDate.get(date) || 0) + pnl)
    })
    
    // 生成所有日期
    const startDate = orders.value.length > 0 ? 
      new Date(Math.min(...orders.value.map(o => new Date(o.time).getTime()))) :
      new Date()
    const endDate = new Date()
    const dates: string[] = []
    const values: number[] = []
    
    let currentDate = new Date(startDate)
    let currentBalance = initialBalance
    
    while (currentDate <= endDate) {
      const dateStr = currentDate.toISOString().split('T')[0]
      dates.push(dateStr)
      
      // 如果当天有交易，更新余额
      if (ordersByDate.has(dateStr)) {
        currentBalance += ordersByDate.get(dateStr)!
      }
      values.push(currentBalance)
      
      currentDate.setDate(currentDate.getDate() + 1)
    }
    
    const chart = echarts.init(performanceChart.value)
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const date = params[0].axisValue
        const value = params[0].data
          return `${date}<br/>净值：${value.toFixed(2)}`
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
  } catch (error) {
    console.error('初始化图表失败', error)
    ElMessage.error('初始化图表失败，请稍后重试')
  }
}

// 分页相关
const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

// 操作策略
const toggleStrategy = async () => {
  if (!strategy.value) return
  
  const newStatus = strategy.value.status === 'running' ? 'stopped' : 'running'
  const actionName = newStatus === 'running' ? '启动' : '停止'
  
  try {
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
      try {
        // 先添加策略
        await QuantAPI.addStrategyToAccount({
          id: strategy.value.id,
          accountId: 0,
          owner: 0
        })
        // 添加成功后再启动策略
        await QuantAPI.runStrategy({
          id: strategy.value.id,
          accountId: 0,
          owner: 0
        })
      } catch (error) {
        // 如果添加或启动失败，直接抛出错误中断操作
        throw error
      }
    } else {
      await QuantAPI.removeStrategy({
        id: strategy.value.id,
        accountId: 0,
        owner: 0
      })
    }
    
    strategy.value.status = newStatus
    ElMessage.success(`策略已${actionName}`)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`操作失败，请稍后重试`)
    }
  }
}

const editStrategy = () => {
  router.push(`/create-strategy?id=${strategy.value.id}`)
}

const deleteStrategy = async () => {
  if (!strategy.value) return
  
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
    
    await QuantAPI.deleteStrategy(strategy.value.id)
    ElMessage.success('策略已删除')
    router.push('/user')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败，请稍后重试')
    }
  }
}

// 监听时间范围变化，重新加载数据
watch(timeRange, () => {
  // 实际应该根据时间范围重新获取数据
  initPerformanceChart()
})

// 回测功能
const runBacktest = async () => {
  // 已禁用回测功能，不执行实际的回测操作
  ElMessage.warning({
    message: '回测功能暂时不可用，该功能正在维护中。',
    duration: 5000
  })
  return

  /* 原回测代码已注释
  if (!strategy.value) return
  
  if (!backtestForm.value.start || !backtestForm.value.end) {
    ElMessage.warning('请选择回测的开始和结束日期')
    return
  }
  
  backtestLoading.value = true
  try {
    const res = await QuantAPI.backTestStrategy({
      id: strategy.value.id,
      symbol: '', // 这个可能在您的API中不需要，根据实际情况调整
      start: backtestForm.value.start,
      end: backtestForm.value.end,
      interval: backtestForm.value.interval
    })
    
    if (res.code === 200) {
      ElMessage.success('回测完成')
      // 回测结果直接从响应中获取
      backtestResult.value = res
      
      // 可以在这里添加代码更新图表或其他UI组件
    } else {
      ElMessage.error(res.msg || '回测失败')
    }
  } catch (error: any) {
    console.error('回测失败', error)
    // 特别处理回测引擎连接错误
    if (error.message === '回测引擎服务未启动') {
      ElMessage.error({
        message: '回测引擎服务未启动，请联系管理员启动服务后再试',
        duration: 7000
      })
    } else {
      ElMessage.error('回测失败，请稍后重试')
    }
  } finally {
    backtestLoading.value = false
  }
  */
}

// 初始化回测表单
const initBacktestForm = () => {
  // 默认回测时间范围：最近一年
  const end = new Date()
  const start = new Date()
  start.setFullYear(start.getFullYear() - 1)
  
  backtestForm.value.end = end.toISOString().split('T')[0]
  backtestForm.value.start = start.toISOString().split('T')[0]
}

// 初始化
onMounted(async () => {
  loading.value = true
  try {
    // 先加载模板和方法数据
    await loadTemplatesAndMethods()
    
    // 然后加载策略数据
    await fetchStrategyData()
    
    // 初始化回测表单
  initBacktestForm()
  } catch (error) {
    console.error('初始化数据失败', error)
    ElMessage.error('加载数据失败，请刷新页面重试')
  } finally {
    loading.value = false
  }
})

// 格式化工具函数
const formatNumber = (value: number | string | undefined | null) => {
  if (value === undefined || value === null) return '-'
  const num = typeof value === 'string' ? parseFloat(value) : value
  return new Intl.NumberFormat('zh-CN', { 
    minimumFractionDigits: 2, 
    maximumFractionDigits: 2 
  }).format(num)
}

const formatPercentage = (value: number | string | undefined | null) => {
  if (value === undefined || value === null) return '-'
  const num = typeof value === 'string' ? parseFloat(value) : value
  return (num * 100).toFixed(2) + '%'
}

const formatMetricValue = (value: number, format: string) => {
  if (format === 'percentage') {
    return formatPercentage(value)
  } else if (format === 'currency') {
    return `¥ ${formatNumber(value)}`
  }
  return value.toFixed(2)
}

const formatDate = (dateStr: string | undefined | null) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const formatDateTime = (dateStr: string | undefined | null) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const getValueClass = (value: any) => {
  if (value === undefined || value === null) return ''
  
  // 如果是对象（性能指标）
  if (typeof value === 'object') {
    const num = value.value
    // 如果是最大回撤这样的负向指标
    if (!value.positive) {
      return num > 0 ? 'negative' : 'positive'
    }
    return num > 0 ? 'positive' : 'negative'
  }
  
  // 如果是数值
  const num = typeof value === 'string' ? parseFloat(value) : value
  return num > 0 ? 'positive' : (num < 0 ? 'negative' : '')
}

// 添加交易对
const addSymbol = () => {
  symbols.value.push('')
}

// 删除交易对
const removeSymbol = (index: number) => {
  symbols.value.splice(index, 1)
}

// 监听选股模板ID变化
watch(() => strategyForm.value.stockSelectionTemplateId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    // 清空旧的模板参数
    strategyForm.value.stockSelection.templateParams = {}
    strategyForm.value.stockSelectionMethod = ''
    // 清空方法参数
    strategyForm.value.stockSelection.params = {}
    
    // 获取新模板的参数，并设置默认值
    const params = getTemplateParams(newVal)
    if (params.length > 0) {
      params.forEach(param => {
        // 只有当参数有默认值时才设置
        if (param.defaultValue !== undefined && param.defaultValue !== null && param.defaultValue !== '') {
          strategyForm.value.stockSelection.templateParams[param.name] = param.defaultValue
        }
      })
    }
    
    // 自动设置选股方法 - 根据当前选中的模板获取所有相关方法
    if (newVal) {
      const selectedTemplate = symbolSelectionTemplates.value.find(t => t.id === newVal)
      if (selectedTemplate) {
        console.log('选中模板:', selectedTemplate)
        
        // 如果是固定交易对模板，清空交易对列表
        if (selectedTemplate.cnClassName === '固定交易对') {
          symbols.value = []
        }
        
        // 找到所有与当前模板相关的方法
        const methods = stockSelectionMethods.value
        
        if (methods.length > 0) {
          // 检查模板是否已指定方法
          if (selectedTemplate.funName) {
            console.log('使用模板指定的方法:', selectedTemplate.funName)
            strategyForm.value.stockSelectionMethod = selectedTemplate.funName
          } else {
            // 默认选择第一个方法
            const firstMethod = methods[0]
            if (firstMethod && firstMethod.funName) {
              console.log('默认选择方法:', firstMethod.funName)
              strategyForm.value.stockSelectionMethod = firstMethod.funName
            }
          }
          
          // 获取选择的方法参数
          if (strategyForm.value.stockSelectionMethod) {
            // 获取参数列表
            const methodParams = getIndicatorParams(strategyForm.value.stockSelectionMethod, 'stock')
            
            // 初始化参数对象
            if (!strategyForm.value.stockSelection.params[strategyForm.value.stockSelectionMethod]) {
              strategyForm.value.stockSelection.params[strategyForm.value.stockSelectionMethod] = {}
            }
            
            // 使用默认值初始化
            methodParams.forEach(param => {
              if (param.name && param.defaultValue !== undefined) {
                strategyForm.value.stockSelection.params[strategyForm.value.stockSelectionMethod][param.name] = param.defaultValue
              }
            })
          }
        }
      }
    }
  }
}, { immediate: true })

// 确保strategyForm.stockSelection.params初始化，防止访问错误
watch(() => strategyForm.value.stockSelectionMethod, (newVal) => {
  // 只在有选股方法时初始化参数
  if (newVal) {
    // 检查对应方法的参数是否已初始化
    if (!strategyForm.value.stockSelection.params[newVal]) {
            // 初始化方法参数对象
      strategyForm.value.stockSelection.params[newVal] = {};
            
            // 获取参数列表
      const params = getIndicatorParams(newVal);
            
            // 使用默认值初始化
      params.forEach(param => {
              if (param.name && param.defaultValue !== undefined) {
          strategyForm.value.stockSelection.params[newVal][param.name] = param.defaultValue;
        }
      });
    }
  }
}, { immediate: true })

// 监听止盈止损模板ID变化
watch(() => strategyForm.value.stopLoss.templateId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    // 清空旧的模板参数
    strategyForm.value.stopLoss.params = {}
    strategyForm.value.stopLossMethod = ''
    strategyForm.value.stopLoss.method = ''
    strategyForm.value.stopLoss.methodParams = {}
    
    // 获取新模板的参数，并设置默认值
    const params = getTemplateParams(newVal, 'exit')
    if (params.length > 0) {
      params.forEach(param => {
        // 只有当参数有默认值时才设置
        if (param.defaultValue !== undefined && param.defaultValue !== null && param.defaultValue !== '') {
          strategyForm.value.stopLoss.params[param.name] = param.defaultValue
        }
      })
    }
    
    // 自动设置止盈止损方法 - 根据当前选中的模板获取所有相关方法
    if (newVal) {
      const selectedTemplate = profitLossTemplates.value.find(t => t.id === newVal)
      if (selectedTemplate) {
        console.log('找到选中的止盈止损模板:', selectedTemplate)
        
        // 找到所有与当前模板相关的方法
        const methods = stopLossMethods.value
        
        if (methods.length > 0) {
          // 检查模板是否已指定方法
          if (selectedTemplate.funName) {
            console.log('使用模板指定的方法:', selectedTemplate.funName)
            strategyForm.value.stopLossMethod = selectedTemplate.funName
            strategyForm.value.stopLoss.method = selectedTemplate.funName
          } else {
            // 默认选择第一个方法
            const firstMethod = methods[0]
            if (firstMethod && firstMethod.funName) {
              console.log('默认选择止盈止损方法:', firstMethod.funName)
              strategyForm.value.stopLossMethod = firstMethod.funName
              strategyForm.value.stopLoss.method = firstMethod.funName
            }
          }
          
          // 获取选择的方法参数
          if (strategyForm.value.stopLossMethod) {
            // 获取参数列表
            const methodParams = getIndicatorParams(strategyForm.value.stopLossMethod, 'exit')
            
            // 使用默认值初始化
            methodParams.forEach(param => {
              if (param.name && param.defaultValue !== undefined) {
                strategyForm.value.stopLoss.methodParams[param.name] = param.defaultValue
              }
            })
          }
        }
      }
    }
  }
}, { immediate: true })

// 监听止盈止损方法变化
watch(() => strategyForm.value.stopLossMethod, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    // 清空旧的方法参数
    strategyForm.value.stopLoss.methodParams = {}
    
    // 设置方法名称到 stopLoss.method
    strategyForm.value.stopLoss.method = newVal
    
    // 获取新方法的参数，并设置默认值
    const params = getIndicatorParams(newVal, 'exit')
    if (params.length > 0) {
      params.forEach(param => {
        // 只有当参数有默认值时才设置
        if (param.defaultValue !== undefined && param.defaultValue !== null && param.defaultValue !== '') {
          strategyForm.value.stopLoss.methodParams[param.name] = param.defaultValue
        }
      })
    }
  }
}, { immediate: true })

// 监听资金管理策略模板 ID 变化
watch(() => strategyForm.value.position.templateId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    // 清空旧的模板参数
    strategyForm.value.position.params = {}
    strategyForm.value.positionMethod = ''
    strategyForm.value.position.method = ''
    strategyForm.value.position.methodParams = {}
    
    // 获取新模板的参数，并设置默认值
    const params = getTemplateParams(newVal, 'fund')
    if (params.length > 0) {
      params.forEach(param => {
        // 只有当参数有默认值时才设置
        if (param.defaultValue !== undefined && param.defaultValue !== null && param.defaultValue !== '') {
          strategyForm.value.position.params[param.name] = param.defaultValue
        }
      })
    }
    
    // 自动设置资金管理方法 - 根据当前选中的模板获取所有相关方法
    if (newVal) {
      const selectedTemplate = positionTemplates.value.find(t => t.id === newVal)
      if (selectedTemplate) {
        console.log('找到选中的资金管理模板:', selectedTemplate)
        
        // 找到所有与当前模板相关的方法
        const methods = positionMethods.value
        
        if (methods.length > 0) {
          // 检查模板是否已指定方法
          if (selectedTemplate.funName) {
            console.log('使用模板指定的方法:', selectedTemplate.funName)
            strategyForm.value.positionMethod = selectedTemplate.funName
            strategyForm.value.position.method = selectedTemplate.funName
          } else {
            // 默认选择第一个方法
            const firstMethod = methods[0]
            if (firstMethod && firstMethod.funName) {
              console.log('默认选择资金管理方法:', firstMethod.funName)
              strategyForm.value.positionMethod = firstMethod.funName
              strategyForm.value.position.method = firstMethod.funName
            }
          }
          
          // 获取选择的方法参数
          if (strategyForm.value.positionMethod) {
            // 获取参数列表
            const methodParams = getIndicatorParams(strategyForm.value.positionMethod, 'fund')
            
            // 使用默认值初始化
            methodParams.forEach(param => {
              if (param.name && param.defaultValue !== undefined) {
                strategyForm.value.position.methodParams[param.name] = param.defaultValue
              }
            })
          }
        }
      }
    }
  }
}, { immediate: true })

// 监听资金管理方法变化
watch(() => strategyForm.value.positionMethod, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    // 清空旧的方法参数
    strategyForm.value.position.methodParams = {}
    
    // 设置方法名称到 position.method
    strategyForm.value.position.method = newVal
    
    // 获取新方法的参数，并设置默认值
    const params = getIndicatorParams(newVal, 'fund')
    if (params.length > 0) {
      params.forEach(param => {
        // 只有当参数有默认值时才设置
        if (param.defaultValue !== undefined && param.defaultValue !== null && param.defaultValue !== '') {
          strategyForm.value.position.methodParams[param.name] = param.defaultValue
        }
      })
    }
  }
}, { immediate: true })

// 监听 position.size (资金)变化，同步更新资金管理策略参数
watch(() => strategyForm.value.position.size, (newVal) => {
  if (newVal && strategyForm.value.position.methodParams) {
    // 将资金数值同步到策略参数的 capital 字段
    strategyForm.value.position.methodParams.capital = newVal
  }
}, { immediate: true })

// 监听 position.maxPositions (最大持仓)变化，同步更新资金管理策略参数
watch(() => strategyForm.value.position.maxPositions, (newVal) => {
  if (newVal !== undefined && strategyForm.value.position.methodParams) {
    // 将最大持仓数同步到策略参数的 maxPositions 字段
    strategyForm.value.position.methodParams.maxPositions = newVal
  }
}, { immediate: true })

// 监听资金管理策略参数 capital 变化，同步更新资金
watch(() => strategyForm.value.position.methodParams?.capital, (newVal) => {
  if (newVal !== undefined && newVal !== null) {
    // 同步到 position.size
    strategyForm.value.position.size = newVal
  }
}, { immediate: true })

// 监听资金管理策略参数 maxPositions 变化，同步更新最大持仓
watch(() => strategyForm.value.position.methodParams?.maxPositions, (newVal) => {
  if (newVal !== undefined && newVal !== null) {
    // 同步到 position.maxPositions
    strategyForm.value.position.maxPositions = newVal
  }
}, { immediate: true })

// 辅助函数 - 记录方法详情
const logMethodDetails = (method: any, category: string) => {
  console.log(`[${category}] 方法信息:`, { 
    className: method.className, 
    cnClassName: method.cnClassName,
    funName: method.funName, 
    cnFunName: method.cnFunName
  });
}

// 计算属性：股票选择方法
const stockSelectionMethods = computed(() => {
  // 日志记录
  console.log('计算 stockSelectionMethods, 模板ID:', strategyForm.value.stockSelectionTemplateId)
  
  // 检查是否有选择的模板
  if (!strategyForm.value.stockSelectionTemplateId) {
    console.log('未选择股票选择模板')
    return []
  }
  
  // 查找当前选中的模板对象
  const selectedTemplate = symbolSelectionTemplates.value.find(
    t => t.id === strategyForm.value.stockSelectionTemplateId
  )
  if (!selectedTemplate) {
    console.log('未找到选中的股票选择模板')
    return []
  }
  
  // 找到所有与当前模板类名相同的模板
  const relatedTemplates = symbolSelectionTemplates.value.filter(
    t => (t.className && t.className === selectedTemplate.className)
  )
  console.log('找到相关模板数量:', relatedTemplates.length)
  
  // 映射出方法
  return relatedTemplates
    .filter(template => template.funName)
    .map(template => {
      return {
        label: template.funName,
        value: template.funName,
        funName: template.funName, // 添加funName属性
        cnFunName: template.cnFunName,
        funArgs: template.funArgs,
        funArgsDes: template.funArgsDes,
        className: template.className,
        cnClassName: template.cnClassName,
        classArgs: template.classArgs,
        classArgsDes: template.classArgsDes,
        template: template,
        params: convertArgsToParams(template.funArgs, template.funArgsDes)
      }
    })
})

// 计算属性：止损方法
const stopLossMethods = computed(() => {
  // 日志记录
  console.log('计算 stopLossMethods, 模板ID:', strategyForm.value.stopLoss.templateId)
  
  // 检查是否有选择的模板
  if (!strategyForm.value.stopLoss.templateId) {
    console.log('未选择止损模板')
    return []
  }
  
  // 查找当前选中的模板对象
  const selectedTemplate = profitLossTemplates.value.find(t => t.id === strategyForm.value.stopLoss.templateId)
  if (!selectedTemplate) {
    console.log('未找到选中的止损模板')
    return []
  }
  
  // 找到所有与当前模板类名相同的模板
  const relatedTemplates = profitLossTemplates.value.filter(t => 
    (t.className && t.className === selectedTemplate.className)
  )
  console.log('找到相关止损模板数量:', relatedTemplates.length)
  
  // 映射出方法
  return relatedTemplates
    .filter(template => template.funName)
    .map(template => {
      return {
        label: template.funName,
        value: template.funName,
        funName: template.funName, // 添加funName属性
        cnFunName: template.cnFunName,
        funArgs: template.funArgs,
        funArgsDes: template.funArgsDes,
        className: template.className,
        cnClassName: template.cnClassName,
        classArgs: template.classArgs,
        classArgsDes: template.classArgsDes,
        template: template,
        params: convertArgsToParams(template.funArgs, template.funArgsDes)
      }
    })
})

// 计算属性：仓位管理方法
const positionMethods = computed(() => {
  // 日志记录
  console.log('计算 positionMethods, 模板ID:', strategyForm.value.position.templateId)
  
  // 检查是否有选择的模板
  if (!strategyForm.value.position.templateId) {
    console.log('未选择仓位管理模板')
    return []
  }
  
  // 查找当前选中的模板对象
  const selectedTemplate = positionTemplates.value.find(t => t.id === strategyForm.value.position.templateId)
  if (!selectedTemplate) {
    console.log('未找到选中的仓位管理模板')
    return []
  }
  
  // 找到所有与当前模板类名相同的模板
  const relatedTemplates = positionTemplates.value.filter(t => 
    (t.className && t.className === selectedTemplate.className)
  )
  console.log('找到相关仓位管理模板数量:', relatedTemplates.length)
  
  // 映射出方法
  return relatedTemplates
    .filter(template => template.funName)
    .map(template => {
      return {
        label: template.funName,
        value: template.funName,
        funName: template.funName, // 添加funName属性
        cnFunName: template.cnFunName,
        funArgs: template.funArgs,
        funArgsDes: template.funArgsDes,
        className: template.className,
        cnClassName: template.cnClassName,
        classArgs: template.classArgs,
        classArgsDes: template.classArgsDes,
        template: template,
        params: convertArgsToParams(template.funArgs, template.funArgsDes)
      }
    })
})
</script>

<style scoped lang="scss">
.strategy-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  
  .loading-container {
    padding: 40px;
  }
  
  .strategy-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    .strategy-title {
      h1 {
        margin: 0 0 10px 0;
        font-size: 28px;
      }
      
      .strategy-tags {
        display: flex;
        gap: 10px;
      }
    }
    
    .strategy-actions {
      display: flex;
      gap: 10px;
    }
  }
  
  .strategy-info {
    margin-bottom: 20px;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h2 {
      margin: 0;
      font-size: 20px;
    }
    
    .order-search {
      width: 200px;
    }
  }
  
  .performance-card,
  .account-card,
  .positions-card,
  .orders-card,
  .backtest-card,
  .strategy-config-card {
    margin-bottom: 20px;
  }
  
  .metric-card {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
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
    
    .metric-info {
      font-size: 12px;
      color: #c0c4cc;
    }
  }
  
  .chart-container {
    margin-top: 20px;
    
    .performance-chart {
      height: 350px;
      width: 100%;
    }
  }
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  
  .positive {
    color: #67c23a;
  }
  
  .negative {
    color: #f56c6c;
  }

  .backtest-card {
    margin-bottom: 20px;
  }

  .backtest-form {
    margin-bottom: 20px;
  }

  .backtest-result {
    margin-top: 20px;
    
    h3 {
      margin-bottom: 15px;
    }
  }
  
  // 策略配置相关样式
  .strategy-config-card {
    margin-bottom: 20px;
    
    .strategy-form {
      .form-section {
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 1px solid #ebeef5;
        
        &:last-child {
          margin-bottom: 0;
          padding-bottom: 0;
          border-bottom: none;
        }
        
        h3 {
          margin: 0 0 20px;
          font-size: 18px;
          font-weight: 500;
          color: #303133;
        }
      }
      
      .params-container {
        margin-top: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        
        .param-config {
          margin-bottom: 15px;
          
          .param-label {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
            
            .param-name {
              margin-right: 5px;
              font-size: 14px;
              color: #606266;
              font-weight: 500;
            }
            
            .el-icon {
              color: #909399;
              cursor: pointer;
              
              &:hover {
                color: #409EFF;
              }
            }
          }
        }
      }
      
      .form-actions {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px;
      }
      
      .symbol-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
        
        .symbol-item {
          display: flex;
          align-items: center;
          gap: 10px;
          
          .symbol-input {
            flex: 1;
          }
          
          .symbol-delete-btn {
            flex-shrink: 0;
          }
        }
        
        .add-symbol-btn {
          margin-top: 10px;
          width: 100%;
        }
      }
    }
  }
}
</style>