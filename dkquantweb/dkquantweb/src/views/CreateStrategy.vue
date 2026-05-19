<template>
  <div class="create-strategy">
    <el-card class="strategy-form" v-loading="loading" style="min-height: 500px;">
      <template #header>
        <div class="card-header">
          <h2>{{ isEdit ? '编辑策略' : '创建策略' }}</h2>
          <div>
            <el-button type="warning" @click="loadDefaultData" :loading="loading">
              加载默认数据
            </el-button>
            <el-button type="primary" @click="handleSubmit" :loading="saving">
              {{ isEdit ? '更新策略' : '保存策略' }}
            </el-button>
          </div>
        </div>
      </template>
      
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        style="width: 100%; padding: 10px;"
      >
        <!-- 基本信息 -->
        <div class="form-section">
          <h3>基本信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="策略名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入策略名称" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="本金" prop="position.size">
                <el-input-number
                  v-model="form.position.size"
                  :min="1000"
                  :step="1000"
                  style="width: 100%"
                >
                  <template #prefix>¥</template>
                </el-input-number>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-form-item label="最大持仓数量" prop="position.maxPositions">
            <el-input-number
              v-model="form.position.maxPositions"
              :min="1"
              :max="100"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="杠杆">
            <el-input-number
              v-model="form.lever"
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
          <!-- 第一步：选择选股模板 -->
          <el-form-item label="选股模板" prop="stockSelectionTemplateId">
            <el-select
              v-model="form.stockSelectionTemplateId"
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
          <div v-if="!isFixedSymbolTemplate && form.stockSelectionTemplateId && getTemplateParams(form.stockSelectionTemplateId).length > 0" class="params-container">
            <el-row :gutter="20">
              <el-col 
                :span="8" 
                v-for="(param, index) in getTemplateParams(form.stockSelectionTemplateId)" 
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
                      v-model="form.stockSelection.templateParams[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                  <template v-else-if="param.type === 'boolean'">
                    <el-switch
                      v-model="form.stockSelection.templateParams[param.name]"
                      active-text="是"
                      inactive-text="否"
                    />
                  </template>
                  <template v-else>
                    <el-input
                      v-model="form.stockSelection.templateParams[param.name]"
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

          <!-- 第二步：选择选股方法 -->
          <el-form-item v-if="stockSelectionMethods && stockSelectionMethods.length > 0" label="选股方式">
            <el-select
              v-model="form.stockSelectionMethod"
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
          <div v-if="form.stockSelectionMethod" class="params-container">
            <div>
              <div class="debug-info" style="margin-bottom: 10px; font-size: 12px; color: #999;">
              </div>
              <el-row :gutter="20">
                <el-col 
                  :span="8" 
                  v-for="(param, index) in getIndicatorParams(form.stockSelectionMethod)" 
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
                        v-model="form.stockSelection.params[form.stockSelectionMethod][param.name]"
                        :placeholder="param.label || param.name"
                        style="width: 100%"
                      />
                    </template>
                    <template v-else-if="param.type === 'boolean'">
                      <el-switch
                        v-model="form.stockSelection.params[form.stockSelectionMethod][param.name]"
                        active-text="是"
                        inactive-text="否"
                      />
                    </template>
                    <template v-else>
                      <el-input
                        v-model="form.stockSelection.params[form.stockSelectionMethod][param.name]"
                        :placeholder="param.label || param.name"
                        style="width: 100%"
                      />
                    </template>
                  </div>
                </el-col>
              </el-row>
              <div v-if="getIndicatorParams(form.stockSelectionMethod).length === 0" class="empty-params">
                该方法无需配置参数
              </div>
            </div>
          </div>
        </div>
        
        <!-- 开仓策略 -->
        <div class="form-section">
          <h3>开仓策略</h3>
          <!-- 第一步：选择开仓策略模板 -->
          <el-form-item label="开仓策略模板" prop="entry.templateId">
            <el-select
              v-model="form.entry.templateId"
              placeholder="请选择开仓策略模板"
              style="width: 100%"
            >
              <el-option
                v-for="item in uniqueOpenPositionTemplates"
                :key="item.id"
                :label="getTemplateName(item)"
                :value="item.id"
              >
                <el-tooltip :content="getTemplateDescription(item)" placement="right">
                  <span>{{ getTemplateName(item) }}</span>
                </el-tooltip>
              </el-option>
            </el-select>
          </el-form-item>
          
          <!-- 显示开仓模板参数 -->
          <div v-if="form.entry.templateId && getTemplateParams(form.entry.templateId, 'entry').length > 0" class="params-container">
            <el-row :gutter="20">
              <el-col 
                :span="8" 
                v-for="(param, index) in getTemplateParams(form.entry.templateId, 'entry')" 
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
                      v-model="form.entry.params[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                  <template v-else-if="param.type === 'boolean'">
                    <el-switch
                      v-model="form.entry.params[param.name]"
                      active-text="是"
                      inactive-text="否"
                    />
                  </template>
                  <template v-else>
                    <el-input
                      v-model="form.entry.params[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                </div>
              </el-col>
            </el-row>
          </div>
          
          <!-- 第二步：选择开仓方法 -->
          <el-form-item v-if="entryMethods && entryMethods.length > 0" label="开仓方式" prop="entryMethod">
            <el-select
              v-model="form.entryMethod"
              placeholder="请选择开仓方式"
              style="width: 100%"
            >
              <el-option
                v-for="method in entryMethods"
                :key="method.className"
                :label="getMethodDisplayName(method)"
                :value="method.funName"
              />
            </el-select>
          </el-form-item>
          
          <!-- 显示开仓方法参数 -->
          <div v-if="form.entryMethod && entryMethods && entryMethods.length > 0 && getIndicatorParams(form.entryMethod).length > 0" class="params-container">
            <el-row :gutter="20">
              <el-col 
                :span="8" 
                v-for="(param, index) in getIndicatorParams(form.entryMethod)" 
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
                      v-model="form.entry.methodParams[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                  <template v-else-if="param.type === 'boolean'">
                    <el-switch
                      v-model="form.entry.methodParams[param.name]"
                      active-text="是"
                      inactive-text="否"
                    />
                  </template>
                  <template v-else>
                    <el-input
                      v-model="form.entry.methodParams[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                </div>
              </el-col>
            </el-row>
            <div v-if="getIndicatorParams(form.entryMethod).length === 0" class="empty-params">
              该方法无需配置参数
            </div>
          </div>
          
          <!-- 自定义公式构造器 -->
          <div v-if="form.entryMode === 'custom'" class="formula-builder-container">
            <el-card shadow="hover" style="height: 100%; min-height: 600px; width: 100%; margin-bottom: 20px;">
              <template #header>
                <div class="card-header">
                  <span>策略公式构建</span>
                  <el-tooltip content="使用公式构建器创建自定义交易策略">
                    <el-icon><question-filled /></el-icon>
                  </el-tooltip>
                </div>
              </template>
              <div class="formula-builder-wrapper" style="min-height: 500px;">
                <formula-builder 
                  :indicators="indicators" 
                  @formula-change="updateFormulaData"
                  @update:formula="(val: string) => { formulaData.formula = val }"
                  :initialData="formulaData"
                  style="width: 100%; height: 100%; min-height: 500px; display: block;"
                />
                
                <div v-if="indicators.length === 0" class="formula-placeholder">
                  <el-empty description="无可用指标" />
                </div>
              </div>
            </el-card>
          </div>
        </div>
        
        <!-- 止盈止损策略 -->
        <div class="form-section">
          <h3>止盈止损策略</h3>
          <el-form-item label="止盈止损模板" prop="stopLoss.templateId">
            <el-select
              v-model="form.stopLoss.templateId"
              placeholder="请选择止盈止损模板"
              style="width: 100%"
            >
              <el-option
                v-for="template in uniqueProfitLossTemplates"
                :key="template.id"
                :label="template.cnClassName"
                :value="template.id"
              />
            </el-select>
          </el-form-item>
          
          <!-- 显示止盈止损模板参数 -->
          <div v-if="form.stopLoss.templateId && getTemplateParams(form.stopLoss.templateId, 'exit').length > 0" class="params-container">
            <el-row :gutter="20">
              <el-col 
                :span="8" 
                v-for="(param, index) in getTemplateParams(form.stopLoss.templateId, 'exit')" 
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
                      v-model="form.stopLoss.params[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                  <template v-else-if="param.type === 'boolean'">
                    <el-switch
                      v-model="form.stopLoss.params[param.name]"
                      active-text="是"
                      inactive-text="否"
                    />
                  </template>
                  <template v-else>
                    <el-input
                      v-model="form.stopLoss.params[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                </div>
              </el-col>
            </el-row>
          </div>
          
          <!-- 第二步：选择止盈止损方法 -->
          <el-form-item v-if="stopLossMethods && stopLossMethods.length > 0" label="止盈止损方式" prop="stopLossMethod">
            <el-select
              v-model="form.stopLossMethod"
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
          
          <!-- 显示止盈止损方法参数 -->
          <div v-if="form.stopLossMethod && stopLossMethods && stopLossMethods.length > 0 && getIndicatorParams(form.stopLossMethod).length > 0" class="params-container">
            <el-row :gutter="20">
              <el-col 
                :span="8" 
                v-for="(param, index) in getIndicatorParams(form.stopLossMethod)" 
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
                      v-model="form.stopLoss.methodParams[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                  <template v-else-if="param.type === 'boolean'">
                    <el-switch
                      v-model="form.stopLoss.methodParams[param.name]"
                      active-text="是"
                      inactive-text="否"
                    />
                  </template>
                  <template v-else>
                    <el-input
                      v-model="form.stopLoss.methodParams[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                </div>
              </el-col>
            </el-row>
            <div v-if="getIndicatorParams(form.stopLossMethod).length === 0" class="empty-params">
              该方法无需配置参数
            </div>
          </div>
        </div>
        
        <!-- 资金策略 -->
        <div class="form-section">
          <h3>资金策略</h3>
          <el-form-item label="资金管理模板" prop="position.templateId">
            <el-select
              v-model="form.position.templateId"
              placeholder="请选择资金管理模板"
              style="width: 100%"
            >
              <el-option
                v-for="template in uniqueFundTemplates"
                :key="template.id"
                :label="template.cnClassName"
                :value="template.id"
              />
            </el-select>
          </el-form-item>
          
          <!-- 显示资金管理模板参数 -->
          <div v-if="form.position.templateId && getTemplateParams(form.position.templateId, 'fund').length > 0" class="params-container">
            <el-row :gutter="20">
              <el-col 
                :span="8" 
                v-for="(param, index) in getTemplateParams(form.position.templateId, 'fund')" 
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
                      v-model="form.position.params[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                  <template v-else-if="param.type === 'boolean'">
                    <el-switch
                      v-model="form.position.params[param.name]"
                      active-text="是"
                      inactive-text="否"
                    />
                  </template>
                  <template v-else>
                    <el-input
                      v-model="form.position.params[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                </div>
              </el-col>
            </el-row>
          </div>
          
          <!-- 资金管理方法选择 -->
          <el-form-item v-if="positionMethods && positionMethods.length > 0" label="资金管理方式" prop="positionMethod">
            <el-select
              v-model="form.positionMethod"
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
          
          <!-- 显示资金管理方法参数 -->
          <div v-if="form.positionMethod && positionMethods && positionMethods.length > 0 && getIndicatorParams(form.positionMethod).length > 0" class="params-container">
            <el-row :gutter="20">
              <el-col 
                :span="8" 
                v-for="(param, index) in getIndicatorParams(form.positionMethod)" 
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
                      v-model="form.position.methodParams[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                  <template v-else-if="param.type === 'boolean'">
                    <el-switch
                      v-model="form.position.methodParams[param.name]"
                      active-text="是"
                      inactive-text="否"
                    />
                  </template>
                  <template v-else>
                    <el-input
                      v-model="form.position.methodParams[param.name]"
                      :placeholder="param.label || param.name"
                      style="width: 100%"
                    />
                  </template>
                </div>
              </el-col>
            </el-row>
            <div v-if="getIndicatorParams(form.positionMethod).length === 0" class="empty-params">
              该方法无需配置参数
            </div>
          </div>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed, unref, defineAsyncComponent } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStrategyStore } from '../stores/strategy'
import { ElMessage } from 'element-plus'
import { InfoFilled, QuestionFilled } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import { QuantAPI, TemplatesAPI } from '../api'
import { Strategy } from '../api/quant'
import { StrategyComponent } from '../api/strategy-components'
import templates from '@/api/templates'

// 异步加载FormulaBuilder组件
const FormulaBuilder = defineAsyncComponent({
  loader: () => import('../components/FormulaBuilder.vue'),
  delay: 200,
  timeout: 30000
})

const router = useRouter()
const route = useRoute()
const strategyStore = useStrategyStore()
const formRef = ref<FormInstance>()
const saving = ref(false)
const loading = ref(false)
const isEdit = ref(false)
const strategyId = ref<number | null>(null)

// 策略分类 - 虽然未直接使用，但为了未来功能扩展保留
// @ts-ignore
const categories = strategyStore.getCategories

// 加载模板数据
const symbolSelectionTemplates = ref<TemplateItem[]>([])
const openPositionTemplates = ref<TemplateItem[]>([])
const profitLossTemplates = ref<TemplateItem[]>([])
const fundTemplates = ref<TemplateItem[]>([])
const indicatorMethods = ref<TargetMethod[]>([])

// 加载模板数据
const loadTemplates = async () => {
  try {
    // 分别加载各个模板
    const symbolSelectionRes = await TemplatesAPI.getSymbolSelectionTemplates()
    const openPositionRes = await TemplatesAPI.getOpenPositionTemplates()
    const profitLossRes = await TemplatesAPI.getProfitLossTemplates()
    const fundRes = await TemplatesAPI.getFundTemplates()
    const indicatorMethodsRes = await TemplatesAPI.getTargetMethods()
    
    // 设置模板数据
    if (symbolSelectionRes?.code === 200) {
      symbolSelectionTemplates.value = symbolSelectionRes.rows || []
    }
    
    if (openPositionRes?.code === 200) {
      openPositionTemplates.value = openPositionRes.rows || []
    }
    
    if (profitLossRes?.code === 200) {
      profitLossTemplates.value = profitLossRes.rows || []
    }
    
    if (fundRes?.code === 200) {
      fundTemplates.value = fundRes.rows || []
    }
    
    if (indicatorMethodsRes?.code === 200) {
      indicatorMethods.value = indicatorMethodsRes.rows || []
    }
    
    // 处理特殊模板
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
    
    // 处理指标方法
    indicatorMethods.value.forEach(method => {
      // 确保函数参数为对象格式
      if (typeof method.parameters === 'string') {
        try {
          method.parameters = JSON.parse(method.parameters)
        } catch (e) {
          console.error('parameters:', e)
          method.parameters = {}
        }
      }
      
      // 确保函数参数描述为对象格式
      if (typeof method.parametersDes === 'string') {
        try {
          method.parametersDes = JSON.parse(method.parametersDes)
        } catch (e) {
          console.error('parametersDes:', e)
          method.parametersDes = {}
        }
      }
    
      
    })
    
    console.log('成功加载模板数据', {
      symbolSelectionTemplates: symbolSelectionTemplates.value.length,
      openPositionTemplates: openPositionTemplates.value.length,
      profitLossTemplates: profitLossTemplates.value.length,
      fundTemplates: fundTemplates.value.length,
      indicatorMethods: indicatorMethods.value.length
    })
  } catch (error) {
    console.error('加载模板数据出错', error)
    ElMessage.error('加载模板数据出错，请刷新页面重试')
  }
}

// 加载指标信息
const indicators = ref<any[]>([])
const loadIndicators = async () => {
  try {
    // 使用API获取指标数据
    console.log('开始从API加载指标数据')
    const indicatorMethodsRes = await TemplatesAPI.getTargetMethods()
    
    if (indicatorMethodsRes?.code === 200 && indicatorMethodsRes.rows.length > 0) {
      // 将API返回的指标方法转换为公式构造器需要的格式
      indicators.value = indicatorMethodsRes.rows
        .filter(method => {
          // 过滤掉基本K线数据指标
          const basicKLineIndicators = ['open', 'high', 'low', 'close', 'volume'];
          return !basicKLineIndicators.includes(method.methodName.toLowerCase());
        })
        .map(method => {
        // 确保parameters是对象
        let parameters: Record<string, any> = {}
        if (typeof method.parameters === 'string') {
          try {
            parameters = JSON.parse(method.parameters)
          } catch (e) {
            console.error('解析parameters失败:', e)
          }
        } else if (method.parameters) {
          parameters = method.parameters
        }
        
        // 确保parametersDes是对象
        let parametersDes: Record<string, any> = {}
        if (typeof method.parametersDes === 'string') {
          try {
            parametersDes = JSON.parse(method.parametersDes)
          } catch (e) {
            console.error('解析parametersDes失败:', e)
          }
        } else if (method.parametersDes) {
          parametersDes = method.parametersDes
        }
        
        // 将parameters和parametersDes转换为公式构造器需要的params格式
        const params: Record<string, any> = {}
        Object.keys(parameters).forEach(key => {
          params[key] = {
            defaultValue: parameters[key],
            description: parametersDes[key] || key
          }
        })
        
        return {
          id: method.id,
          name: method.methodName,
          cnName: method.methodName, // 使用methodName作为中文名
          description: `${method.methodName}指标`,
          params
        }
      })
      
      console.log('成功从API加载指标数据，数量:', indicators.value.length)
    } else {
      console.warn('API未返回有效的指标数据，使用默认数据')
    }
  } catch (error) {
    console.error('加载指标数据出错，使用默认数据', error)

  }
}

// 公式相关状态
const formulaData = ref<FormulaData>({
  formula: '',
  actions: [],
  labels: [],
  bars: []
})

// 定义公式数据类型
interface FormulaData {
  formula: string
  actions: any[]
  labels: any[]
  bars: any[]
  [key: string]: any
}

// 更新公式数据
const updateFormulaData = (data: any) => {
  console.log('CreateStrategy 接收到公式数据:', data);
  
  // 检查收到的数据是否有效
  if (!data) {
    console.warn('接收到的公式数据为空');
    return;
  }

  // 确保所有数组字段都是有效的数组
  const labels = Array.isArray(data.labels) ? data.labels : [];
  const actions = Array.isArray(data.actions) ? data.actions : [];
  const bars = Array.isArray(data.bars) ? data.bars : [];
  
  console.log('处理后的数组数据:', { 
    labelsLength: labels.length, 
    actionsLength: actions.length, 
    barsLength: bars.length 
  });
  
  // 更新 formulaData 值
  formulaData.value = {
    formula: data.formula || '',
    actions: actions,
    labels: labels,
    bars: bars
  };
  
  // 同步到表单中的 customFormula
  if (form.value && form.value.entry) {
    // 初始化 customFormula 对象(如果不存在)
    if (!form.value.entry.customFormula) {
      form.value.entry.customFormula = {
        label: [],
        action: [],
        bar: [],
        args: []
      };
    }
    
    // 将数据从 formulaData 复制到 form.value.entry.customFormula
    // label 数组只保存指标名称
    form.value.entry.customFormula.label = labels.map((label: any) => label.name || label);
    form.value.entry.customFormula.action = [...actions];
    form.value.entry.customFormula.bar = [...bars];
    
    // 处理 args 数组(如果指标参数可用)
    const args: any[] = [];
    
    // 为每个指标创建 args 项，格式为 [{"指标名": {"参数名": "参数值"}}]
    if (labels.length > 0) {
      for (const label of labels) {
        if (typeof label === 'string') {
          // 如果是字符串，查找对应的指标定义
          const indicator = indicators.value.find(ind => ind.name === label);
          
          if (indicator && indicator.params) {
            const argObj: any = {};
            argObj[label] = { ...indicator.params };
            args.push(argObj);
          }
        } else if (label && typeof label === 'object' && 'name' in label && 'params' in label) {
          // 如果是对象，直接使用其名称和参数
          const argObj: any = {};
          argObj[label.name] = { ...label.params };
          args.push(argObj);
        }
      }
    }
    
    // 更新 args 数组
    form.value.entry.customFormula.args = args;
    
    console.log('调整格式后的 customFormula 数据:', JSON.stringify(form.value.entry.customFormula));
  }
}

// 加载默认数据
const loadDefaultData = async () => {
  console.log('加载模板数据')
  try {
    loading.value = true
    // 重新从API加载数据
    await loadTemplates()
    await loadIndicators()
    ElMessage.success('已成功加载模板数据')
  } catch (error) {
    console.error('加载模板数据失败', error)
    ElMessage.error('加载模板数据失败，请重试')
  } finally {
    loading.value = false
  }
}

// 定义开仓条件的类型
interface EntryConditionOption {
  className?: string
  value?: string
  cnClassName?: string
  label?: string
}

// 定义时机选项类型
interface TimingOption {
  value: string
  label: string
}

// 开仓条件选项
const entryConditions = computed<EntryConditionOption[]>(() => {
  const methods = unref(openPositionTemplates); // 使用unref获取真实值
  // 尝试从API获取开仓条件
  if (methods && methods.length > 0) {
    const apiConditions = methods
      .map((method: MethodItem) => ({
        className: method.className,
        cnClassName: method.cnClassName, // 使用methodName作为显示名称
      }))
    
    // 如果API返回了条件，则使用API数据
    if (apiConditions.length > 0) {
      return apiConditions
    }
  }
  
  // 如果API返回为空，则返回空数组
  return []
})

// 定义资金分配选项类型
interface AllocationOption {
  value: string
  label: string
}



// 模板接口
interface TemplateItem {
  id: number;
  fileName?: string;
  name?: string;
  className?: string;
  cnClassName?: string;
  classArgs?: any;
  classArgsDes?: any;
  funName?: string;
  cnFunName?: string;
  funArgs?: any;
  funArgsDes?: any;
}

// 方法接口
interface MethodItem {
  className?: string;
  cnClassName?: string;
  cnFunName?: string;
  funName?: string;
  classArgs?: any;
  classArgsDes?: any;
  funArgs?: any;
  funArgsDes?: any;
}

interface TargetMethod {
  id: number
  methodName: string
  parameters: Record<string, any>
  parametersDes: Record<string, any>
  owner: number
}

// 策略表单接口定义
interface StrategyForm {
  name: string
  description: string
  status: number
  capital: number
  maxPositions: number
  lever: number
  stockSelectionTemplateId: number | null
  stockSelectionMethod: string
  entryMethod: string
  stopLossMethod: string
  positionMethod: string // 新增资金管理方法字段
  
  // 股票池选择
  stockSelection: {
    templateId: number | null
    method: string | null
    params: Record<string, any>
    templateParams: Record<string, any>
  }
  
  // 开仓策略
  entry: {
    templateId: number | null
    params: Record<string, any>
    methodParams: Record<string, any>
    customFormula: any
  }
  
  // 平仓策略
  exit: {
    templateId: number | null
    params: Record<string, any>
  }
  
  // 止盈止损
  stopLoss: {
    templateId: number | null
    percentage: number
    takeProfit: number
    trailingStop: boolean
    trailingDistance: number
    params: Record<string, any> // 新增模板参数
    methodParams: Record<string, any> // 新增方法参数
    method: string // 新增方法字段
  }
  
  // 资金管理
  position: {
    templateId: number | null
    size: number
    maxPositions: number
    allocation: string
    params: Record<string, any> // 新增模板参数
    methodParams: Record<string, any> // 新增方法参数
    method: string // 新增方法字段
  }
  
  // 指标数据
  technicalIndicators: Array<{
    id: string
    name: string
    params: Record<string, any>
  }>
  fundamentalIndicators: Array<{
    id: string
    name: string
    params: Record<string, any>
  }>
  
  // 回测时间范围
  backtestStart: string
  backtestEnd: string
  [key: string]: any // 允许任意附加属性
}

// 定义提交给API的策略数据类型
interface SubmitStrategyData {
  id?: number
  strategyName: string
  remark: string
  maxPosition?: number
  parameters: {
    stockSelection?: number
    entry?: number
    stopLoss?: number
    position?: number
  }
}

// 策略详情接口
interface StrategyDetail {
  id?: number
  strategyName?: string
  capital?: number
  maxPositions?: number
  taskParameters?: {
    symbolSelectionParameters?: {
      templateId?: number
      templateArgs?: Record<string, any>
      methodName?: string
      methodArgs?: Record<string, any>
    }
    technicalIndicators?: Array<{
      indicatorId?: string
      name: string
      args?: Record<string, any>
    }>
    fundamentalIndicators?: Array<{
      indicatorId?: string
      name: string
      args?: Record<string, any>
    }>
  }
  backTestParameters?: {
    startDate?: string
    endDate?: string
    capital?: number
    maxPositions?: number
  }
}

// 获取基本面指标的显示名称
const getFundamentalLabel = (indicator: string): string => {
  if (!indicator) return '未知指标'
  
  // 使用unref安全地获取真实值
  const methods = unref(indicatorMethods);
  
  // 查找匹配的基本面指标
  const fundamentalMethod = methods.find((method: TargetMethod) => 
    method.methodName === indicator)
  
  if (fundamentalMethod) {
    // 优先使用cnClassName，其次使用原始名称
    return fundamentalMethod.methodName
  }
  
  // 如果API中没有找到，直接返回原始名称
  return indicator
}

// 获取基本面指标的显示名称，添加注释避免TypeScript警告
// @ts-ignore
const _getFundamentalLabel = getFundamentalLabel;

// 表单数据
const form = ref<StrategyForm>({
  name: '',
  description: '',
  status: 1, // 默认为运行状态
  capital: 1000000, // 默认本金
  maxPositions: 5, // 默认最大持仓数量
  lever: 50, // 默认杠杆值
  stockSelectionTemplateId: null,
  stockSelectionMethod: '',
  entryMethod: '',
  stopLossMethod: '', // 新增止盈止损方法字段
  positionMethod: '', // 新增资金管理方法字段
  
  // 股票池选择
  stockSelection: {
    templateId: null as number | null,
    method: '',
    params: {} as Record<string, any>,
    templateParams: {} as Record<string, any>
  },
  
  // 开仓策略
  entry: {
    templateId: null as number | null,
    params: {} as Record<string, any>,
    methodParams: {} as Record<string, any>,
    customFormula: null as any
  },
  
  // 平仓策略
  exit: {
    templateId: null as number | null,
    params: {} as Record<string, any>
  },
  
  // 止盈止损
  stopLoss: {
    templateId: null as number | null,
    percentage: 10, // 默认止损比例10%
    takeProfit: 20, // 默认止盈比例20%
    trailingStop: false,
    trailingDistance: 5,
    params: {} as Record<string, any>, // 新增模板参数
    methodParams: {} as Record<string, any>, // 新增方法参数
    method: '' // 新增方法字段
  },
  
  // 资金管理
  position: {
    templateId: null as number | null,
    size: 1000000, // 默认本金
    maxPositions: 5, // 默认最大持仓
    allocation: 'equal',
    params: {} as Record<string, any>, // 新增模板参数
    methodParams: {} as Record<string, any>, // 新增方法参数
    method: '' // 新增方法字段
  },
  
  // 指标数据
  technicalIndicators: [],
  fundamentalIndicators: [],
  
  // 回测时间范围
  backtestStart: '',
  backtestEnd: '',
  
  // 添加entryMode字段以支持表单显示逻辑
  entryMode: 'template'
})

// 交易对列表
const symbols = ref<string[]>([])

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入策略名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  'capital': [
    { required: true, message: '请输入本金', trigger: 'blur' }
  ],
  'maxPositions': [
    { required: true, message: '请输入最大持仓数量', trigger: 'blur' }
  ],
  // 移除选股方法的必选验证规则，使其变为非必选项
  'stockSelectionTemplateId': [
    { required: true, message: '请选择选股模板', trigger: 'change' }
  ],
  'entry.templateId': [
    { required: true, message: '请选择开仓模板', trigger: 'change' }
  ],
  'stopLoss.templateId': [
    { required: true, message: '请选择止损模板', trigger: 'change' }
  ],
  'position.templateId': [
    { required: true, message: '请选择资金管理模板', trigger: 'change' }
  ],
  'positionMethod': [
    { required: true, message: '请选择资金管理方式', trigger: 'change' }
  ]
  // 注意：这里没有entryMethod的验证规则，使其成为非必选项
}

// 调试辅助函数
const logMethodDetails = (method: any, label: string) => {
  if (!method) {
    console.log(`${label}: 未找到方法`);
    return;
  }
  
  console.log(`${label}:`, {
    cnFunName: method.cnFunName,
    funName: method.funName,
    className: method.className,
    cnClassName: method.cnClassName
  });
};

// 修改stockSelectionMethods计算属性，确保保存完整的方法信息
const stockSelectionMethods = computed(() => {
  const selectedTemplateId = form.value.stockSelectionTemplateId;
  
  if (!selectedTemplateId) {
    return []
  }
  
  // 查找当前选中的模板对象
  const selectedTemplate = symbolSelectionTemplates.value.find(t => t.id === selectedTemplateId)
  if (!selectedTemplate) {
    return []
  }
  
  // 找到所有与当前模板类名相同的模板
  const relatedTemplates = symbolSelectionTemplates.value.filter(t => 
  (t.className && t.className === selectedTemplate.className) || 
    (t.cnClassName && t.cnClassName === selectedTemplate.cnClassName)
  );
  
  console.log('相关选股模板数量:', relatedTemplates.length)
  
  // 将这些相关模板转换为选股方法
  const methods = relatedTemplates
    .filter(template => template.funName) // 只保留有funName的模板
    .map(template => ({ 
      className: template.className,
      cnClassName: template.cnClassName,
      funName: template.funName, // 确保保存funName
      cnFunName: template.cnFunName,
      funArgs: template.funArgs,
      funArgsDes: template.funArgsDes,
      classArgs: template.classArgs,
      classArgsDes: template.classArgsDes
    }));
  
  // 调试信息
  methods.forEach(m => logMethodDetails(m, '选股方法'));
  
  return methods
});

// 以下computed属性被定义但未使用，添加注释避免TypeScript警告
// @ts-ignore
const _technicalIndicators = computed<MethodItem[]>(() => {
  const methods = unref(indicatorMethods); // 使用unref获取真实值
  // 尝试从API获取技术指标
  if (methods && methods.length > 0) {
    const apiIndicators = methods
      .map((method: TargetMethod) => ({
        methodName: method.methodName,
        parameters: method.parameters,
        parametersDes: method.parametersDes
      }))
    
    // 如果API返回了指标，则使用API数据
    if (apiIndicators.length > 0) {
      console.log('使用API返回的技术指标:', apiIndicators)
      return apiIndicators
    }
  }
  
  // 如果API返回为空，则返回空数组而不是默认数据
  console.log('API未返回技术指标，显示空')
  return []
})

// 获取模板名称
function getTemplateName(templateId: any): string {
  if (!templateId) {
    return '请选择模板'
  }
  
  // 如果传入的是对象而不是ID
  if (typeof templateId === 'object' && templateId.id) {
    return templateId.cnClassName || templateId.fileName || templateId.name || templateId.className || '未命名模板'
  }
  
  // 使用ID查找模板
  const templates = unref(symbolSelectionTemplates)
  const template = templates.find((t: any) => t.id === templateId)
  
  return template ? (template.cnClassName || template.fileName || template.name || template.className || '未命名模板') : '请选择有效模板'
}

// 参数接口定义
interface IndicatorParameter {
  name: string
  label: string
  description: string
  type: string
  defaultValue: any
}

// 获取股票选择模板的参数
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
    templates = unref(openPositionTemplates)
  } else if (type === 'stock') {
    templates = unref(symbolSelectionTemplates)
  } else if (type === 'exit') {
    templates = unref(profitLossTemplates)
  } else if (type === 'fund') {
    templates = unref(fundTemplates)
  } else {
    templates = unref(symbolSelectionTemplates) // 默认使用选股模板
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

// 获取指标方法的参数
function getIndicatorParams(className: string): IndicatorParameter[] {
  console.log('getIndicatorParams 被调用，参数:', className)
  
  if (!className) {
    console.log('方法名为空，返回空数组')
    return []
  }
  
  // 1. 首先尝试从选股方法中查找
  if (form.value.stockSelectionTemplateId) {
    console.log('尝试从选股方法中查找:', className)
    const selectionMethods = unref(stockSelectionMethods.value);
    
    // 查找匹配的选股方法
    const stockMethod = selectionMethods.find((m: MethodItem) => 
      m.funName === className 
    )
    
    if (stockMethod) {
      console.log('在选股方法中找到:', stockMethod)
      return extractMethodParams(stockMethod);
    } else {
      console.log('在选股方法中未找到:', className)
    }
  }
  
  // 2. 如果不是选股方法，尝试从开仓方法中查找
  if (form.value.entry.templateId) {
    console.log('尝试从开仓方法中查找:', className)
    const entryMethodsList = unref(entryMethods.value);
    
    // 查找匹配的开仓方法
    const entryMethod = entryMethodsList.find((m: MethodItem) => 
      m.funName === className
    )
    
    if (entryMethod) {
      console.log('在开仓方法中找到:', entryMethod)
      return extractMethodParams(entryMethod);
    } else {
      console.log('在开仓方法中未找到:', className)
    }
  }
  
  // 3. 如果不是开仓方法，尝试从止盈止损方法中查找
  if (form.value.stopLoss.templateId) {
    console.log('尝试从止盈止损方法中查找:', className)
    const stopLossMethodsList = unref(stopLossMethods.value);
    
    // 查找匹配的止盈止损方法
    const stopLossMethod = stopLossMethodsList.find((m: MethodItem) => 
      m.funName === className
    )
    
    if (stopLossMethod) {
      console.log('在止盈止损方法中找到:', stopLossMethod)
      return extractMethodParams(stopLossMethod);
    } else {
      console.log('在止盈止损方法中未找到:', className)
    }
  }
  
  // 4. 如果不是止盈止损方法，尝试从资金管理方法中查找
  if (form.value.position.templateId) {
    console.log('尝试从资金管理方法中查找:', className)
    const positionMethodsList = unref(positionMethods.value);
    
    // 查找匹配的资金管理方法
    const positionMethod = positionMethodsList.find((m: MethodItem) => 
      m.funName === className
    )
    
    if (positionMethod) {
      console.log('在资金管理方法中找到:', positionMethod)
      return extractMethodParams(positionMethod);
    } else {
      console.log('在资金管理方法中未找到:', className)
    }
  }
  
  // 如果在所有方法中都未找到，返回空数组
  console.log('在所有方法中均未找到参数，返回空数组')
  return []
}

// 从方法对象中提取参数
function extractMethodParams(method: MethodItem): IndicatorParameter[] {
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

// 获取方法显示名称（按优先级：中文名称 > 方法名称 > 类名称）
function getMethodDisplayName(method: MethodItem): string {
  if (!method) return '未知方法'
  
  console.log('获取方法显示名称:', method)
  
  // 优先使用cnFunName作为显示
  if (method.cnFunName) return method.cnFunName


  return "无需选择"
}

// 获取模板描述
const getTemplateDescription = (template: any) => {
  if (!template) return ''
  return template.description || template.fileName || template.name || '未知模板'
}

// 获取方法名称（显示中文名称）
const getMethodName = (className: string): string => {
  if (!className) return '未找到方法'
  
  // 使用unref安全地获取真实值
  const methods = unref(symbolSelectionTemplates);
  
  const method = methods.find((m: MethodItem) => m.className === className)
  if (!method) return ""
  
  // 优先使用cnFunName，其次是funName
  return method.cnFunName || ""
}

// 获取方法描述
const getMethodDescription = (className: string): string => {
  if (!className) return ''
  
  // 使用unref安全地获取真实值
  const methods = unref(symbolSelectionTemplates);
  
  const method = methods.find((m: MethodItem) => m.className === className)
  if (!method) return ""
  
  // 构建一个更详细的描述，使用中文名称
  const classNameText = method.cnClassName
  const funNameText = method.cnFunName
  
  return `${classNameText} - ${funNameText}`
}

// 监听选股模板ID变化
watch(() => form.value.stockSelectionTemplateId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    // 清空旧的模板参数
    form.value.stockSelection.templateParams = {}
    form.value.stockSelectionMethod = ''
    form.value.stockSelection.method = ''
    form.value.stockSelection.params = {}
    
    // 获取新模板的参数，并设置默认值
    const params = getTemplateParams(newVal)
    if (params.length > 0) {
      params.forEach(param => {
        // 只有当参数有默认值时才设置
        if (param.defaultValue !== undefined && param.defaultValue !== null && param.defaultValue !== '') {
          form.value.stockSelection.templateParams[param.name] = param.defaultValue
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
            form.value.stockSelectionMethod = selectedTemplate.funName
            form.value.stockSelection.method = selectedTemplate.funName
          } else {
            // 默认选择第一个方法
            const firstMethod = methods[0]
            if (firstMethod && firstMethod.funName) {
              console.log('默认选择方法:', firstMethod.funName)
              form.value.stockSelectionMethod = firstMethod.funName
              form.value.stockSelection.method = firstMethod.funName
            }
          }
          
          // 获取选择的方法参数
          if (form.value.stockSelectionMethod) {
            // 初始化方法参数对象
            form.value.stockSelection.params = {}
            
            // 获取参数列表
            const methodParams = getIndicatorParams(form.value.stockSelectionMethod)
            
            // 使用默认值初始化
            if (methodParams.length > 0) {
              if (!form.value.stockSelection.params[form.value.stockSelectionMethod]) {
                form.value.stockSelection.params[form.value.stockSelectionMethod] = {}
              }
              
              methodParams.forEach(param => {
                if (param.name && param.defaultValue !== undefined) {
                  form.value.stockSelection.params[form.value.stockSelectionMethod][param.name] = param.defaultValue
                }
              })
            }
          }
        }
      }
    }
  }
}, { immediate: true })

// 确保form.stockSelection.params初始化，防止访问错误
watch(() => form.value.stockSelectionMethod, (newVal) => {
  // 确保不会将 undefined 或 null 赋值给非 null 类型
  form.value.stockSelection.method = newVal || '';
  
  // 只在有选股方法时初始化参数
  if (newVal) {
    // 检查对应方法的参数是否已初始化
    if (!form.value.stockSelection.params[newVal]) {
      // 初始化方法参数对象
      form.value.stockSelection.params[newVal] = {};
      
      // 获取参数列表
      const params = getIndicatorParams(newVal);
      
      // 使用默认值初始化
      params.forEach(param => {
        if (param.name && param.defaultValue !== undefined) {
          form.value.stockSelection.params[newVal][param.name] = param.defaultValue;
        }
      });
    }
  }
}, { immediate: true })

// 反向监听，确保双向同步
watch(() => form.value.stockSelection.templateId, (newVal) => {
  form.value.stockSelectionTemplateId = newVal
}, { immediate: true })

watch(() => form.value.stockSelection.method, (newVal) => {
  // 确保不会将 null 赋值给不允许 null 的类型
  form.value.stockSelectionMethod = newVal || ''
}, { immediate: true })

// 扩展StrategyComponent接口，添加前端需要的额外属性 - 虽然未直接使用，但为了类型定义保留
// @ts-ignore
interface ExtendedComponent extends StrategyComponent {
  args?: {
    conditions?: any[]
    timing?: string
    percentage?: number
    takeProfit?: number
    trailingStop?: boolean
    trailingDistance?: number
    size?: number
    maxPositions?: number
    allocation?: string
    [key: string]: any
  }
}

// 扩展Strategy接口，添加前端需要的额外属性 - 虽然未直接使用，但为了类型定义保留
// @ts-ignore
interface ExtendedStrategy extends Strategy {
  name?: string
  category?: string
  description?: string
  parameters?: {
    stockSelection?: number
    entry?: number
    stopLoss?: number
    position?: number
  }
}

// 加载策略数据
const loadStrategy = async (id: string) => {
  try {
    console.log('加载策略详情:', id)
    const response = await QuantAPI.getStrategyDetail(parseInt(id))
    const strategy = response.data
    
    if (strategy && strategy.id) {
      console.log('策略详情数据:', strategy)
      
      // 设置基本信息，只使用策略中已有的值，不提供默认值
      if (strategy.strategyName) {
        form.value.name = strategy.strategyName
      }
      
      // 获取策略额外数据
      let extraData = {}
      try {
        if (strategy.remark) {
          extraData = JSON.parse(strategy.remark)
          console.log('解析到额外数据:', extraData)
        }
      } catch (error) {
        console.error('解析策略额外数据失败:', error)
      }
      
      // 如果有extraData中包含stockSelectionTemplateId，则使用它
      // @ts-ignore
      if (extraData.stockSelectionTemplateId) {
        // @ts-ignore
        form.value.stockSelectionTemplateId = extraData.stockSelectionTemplateId
        // @ts-ignore
        form.value.stockSelection.templateId = extraData.stockSelectionTemplateId
        
        // @ts-ignore
        console.log('设置选股模板ID:', extraData.stockSelectionTemplateId)
        
        // @ts-ignore
        if (extraData.stockSelectionParams) {
          // @ts-ignore
          form.value.stockSelection.templateParams = extraData.stockSelectionParams
          
          // 处理固定交易对模板
          const selectedTemplate = symbolSelectionTemplates.value.find(t => t.id === form.value.stockSelectionTemplateId)
          if (selectedTemplate && selectedTemplate.cnClassName === '固定交易对') {
            // @ts-ignore
            if (extraData.stockSelectionParams.symbols && Array.isArray(extraData.stockSelectionParams.symbols)) {
              // @ts-ignore
              symbols.value = extraData.stockSelectionParams.symbols
            } else {
              symbols.value = [] // 确保至少有一个空数组
            }
          }
        }
        
        // @ts-ignore
        if (extraData.stockSelectionMethod) {
          // @ts-ignore
          form.value.stockSelectionMethod = extraData.stockSelectionMethod
          // @ts-ignore
          form.value.stockSelection.method = extraData.stockSelectionMethod
        }
        
        // @ts-ignore
        if (extraData.stockSelectionMethodParams) {
          // 确保params对象存在
          if (!form.value.stockSelection.params) {
            form.value.stockSelection.params = {}
          }
          
          // 初始化方法参数对象
          // @ts-ignore
          if (extraData.stockSelectionMethod) {
            // @ts-ignore
            const methodName = extraData.stockSelectionMethod
            
            if (!form.value.stockSelection.params[methodName]) {
              form.value.stockSelection.params[methodName] = {}
            }
            
            // @ts-ignore
            form.value.stockSelection.params[methodName] = extraData.stockSelectionMethodParams
          }
        }
      }
    }
    
    loading.value = false
  } catch (error) {
    console.error('加载策略数据失败:', error)
    ElMessage.error('加载策略数据失败')
    loading.value = false
  }
}

// 将中文方法名转换为英文函数名的辅助函数
const getCnFunNameToFunName = (cnFunName: string, methodList: MethodItem[]): string => {
  if (!cnFunName || !methodList || methodList.length === 0) return cnFunName;
  
  // 在方法列表中查找匹配的中文方法名
  const method = methodList.find(m => m.cnFunName === cnFunName);
  if (method && method.funName) {
    console.log(`转换方法名: ${cnFunName} -> ${method.funName}`);
    return method.funName;
  }
  
  // 如果没找到，返回原始名称
  return cnFunName;
}

// 确定参数类型的辅助函数
function detectParamType(name: string, value: any): string {
  // 如果值是布尔类型
  if (typeof value === 'boolean') {
    return 'boolean'
  }
  
  // 如果值是数字类型
  if (typeof value === 'number') {
    return 'number'
  }
  
  // 通过名称推断类型
  const nameLC = name.toLowerCase()
  if (
    nameLC.includes('is') || 
    nameLC.includes('has') || 
    nameLC.includes('enable') || 
    nameLC.includes('use') ||
    nameLC.includes('flag')
  ) {
    return 'boolean'
  }
  
  if (
    nameLC.includes('period') || 
    nameLC.includes('days') || 
    nameLC.includes('count') || 
    nameLC.includes('size') || 
    nameLC.includes('length') ||
    nameLC.includes('threshold') || 
    nameLC.includes('ratio') || 
    nameLC.includes('rate') || 
    nameLC.includes('value') || 
    nameLC.includes('limit') || 
    nameLC.includes('max') || 
    nameLC.includes('min')
  ) {
    return 'number'
  }
  
  // 默认为字符串
  return 'string'
}

// 将参数转换为正确的数据类型
function convertParamsToCorrectType(params: Record<string, any>): Record<string, any> {
  if (!params || typeof params !== 'object') return params
  
  const result: Record<string, any> = {}
  
  for (const key in params) {
    const value = params[key]
    const paramType = detectParamType(key, value)
    
    if (paramType === 'number' && typeof value === 'string') {
      // 将字符串转换为数字
      const numberValue = parseFloat(value)
      result[key] = isNaN(numberValue) ? value : numberValue
    } else if (paramType === 'boolean' && typeof value === 'string') {
      // 将字符串转换为布尔值
      result[key] = value.toLowerCase() === 'true'
    } else {
      result[key] = value
    }
  }
  
  return result
}

// 处理提交表单数据
const prepareSubmitData = (): SubmitStrategyData => {
  // 辅助函数：将字符串形式的数字参数转换为数字类型
  const convertParamsToCorrectType = (params: Record<string, any>): Record<string, any> => {
    if (!params || typeof params !== 'object') return params;
    
    const result: Record<string, any> = {};
    
    for (const key in params) {
      const value = params[key];
      
      // 检查是否为数字字符串
      if (typeof value === 'string' && !isNaN(Number(value))) {
        // 尝试转换为数字
        result[key] = parseFloat(value);
      } else if (typeof value === 'string' && (value.toLowerCase() === 'true' || value.toLowerCase() === 'false')) {
        // 转换布尔值
        result[key] = value.toLowerCase() === 'true';
      } else {
        // 保持原值
        result[key] = value;
      }
    }
    
    return result;
  };

  // 准备各个模板ID
  const stockSelectionId = form.value.stockSelectionTemplateId === null ? undefined : form.value.stockSelectionTemplateId;
  const entryId = form.value.entry.templateId === null ? undefined : form.value.entry.templateId;
  const stopLossId = form.value.stopLoss.templateId === null ? undefined : form.value.stopLoss.templateId;
  const positionId = form.value.position.templateId === null ? undefined : form.value.position.templateId;
  
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
  const stockSelectionFunName = convertMethodName(form.value.stockSelectionMethod, stockSelectionMethods.value);
  const entryFunName = convertMethodName(form.value.entryMethod, entryMethods.value);
  const stopLossFunName = convertMethodName(form.value.stopLossMethod, stopLossMethods.value);
  const positionFunName = convertMethodName(form.value.positionMethod, positionMethods.value);
  
  // 转换参数类型
  const convertedStockSelectionParams = convertParamsToCorrectType(form.value.stockSelection.templateParams);
  const convertedStockSelectionMethodParams = form.value.stockSelectionMethod 
    ? convertParamsToCorrectType(form.value.stockSelection.params[form.value.stockSelectionMethod]) 
    : {};
  const convertedEntryParams = convertParamsToCorrectType(form.value.entry.params);
  const convertedEntryMethodParams = convertParamsToCorrectType(form.value.entry.methodParams);
  const convertedStopLossParams = convertParamsToCorrectType(form.value.stopLoss.params);
  const convertedStopLossMethodParams = convertParamsToCorrectType(form.value.stopLoss.methodParams);
  const convertedPositionParams = convertParamsToCorrectType(form.value.position.params);
  const convertedPositionMethodParams = convertParamsToCorrectType(form.value.position.methodParams);
  
  // 将额外数据保存到remark中
  const extraData: any = {
    capital: form.value.position.size, // 确保使用position.size作为本金
    maxPositions: form.value.position.maxPositions, // 确保使用position.maxPositions作为最大持仓数量
    lever: form.value.lever.toString(), // 添加杠杆值，转换为字符串
    
    // 保存选股策略信息
    stockSelectionTemplateId: form.value.stockSelectionTemplateId,
    stockSelectionMethod: stockSelectionFunName, // 使用转换后的方法名
    stockSelectionParams: convertedStockSelectionParams,
    stockSelectionMethodParams: convertedStockSelectionMethodParams,
    
    // 保存开仓策略信息
    entryTemplateId: form.value.entry.templateId,
    entryMethod: entryFunName, // 使用转换后的方法名
    entryParams: convertedEntryParams,
    entryMethodParams: convertedEntryMethodParams,
    
    // 保存止盈止损策略信息
    stopLossTemplateId: form.value.stopLoss.templateId,
    stopLossMethod: stopLossFunName, // 使用转换后的方法名
    stopLossParams: convertedStopLossParams,
    stopLossMethodParams: convertedStopLossMethodParams,
    
    // 保存资金管理策略信息
    positionTemplateId: form.value.position.templateId,
    positionMethod: positionFunName, // 使用转换后的方法名
    positionParams: convertedPositionParams,
    positionMethodParams: convertedPositionMethodParams
  }
  
  // 如果是固定交易对模板，把交易对数组放入templateParams
  if (isFixedSymbolTemplate.value && symbols.value.length > 0) {
    extraData.stockSelectionParams = {
      ...convertedStockSelectionParams,
      symbols: symbols.value.filter(s => s.trim() !== '') // 过滤掉空白交易对
    }
  }
  
  // 如果是自定义模板模式，将公式数据添加到extraData中
  if (form.value.entryMode === 'custom' && form.value.entry.customFormula) {
    console.log('准备添加自定义公式数据:', form.value.entry.customFormula);
    
    // 获取公式数据 - 已经是后端期望的格式 (单数形式字段名)
    const customFormula = form.value.entry.customFormula;
  
    // 直接使用现有数据，确保存在且是数组
    const customFormulaData: any = {
      label: Array.isArray(customFormula.label) ? customFormula.label : [],
      action: Array.isArray(customFormula.action) ? customFormula.action : [],
      bar: Array.isArray(customFormula.bar) ? customFormula.bar : [],
      args: Array.isArray(customFormula.args) ? customFormula.args : []
    };
    
    // 输出调试信息
    console.log('要提交的公式数据:', {
      labelCount: customFormulaData.label.length,
      actionCount: customFormulaData.action.length,
      barCount: customFormulaData.bar.length,
      argsCount: customFormulaData.args.length
    });
    
    console.log('检查数组类型:', {
      labelIsArray: Array.isArray(customFormulaData.label),
      actionIsArray: Array.isArray(customFormulaData.action),
      barIsArray: Array.isArray(customFormulaData.bar),
      argsIsArray: Array.isArray(customFormulaData.args)
    });
    
    // 确保 args 数组中包含了所有指标的参数
    // 从外部组件级别的 formulaData 变量获取指标参数
    if (formulaData.value && formulaData.value.labels && formulaData.value.labels.length > 0) {
      // 确保 args 是数组
      if (!Array.isArray(customFormulaData.args)) {
        customFormulaData.args = [];
      }
      
      // 使用 formulaData 中的 labels 数据
      formulaData.value.labels.forEach((label: any) => {
        if (label && label.params) {
          // 创建正确的参数对象格式：{"指标名": {"参数名": "参数值"}}
          const argObj: any = {};
          const convertedParams = convertParamsToCorrectType(label.params);
          argObj[label.name] = convertedParams;
          
          // 检查 args 数组中是否已经存在相同指标的参数
          const existingArgIndex = customFormulaData.args.findIndex(
            (arg: any) => arg && typeof arg === 'object' && Object.keys(arg)[0] === label.name
          );
          
          if (existingArgIndex === -1) {
            // 不存在则添加新的
            customFormulaData.args.push(argObj);
          } else {
            // 已存在则更新
            customFormulaData.args[existingArgIndex] = argObj;
          }
        }
      });
    } else {
      console.warn('警告：formulaData.value 不可用或无 labels 数据，无法提取指标参数信息。');
    }
    
    console.log('最终传递的自定义公式数据:', customFormulaData);
    
    // 将公式数据添加到extraData
    extraData.customFormula = customFormulaData;
  }
  
  // 创建并返回策略数据
  const strategyData: SubmitStrategyData = {
    ...(isEdit.value && strategyId.value ? { id: strategyId.value } : {}),
    strategyName: form.value.name || '',
    remark: JSON.stringify(extraData),
    parameters: {
      stockSelection: stockSelectionId,
      entry: entryId,
      stopLoss: stopLossId,
      position: positionId
    }
  };
  
  return strategyData;
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      saving.value = true
      try {
        // 如果是自定义模板模式，确保自定义公式数据存在
        if (form.value.entryMode === 'custom') {
          console.log('提交前检查自定义公式数据...', form.value.entry.customFormula);
          
          // 直接检查现有的自定义公式数据是否为空
          const isEmpty = 
            !form.value.entry.customFormula || 
            ((!form.value.entry.customFormula.label || form.value.entry.customFormula.label.length === 0) &&
            (!form.value.entry.customFormula.action || form.value.entry.customFormula.action.length === 0) &&
            (!form.value.entry.customFormula.bar || form.value.entry.customFormula.bar.length === 0));
          
          if (isEmpty) {
            console.log('自定义公式数据为空，尝试从 formulaData.value 同步数据...');
            
            // 初始化 customFormula 如果不存在
            if (!form.value.entry.customFormula) {
              form.value.entry.customFormula = {
                label: [],
                action: [],
                bar: [],
                args: []
              };
            }
            
            // 从 formulaData 中同步数据
            if (formulaData.value && formulaData.value.labels && formulaData.value.labels.length > 0) {
              form.value.entry.customFormula.label = formulaData.value.labels.map(label => label.name);
            }
            
            if (formulaData.value && formulaData.value.actions && formulaData.value.actions.length > 0) {
              form.value.entry.customFormula.action = formulaData.value.actions;
            }
            
            if (formulaData.value && formulaData.value.bars && formulaData.value.bars.length > 0) {
              form.value.entry.customFormula.bar = formulaData.value.bars;
            }
            
            // 处理参数
            if (formulaData.value && formulaData.value.labels && formulaData.value.labels.length > 0) {
              const args: any[] = [];
              
              formulaData.value.labels.forEach(label => {
                if (label && label.params) {
                  // 创建正确的参数对象格式：{"指标名": {"参数名": "参数值"}}
                  const argObj: any = {};
                  argObj[label.name] = { ...label.params };
                  args.push(argObj);
                }
              });
              
              form.value.entry.customFormula.args = args;
            }
            
            console.log('同步后的自定义公式数据:', form.value.entry.customFormula);
            
            // 再次检查数据是否仍然为空 - 使用AND关系而不是OR关系
            const stillEmpty = 
              (!form.value.entry.customFormula.label || form.value.entry.customFormula.label.length === 0) &&
              (!form.value.entry.customFormula.action || form.value.entry.customFormula.action.length === 0) &&
              (!form.value.entry.customFormula.bar || form.value.entry.customFormula.bar.length === 0);
            
            // 如果仍然为空，显示警告并终止提交
            if (stillEmpty) {
              console.warn('同步后公式数据仍然为空！无法保存策略。');
              ElMessage.error('公式数据为空，请先使用公式构建器构建交易公式，再提交策略。');
              saving.value = false;
              return; // 终止提交
            } else {
              console.log('同步后的公式数据有效，继续提交...');
              console.log('同步后的完整公式数据:', JSON.stringify(form.value.entry.customFormula));
            }
          } else {
            console.log('自定义公式数据已有效，继续提交...');
            console.log('现有完整公式数据:', JSON.stringify(form.value.entry.customFormula));
          }
        } else {
          console.log('自定义公式数据验证通过，继续提交...');
          console.log('自定义公式完整数据:', JSON.stringify(form.value.entry.customFormula));
        }
        
        // 在提交前转换参数数据类型
        convertAllParamsTypes();
        
        // 准备策略数据
        const strategyData = prepareSubmitData()
        
        // 调试输出 - 检查自定义公式数据
        if (form.value.entryMode === 'custom') {
          console.log('提交表单前的自定义公式数据:', form.value.entry.customFormula);
          
          // 解析remark中的customFormula数据来检查
          try {
            const remarkData = JSON.parse(strategyData.remark);
            console.log('要发送到后端的公式数据:', remarkData.customFormula);
            console.log('要发送到后端的完整remark数据:', remarkData);
            
            // 特别检查label、action、bar和args数组
            console.log('自定义公式的label数组:', remarkData.customFormula.label);
            console.log('自定义公式的action数组:', remarkData.customFormula.action);
            console.log('自定义公式的bar数组:', remarkData.customFormula.bar);
            console.log('自定义公式的args数组:', remarkData.customFormula.args);
          } catch (e) {
            console.error('解析remark数据失败:', e);
          }
        }
        
        if (isEdit.value && strategyId.value) {
          // 更新策略
          await QuantAPI.updateStrategy(strategyData)
          ElMessage.success('策略更新成功')
        } else {
          // 创建新策略
          await QuantAPI.addStrategy(strategyData)
          ElMessage.success('策略创建成功')
        }
        
        router.push('/user')
      } catch (error) {
        console.error('保存策略失败', error)
        ElMessage.error('保存策略失败，请重试')
      } finally {
        saving.value = false
      }
    }
  })
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
  convertObjectParams(form.value.stockSelection.templateParams);
  
  // 转换选股方法参数
  if (form.value.stockSelectionMethod && form.value.stockSelection.params[form.value.stockSelectionMethod]) {
    convertObjectParams(form.value.stockSelection.params[form.value.stockSelectionMethod]);
  }
  
  // 转换开仓参数
  convertObjectParams(form.value.entry.params);
  convertObjectParams(form.value.entry.methodParams);
  
  // 转换止盈止损参数
  convertObjectParams(form.value.stopLoss.params);
  convertObjectParams(form.value.stopLoss.methodParams);
  
  // 转换资金管理参数
  convertObjectParams(form.value.position.params);
  convertObjectParams(form.value.position.methodParams);
  
  // 转换自定义公式参数（如果存在）
  if (form.value.entry.customFormula && form.value.entry.customFormula.args) {
    // 遍历args数组
    form.value.entry.customFormula.args.forEach((argObj: any) => {
      if (argObj && typeof argObj === 'object') {
        const indicatorName = Object.keys(argObj)[0];
        if (indicatorName && argObj[indicatorName]) {
          convertObjectParams(argObj[indicatorName]);
        }
      }
    });
  }
  
  console.log('参数类型转换完成');
}

// 初始化
onMounted(async () => {
  loading.value = true
  try {
    await loadTemplates()
    await loadIndicators()
    
    // 初始化表单
    initForm()
    
    // 如果是编辑模式，加载策略数据
    const id = route.query.id
    if (id) {
      isEdit.value = true
      strategyId.value = parseInt(id as string)
      await loadStrategy(strategyId.value.toString())
    }
    
    // 检查是否需要初始化公式数据
    if (form.value.entryMode === 'custom') {
      console.log('页面加载时初始化公式数据');
    }
  } catch (error) {
    console.error('初始化数据失败', error)
    ElMessage.error('初始化数据失败，请刷新页面重试')
  } finally {
    loading.value = false
  }
})

// 从现有策略初始化表单 - 虽然未直接调用，但保留以供后续功能使用
// @ts-ignore
const initFromStrategy = (strategy: StrategyDetail) => {
  if (!strategy) return
  
  // 设置基本信息，只使用策略中已有的值，不提供默认值
  if (strategy.strategyName) {
    form.value.name = strategy.strategyName
  }
  
  if (strategy.capital) {
    form.value.capital = strategy.capital
  }
  
  if (strategy.maxPositions) {
    form.value.maxPositions = strategy.maxPositions
  }
  
  // 设置股票选择
  if (strategy.taskParameters && strategy.taskParameters.symbolSelectionParameters) {
    const stockSelection = strategy.taskParameters.symbolSelectionParameters
    
    // 设置选股模板
    if (stockSelection.templateId) {
      form.value.stockSelectionTemplateId = stockSelection.templateId
      form.value.stockSelection.templateId = stockSelection.templateId
      
      // 加载模板参数
      if (stockSelection.templateArgs) {
        form.value.stockSelection.templateParams = stockSelection.templateArgs
      }
    }
    
    // 设置选股方法
    if (stockSelection.methodName) {
      form.value.stockSelectionMethod = stockSelection.methodName
      form.value.stockSelection.method = stockSelection.methodName
      
      // 加载方法参数
      if (stockSelection.methodArgs) {
        form.value.stockSelection.params[stockSelection.methodName] = stockSelection.methodArgs
      }
    }
  }
  
  // 设置技术指标
  if (strategy.taskParameters && strategy.taskParameters.technicalIndicators) {
    const indicators = strategy.taskParameters.technicalIndicators
    form.value.technicalIndicators = indicators.map(indicator => {
      return {
        id: indicator.indicatorId || indicator.name,
        name: indicator.name,
        params: indicator.args || {}
      }
    })
  }
  
  // 设置基本面指标
  if (strategy.taskParameters && strategy.taskParameters.fundamentalIndicators) {
    const indicators = strategy.taskParameters.fundamentalIndicators
    form.value.fundamentalIndicators = indicators.map(indicator => {
      return {
        id: indicator.indicatorId || indicator.name,
        name: indicator.name,
        params: indicator.args || {}
      }
    })
  }
  
  // 设置回测配置
  if (strategy.backTestParameters) {
    const backtest = strategy.backTestParameters
    
    if (backtest.startDate) {
      form.value.backtestStart = backtest.startDate
    }
    
    if (backtest.endDate) {
      form.value.backtestEnd = backtest.endDate
    }
    
    // 加载其他回测参数
    if (backtest.capital) {
      form.value.capital = backtest.capital
    }
    
    if (backtest.maxPositions) {
      form.value.maxPositions = backtest.maxPositions
    }
  }
}

// 获取开仓策略参数
const getEntryParams = (templateId: number | null) => {
  if (!templateId) return []
  
  const template = unref(openPositionTemplates).find(t => t.id === templateId)
  if (!template) return []
  
  // 如果是自定义策略，不显示参数配置
  if (template.cnClassName === '自定义') return []
  
  // 从模板中获取参数
  let params: any[] = []
  
  if (template.classArgsDes && typeof template.classArgsDes === 'object') {
    params = Object.keys(template.classArgsDes).map(key => {
      return {
        name: key,
        description: template.classArgsDes[key],
        defaultValue: template.classArgs?.[key] || ''
      }
    })
  }
  
  // 确保表单中有params对象
  if (!form.value.entry.params) {
    form.value.entry.params = {}
  }
  
  // 设置默认值
  params.forEach(param => {
    if (form.value.entry.params[param.name] === undefined) {
      form.value.entry.params[param.name] = param.defaultValue
    }
  })
  
  return params
}

// 初始化开仓策略表单
const initEntryForm = () => {
  if (!form.value.entry) {
    form.value.entry = {
      templateId: null,
      params: {},
      methodParams: {},
      customFormula: null
    }
  }
}

// 初始化表单
const initForm = () => {
  // 初始化各个部分
  initEntryForm()
  
  // 确保其他表单部分也初始化
  if (!form.value.stockSelection) {
    form.value.stockSelection = {
      templateId: null,
      method: '',
      params: {},
      templateParams: {}
    }
  } else {
    // 确保method为空字符串而不是null
    form.value.stockSelection.method = form.value.stockSelection.method || ''
  }
  
  // 确保stockSelectionMethod为空字符串
  form.value.stockSelectionMethod = form.value.stockSelectionMethod || ''
  
  if (!form.value.exit) {
    form.value.exit = {
      templateId: null,
      params: {}
    }
  }
  
  if (!form.value.stopLoss) {
    form.value.stopLoss = {
      templateId: null,
      percentage: 10,
      takeProfit: 20,
      trailingStop: false,
      trailingDistance: 5,
      params: {},
      methodParams: {},
      method: ''
    }
  }
  
  // 确保stopLossMethod为空字符串
  form.value.stopLossMethod = form.value.stopLossMethod || ''
  
  if (!form.value.position) {
    form.value.position = {
      templateId: null,
      size: form.value.capital || 1000000, // 使用表单本金值或默认值初始化position.size
      maxPositions: form.value.maxPositions || 5, // 使用表单最大持仓数量或默认值初始化position.maxPositions
      allocation: 'equal',
      params: {},
      methodParams: {},
      method: ''
    }
  } else {
    // 确保position中的字段初始化
    form.value.position.params = form.value.position.params || {}
    form.value.position.methodParams = form.value.position.methodParams || {}
    form.value.position.method = form.value.position.method || ''
    // 确保position.size和position.maxPositions与表单值一致
    form.value.position.size = form.value.capital || form.value.position.size || 1000000
    form.value.position.maxPositions = form.value.maxPositions || form.value.position.maxPositions || 5
  }
  
  // 确保positionMethod为空字符串
  form.value.positionMethod = form.value.positionMethod || ''
  
  if (!form.value.fund) {
    form.value.fund = {
      templateId: null,
      params: {}
    }
  }
}

// 过滤出唯一的选股模板（按描述或类名去重）
const uniqueSymbolSelectionTemplates = computed(() => {
  // 用于跟踪已处理的模板描述
  const processedDescriptions = new Set();
  const processedClassNames = new Set();
  
  // 筛选结果数组
  const uniqueTemplates: TemplateItem[] = [];
  
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

// 过滤出唯一的开仓策略模板（按描述或类名去重）
const uniqueOpenPositionTemplates = computed(() => {
  // 用于跟踪已处理的模板描述
  const processedDescriptions = new Set();
  const processedClassNames = new Set();
  
  // 筛选结果数组
  const uniqueTemplates: TemplateItem[] = [];
  
  // 遍历所有模板
  openPositionTemplates.value.forEach(template => {
    // 优先使用描述作为唯一键
    if (template.className && !processedDescriptions.has(template.className)) {
      processedDescriptions.add(template.className);
      uniqueTemplates.push(template);
    }
  });
  
  return uniqueTemplates;
});

// 过滤出唯一的止盈止损策略模板（按描述或类名去重）
const uniqueProfitLossTemplates = computed(() => {
  // 用于跟踪已处理的模板描述
  const processedDescriptions = new Set();
  const processedClassNames = new Set();
  
  // 筛选结果数组
  const uniqueTemplates: TemplateItem[] = [];
  
  // 遍历所有模板
  profitLossTemplates.value.forEach(template => {
    // 优先使用描述作为唯一键
    if (template.cnClassName && !processedDescriptions.has(template.cnClassName)) {
      processedDescriptions.add(template.className);
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

// 过滤出唯一的资金管理策略模板（按描述或类名去重）
const uniqueFundTemplates = computed(() => {
  // 用于跟踪已处理的模板描述
  const processedDescriptions = new Set();
  const processedClassNames = new Set();
  
  // 筛选结果数组
  const uniqueTemplates: TemplateItem[] = [];
  
  // 遍历所有模板
  fundTemplates.value.forEach(template => {
    // 优先使用描述作为唯一键
    if (template.cnClassName && !processedDescriptions.has(template.cnClassName)) {
      processedDescriptions.add(template.cnClassName);
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

// 开仓方法选项列表 - 筛选与当前模板相关的所有方法
const entryMethods = computed<MethodItem[]>(() => {
  const selectedTemplateId = form.value.entry.templateId;
  
  if (!selectedTemplateId) {
    return []
  }
  
  // 查找当前选中的模板对象
  const selectedTemplate = openPositionTemplates.value.find(t => t.id === selectedTemplateId)
  if (!selectedTemplate) {
    return []
  }
  
  // 找到所有与当前模板描述相同的模板
  const relatedTemplates = openPositionTemplates.value.filter(t => 
    (t.className && t.className === selectedTemplate.className) || 
    (t.cnClassName && t.cnClassName === selectedTemplate.cnClassName)
  );
  
  console.log('相关开仓模板数量:', relatedTemplates.length)
  
  // 将这些相关模板转换为开仓方法
  const methods = relatedTemplates
    .filter(template => template.funName) // 只保留有funName的模板
    .map(template => ({ 
      className: template.className,
      cnClassName: template.cnClassName,
      funName: template.funName, // 确保保存funName
      cnFunName: template.cnFunName,
      funArgs: template.funArgs,
      funArgsDes: template.funArgsDes,
      classArgs: template.classArgs,
      classArgsDes: template.classArgsDes
    }));
  
  // 调试信息
  methods.forEach(m => logMethodDetails(m, '开仓方法'));
  
  return methods
});

// 止盈止损方法选项列表 - 筛选与当前模板相关的所有方法
const stopLossMethods = computed<MethodItem[]>(() => {
  const selectedTemplateId = form.value.stopLoss.templateId;
  
  if (!selectedTemplateId) {
    return []
  }
  
  // 查找当前选中的模板对象
  const selectedTemplate = profitLossTemplates.value.find(t => t.id === selectedTemplateId)
  if (!selectedTemplate) {
    return []
  }
  
  // 找到所有与当前模板类名相同的模板
  const relatedTemplates = profitLossTemplates.value.filter(t => 
  (t.cnClassName && t.cnClassName === selectedTemplate.cnClassName) || 
    (t.className && t.className === selectedTemplate.className)
  );
  
  console.log('相关止盈止损模板数量:', relatedTemplates.length)
  
  // 将这些相关模板转换为止盈止损方法
  const methods = relatedTemplates
    .filter(template => template.funName) // 只保留有funName的模板
    .map(template => ({ 
      className: template.className,
      cnClassName: template.cnClassName,
      funName: template.funName, // 确保保存funName
      cnFunName: template.cnFunName,
      funArgs: template.funArgs,
      funArgsDes: template.funArgsDes,
      classArgs: template.classArgs,
      classArgsDes: template.classArgsDes
    }));
  
  // 调试信息
  methods.forEach(m => logMethodDetails(m, '止盈止损方法'));
  
  return methods
});

// 资金管理方法选项列表 - 筛选与当前模板相关的所有方法
const positionMethods = computed<MethodItem[]>(() => {
  const selectedTemplateId = form.value.position.templateId;
  
  if (!selectedTemplateId) {
    return []
  }
  
  // 查找当前选中的模板对象
  const selectedTemplate = fundTemplates.value.find(t => t.id === selectedTemplateId)
  if (!selectedTemplate) {
    return []
  }
  
  // 找到所有与当前模板类名相同的模板
  const relatedTemplates = fundTemplates.value.filter(t => 
    (t.className && t.className === selectedTemplate.className)
  );
  
  console.log('相关资金管理模板数量:', relatedTemplates.length)
  
  // 将这些相关模板转换为资金管理方法
  const methods = relatedTemplates
    .filter(template => template.funName) // 只保留有funName的模板
    .map(template => ({ 
      className: template.className,
      cnClassName: template.cnClassName,
      funName: template.funName, // 确保保存funName
      cnFunName: template.cnFunName,
      funArgs: template.funArgs,
      funArgsDes: template.funArgsDes,
      classArgs: template.classArgs,
      classArgsDes: template.classArgsDes
    }));
  
  // 调试信息
  methods.forEach(m => logMethodDetails(m, '资金管理方法'));
  
  return methods
});

// 监听开仓策略模板ID变化
watch(() => form.value.entry.templateId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    // 清空旧的模板参数
    form.value.entry.params = {}
    form.value.entryMethod = ''
    // 获取新模板的参数，并设置默认值
    const params = getTemplateParams(newVal, 'entry')
    if (params.length > 0) {
      params.forEach(param => {
        // 只有当参数有默认值时才设置
        if (param.defaultValue !== undefined && param.defaultValue !== null && param.defaultValue !== '') {
          form.value.entry.params[param.name] = param.defaultValue
        }
      })
    }
    
    // 自动设置开仓方法 - 根据当前选中的模板获取所有相关方法
    if (newVal) {
      const selectedTemplate = openPositionTemplates.value.find(t => t.id === newVal)
      if (selectedTemplate) {
        console.log('选中开仓模板:', selectedTemplate)
        
        // 找到所有与当前模板相关的方法
        const methods = entryMethods.value
        
        if (methods.length > 0) {
          // 默认选择第一个方法
          const firstMethod = methods[0]
          const methodName = firstMethod.cnFunName
          
          if (methodName) {
            console.log('默认选择开仓方法:', methodName)
            form.value.entryMethod = methodName
            
            // 初始化方法参数对象
            if (!form.value.entry.methodParams) {
              form.value.entry.methodParams = {}
            }
            
            // 初始化参数
            const method = methods.find(m => 
               (m.cnFunName === methodName)
            )
            
            if (method) {
              // 优先复制funArgs参数到方法参数
              if (method.funArgs) {
                console.log('复制函数参数到开仓方法参数:', method.funArgs)
                Object.entries(method.funArgs).forEach(([key, value]) => {
                  form.value.entry.methodParams[key] = value
                })
              }
              // 如果没有funArgs，则使用classArgs
              else if (method.classArgs) {
                console.log('复制类参数到开仓方法参数:', method.classArgs)
                Object.entries(method.classArgs).forEach(([key, value]) => {
                  form.value.entry.methodParams[key] = value
                })
              }
            }
          }
        }
      }
    }
  }
}, { immediate: true })

// 确保form.entry.methodParams初始化，防止访问错误
watch(() => form.value.entryMethod, (newVal) => {
  if (newVal && !form.value.entry.methodParams[newVal]) {
    // 初始化方法参数对象
    form.value.entry.methodParams = {}
    
    // 获取参数列表
    const params = getIndicatorParams(newVal)
    
    // 使用默认值初始化
    params.forEach(param => {
      if (param.name && param.defaultValue !== undefined) {
        form.value.entry.methodParams[param.name] = param.defaultValue
      }
    })
  }
}, { immediate: true })

// 监听开仓策略模板变化，当选择"自定义"模板时切换到公式构造器模式
watch(() => form.value.entry.templateId, (newVal) => {
  if (newVal) {
    // 查找选中的模板
    const selectedTemplate = openPositionTemplates.value.find(t => t.id === newVal)
    
    // 如果模板名称包含"自定义"，则切换到自定义公式模式
    if (selectedTemplate && 
        ((selectedTemplate.className && selectedTemplate.className.includes('Custom')) || 
         (selectedTemplate.cnClassName && selectedTemplate.cnClassName.includes('自定义')))) {
      form.value.entryMode = 'custom'
      
      // 检查现有的公式数据
      if (!form.value.entry.customFormula) {
        // 初始化自定义公式数据结构 - 使用后端期望的格式 (单数形式)
        form.value.entry.customFormula = {
          label: [],
          action: [],
          bar: [],
          args: []
        }
        
        console.log('初始化自定义公式数据:', form.value.entry.customFormula);
      }
      
      // 更新formulaData对象，使其与表单数据保持同步
      // 注意：FormulaBuilder 组件使用复数形式的字段名 (labels, actions, bars)
      formulaData.value = {
        formula: '',
        labels: form.value.entry.customFormula.label ? [...form.value.entry.customFormula.label] : [],
        actions: form.value.entry.customFormula.action ? [...form.value.entry.customFormula.action] : [],
        bars: form.value.entry.customFormula.bar ? [...form.value.entry.customFormula.bar] : []
      }
      
      console.log('已更新formulaData (FormulaBuilder格式):', formulaData.value);
    } else {
      form.value.entryMode = 'template'
    }
  }
}, { immediate: true })

// 监听止盈止损模板ID变化
watch(() => form.value.stopLoss.templateId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    // 清空旧的模板参数
    form.value.stopLoss.params = {}
    form.value.stopLossMethod = ''
    form.value.stopLoss.method = ''
    // 获取新模板的参数，并设置默认值
    const params = getTemplateParams(newVal, 'exit')
    if (params.length > 0) {
      params.forEach(param => {
        // 只有当参数有默认值时才设置
        if (param.defaultValue !== undefined && param.defaultValue !== null && param.defaultValue !== '') {
          form.value.stopLoss.params[param.name] = param.defaultValue
        }
      })
    }
    
    // 自动设置止盈止损方法 - 根据当前选中的模板获取所有相关方法
    if (newVal) {
      const selectedTemplate = profitLossTemplates.value.find(t => t.id === newVal)
      if (selectedTemplate) {
        console.log('选中止盈止损模板:', selectedTemplate)
        
        // 找到所有与当前模板相关的方法
        const methods = stopLossMethods.value
        
        if (methods.length > 0) {
          // 默认选择第一个方法
          const firstMethod = methods[0]
          const methodName = firstMethod.cnFunName
          
          if (methodName) {
            console.log('默认选择止盈止损方法:', methodName)
            form.value.stopLossMethod = methodName
            form.value.stopLoss.method = methodName
            
            // 初始化方法参数对象
            if (!form.value.stopLoss.methodParams) {
              form.value.stopLoss.methodParams = {}
            }
            
            // 初始化参数
            const method = methods.find(m => 
              (m.cnFunName === methodName)
            )
            
            if (method) {
              // 优先复制funArgs参数到方法参数
              if (method.funArgs) {
                console.log('复制函数参数到止盈止损方法参数:', method.funArgs)
                Object.entries(method.funArgs).forEach(([key, value]) => {
                  form.value.stopLoss.methodParams[key] = value
                })
              }
            }
          }
        }
      }
    }
  }
}, { immediate: true })

// 确保form.stopLoss.methodParams初始化，防止访问错误
watch(() => form.value.stopLossMethod, (newVal) => {
  form.value.stopLoss.method = newVal || ''
  
  if (newVal && !form.value.stopLoss.methodParams) {
    // 初始化方法参数对象
    form.value.stopLoss.methodParams = {}
  }
  
  if (newVal) {
    // 获取参数列表
    const params = getIndicatorParams(newVal)
    
    // 使用默认值初始化
    params.forEach(param => {
      if (param.name && param.defaultValue !== undefined) {
        form.value.stopLoss.methodParams[param.name] = param.defaultValue
      }
    })
  }
}, { immediate: true })

// 反向监听，确保双向同步
watch(() => form.value.stopLoss.method, (newVal) => {
  form.value.stopLossMethod = newVal || ''
}, { immediate: true })

// 监听资金管理模板ID变化
watch(() => form.value.position.templateId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    // 清空旧的模板参数
    form.value.position.params = {}
    form.value.positionMethod = ''
    form.value.position.method = ''
    // 获取新模板的参数，并设置默认值
    const params = getTemplateParams(newVal, 'fund')
    if (params.length > 0) {
      params.forEach(param => {
        // 只有当参数有默认值时才设置
        if (param.defaultValue !== undefined && param.defaultValue !== null && param.defaultValue !== '') {
          form.value.position.params[param.name] = param.defaultValue
        }
      })
    }
    
    // 自动设置资金管理方法 - 根据当前选中的模板获取所有相关方法
    if (newVal) {
      const selectedTemplate = fundTemplates.value.find(t => t.id === newVal)
      if (selectedTemplate) {
        console.log('选中资金管理模板:', selectedTemplate)
        
        // 找到所有与当前模板相关的方法
        const methods = positionMethods.value
        
        if (methods.length > 0) {
          // 默认选择第一个方法
          const firstMethod = methods[0]
          const methodName = firstMethod.cnFunName
          
          if (methodName) {
            console.log('默认选择资金管理方法:', methodName)
            form.value.positionMethod = methodName
            form.value.position.method = methodName
            
            // 初始化方法参数对象
            if (!form.value.position.methodParams) {
              form.value.position.methodParams = {}
            }
            
            // 初始化参数
            const method = methods.find(m => 
              (m.cnFunName === methodName)
            )
            
            if (method) {
              // 优先复制funArgs参数到方法参数
              if (method.funArgs) {
                console.log('复制函数参数到资金管理方法参数:', method.funArgs)
                Object.entries(method.funArgs).forEach(([key, value]) => {
                  form.value.position.methodParams[key] = value
                })
              }
              
            }
          }
        }
      }
    }
  }
}, { immediate: true })

// 确保form.position.methodParams初始化，防止访问错误
watch(() => form.value.positionMethod, (newVal) => {
  form.value.position.method = newVal || ''
  
  if (newVal && !form.value.position.methodParams) {
    // 初始化方法参数对象
    form.value.position.methodParams = {}
  }
  
  if (newVal) {
    // 获取参数列表
    const params = getIndicatorParams(newVal)
    
    // 使用默认值初始化
    params.forEach(param => {
      if (param.name && param.defaultValue !== undefined) {
        form.value.position.methodParams[param.name] = param.defaultValue
      }
    })
  }
}, { immediate: true })

// 反向监听，确保双向同步
watch(() => form.value.position.method, (newVal) => {
  form.value.positionMethod = newVal || ''
}, { immediate: true })

// 监听表单中的本金和最大持仓数量，同步到position字段
watch(() => form.value.capital, (newVal) => {
  if (newVal !== undefined && newVal !== null) {
    form.value.position.size = newVal;
    console.log('同步本金到position.size:', newVal);
  }
}, { immediate: true });

watch(() => form.value.maxPositions, (newVal) => {
  if (newVal !== undefined && newVal !== null) {
    form.value.position.maxPositions = newVal;
    console.log('同步最大持仓数量到position.maxPositions:', newVal);
  }
}, { immediate: true });

// 反向监听，确保双向同步
watch(() => form.value.position.size, (newVal) => {
  if (newVal !== undefined && newVal !== null && newVal !== form.value.capital) {
    form.value.capital = newVal;
    console.log('同步position.size到本金:', newVal);
  }
}, { immediate: true });

watch(() => form.value.position.maxPositions, (newVal) => {
  if (newVal !== undefined && newVal !== null && newVal !== form.value.maxPositions) {
    form.value.maxPositions = newVal;
    console.log('同步position.maxPositions到最大持仓数量:', newVal);
  }
}, { immediate: true });

// 判断当前是否为固定交易对模板
const isFixedSymbolTemplate = computed(() => {
  if (!form.value.stockSelectionTemplateId) return false
  
  const selectedTemplate = symbolSelectionTemplates.value.find(t => t.id === form.value.stockSelectionTemplateId)
  if (!selectedTemplate) return false
  
  return selectedTemplate.cnClassName === '固定交易对'
})

// 添加交易对
const addSymbol = () => {
  symbols.value.push('')
}

// 删除交易对
const removeSymbol = (index: number) => {
  symbols.value.splice(index, 1)
}

// 表单提交前处理
const prepareFormData = () => {
  const formData: any = {
    name: form.value.name,
    description: form.value.description,
    status: form.value.status,
    
    indicators: [
      ...form.value.technicalIndicators.map(indicator => ({ 
        indicatorId: indicator.id,
        indicatorName: indicator.name,
        args: indicator.params || {}
      })),
      ...form.value.fundamentalIndicators.map(indicator => ({ 
        indicatorId: indicator.id,
        indicatorName: indicator.name,
        args: indicator.params || {}
      }))
    ],
    
    backtest: {
      startDate: form.value.backtestStart,
      endDate: form.value.backtestEnd,
      capital: form.value.position.size, // 确保使用position.size作为本金
      maxPositions: form.value.position.maxPositions // 确保使用position.maxPositions作为最大持仓数量
    }
  }
  
  // 获取各模块的方法名称 - 需要转换为真实的Java方法名
  let stockSelectionFunName = ""
  let entryFunName = ""
  let stopLossFunName = ""
  let positionFunName = ""
  
  // 查找选股方法的真实funName
  if (form.value.stockSelectionMethod) {
    const method = stockSelectionMethods.value.find(m => m.funName === form.value.stockSelectionMethod)
    if (method) {
      stockSelectionFunName = method.funName
    }
  }
  
  // 查找开仓方法的真实funName
  if (form.value.entryMethod) {
    const method = entryMethods.value.find(m => m.funName === form.value.entryMethod)
    if (method) {
      entryFunName = method.funName
    }
  }
  
  // 查找止盈止损方法的真实funName
  if (form.value.stopLossMethod) {
    const method = stopLossMethods.value.find(m => m.funName === form.value.stopLossMethod)
    if (method) {
      stopLossFunName = method.funName
    }
  }
  
  // 查找资金管理方法的真实funName
  if (form.value.positionMethod) {
    const method = positionMethods.value.find(m => m.funName === form.value.positionMethod)
    if (method) {
      positionFunName = method.funName
    }
  }
  
  // 额外的策略配置数据
  const extraData: any = {
    capital: form.value.position.size, // 确保使用position.size作为本金
    maxPositions: form.value.position.maxPositions, // 确保使用position.maxPositions作为最大持仓数量
    lever: form.value.lever.toString(), // 添加杠杆值，转换为字符串
    
    // 保存选股策略信息
    stockSelectionTemplateId: form.value.stockSelectionTemplateId,
    stockSelectionMethod: stockSelectionFunName, // 使用转换后的方法名
    stockSelectionParams: form.value.stockSelection.templateParams,
    stockSelectionMethodParams: form.value.stockSelectionMethod ? form.value.stockSelection.params[form.value.stockSelectionMethod] : {},
    
    // 保存开仓策略信息
    entryTemplateId: form.value.entry.templateId,
    entryMethod: entryFunName, // 使用转换后的方法名
    entryParams: form.value.entry.params,
    entryMethodParams: form.value.entry.methodParams,
    
    // 保存止盈止损策略信息
    stopLossTemplateId: form.value.stopLoss.templateId,
    stopLossMethod: stopLossFunName, // 使用转换后的方法名
    stopLossParams: form.value.stopLoss.params,
    stopLossMethodParams: form.value.stopLoss.methodParams,
    
    // 保存资金管理策略信息
    positionTemplateId: form.value.position.templateId,
    positionMethod: positionFunName, // 使用转换后的方法名
    positionParams: form.value.position.params,
    positionMethodParams: form.value.position.methodParams
  }
  
  // 如果是固定交易对模板，把交易对数组放入templateParams
  if (isFixedSymbolTemplate.value && symbols.value.length > 0) {
    extraData.stockSelectionParams = {
      ...form.value.stockSelection.templateParams,
      symbols: symbols.value.filter(s => s.trim() !== '') // 过滤掉空白交易对
    }
  }
}

// 从方法对象中查找真实函数名
const findRealMethodName = () => {
  // 查找选股方法的真实funName
  if (form.value.stockSelectionMethod) {
    const method = stockSelectionMethods.value.find(m => m.funName === form.value.stockSelectionMethod)
    if (method) {
      stockSelectionFunName = method.funName || ''
    }
  }
  
  // 查找开仓方法的真实funName
  if (form.value.entryMethod) {
    const method = entryMethods.value.find(m => m.funName === form.value.entryMethod)
    if (method) {
      entryFunName = method.funName || ''
    }
  }
  
  // 查找止盈止损方法的真实funName
  if (form.value.stopLossMethod) {
    const method = stopLossMethods.value.find(m => m.funName === form.value.stopLossMethod)
    if (method) {
      stopLossFunName = method.funName || ''
    }
  }
  
  // 查找资金管理方法的真实funName
  if (form.value.positionMethod) {
    const method = positionMethods.value.find(m => m.funName === form.value.positionMethod)
    if (method) {
      positionFunName = method.funName || ''
    }
  }
}
</script>

<style scoped lang="scss">
.create-strategy {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  min-height: calc(100vh - 60px - 40px);
  padding: 20px 0;
  
  .strategy-form {
    width: 100%;
    display: block;
    background-color: #fff;
    padding: 0;
    margin-bottom: 20px;
    
    :deep(.el-card__body) {
      padding: 20px;
    }
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      h2 {
        margin: 0;
      }
    }
    
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
  }
  
  // 方法详情卡片样式
  .method-detail-card {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 20px;
    border-left: 4px solid #409eff;
    
    h4 {
      margin-top: 0;
      margin-bottom: 10px;
      font-size: 16px;
      color: #303133;
    }
    
    .method-description {
      color: #606266;
      font-size: 14px;
      line-height: 1.5;
      margin-bottom: 15px;
    }
    
    .el-divider {
      margin: 12px 0;
    }
  }
  
  // 参数配置区域样式
  .param-config {
    margin-bottom: 15px;
    
    .param-label {
      display: flex;
      align-items: center;
      margin-bottom: 6px;
      
      .param-name {
        font-weight: 500;
        margin-right: 6px;
      }
      
      .el-icon {
        color: #909399;
        font-size: 14px;
        cursor: pointer;
      }
    }
  }
  
  // 空参数状态样式
  .empty-params {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
    color: #909399;
  }

  .formula-builder-container {
    width: 100%;
    height: 100%;
    min-height: 600px;
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .custom-formula-builder {
    width: 100%;
    height: 100%;
    min-height: 500px;
    display: block;
  }

  .formula-builder-wrapper {
    min-height: 500px;
  }

  .formula-placeholder {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
    color: #909399;
  }

  .json-preview {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 4px;
    border: 1px solid #ddd;
    font-family: monospace;
    white-space: pre-wrap;
    max-height: 300px;
    overflow-y: auto;
  }

  .preview-section {
    margin-top: 20px;
  }

  // 添加params-container样式
  .params-container {
    background-color: #f5f7fa;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 15px;
  }

  // 保留param-config的样式
  .param-config {
    margin-bottom: 15px;
    
    .param-label {
      display: flex;
      align-items: center;
      margin-bottom: 6px;
      
      .param-name {
        font-weight: 500;
        margin-right: 6px;
      }
      
      .el-icon {
        color: #909399;
        font-size: 14px;
        cursor: pointer;
      }
    }
  }

  // 交易对输入样式
  .symbol-list {
    margin-top: 10px;
  }

  .symbol-item {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }

  .symbol-input {
    flex: 1;
    margin-right: 10px;
  }

  .symbol-delete-btn {
    flex-shrink: 0;
  }

  .add-symbol-btn {
    margin-top: 5px;
  }
}
</style> 