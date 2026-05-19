<template>
  <div class="formula-builder">
    <h3>公式构造器</h3>
    
    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="toolbar-section">
        <h4>操作符</h4>
        <div class="button-group">
          <el-button size="small" @click="addOperation('ELIF')">附加条件</el-button>
          <el-button size="small" @click="addOperation('ELSE')">否则</el-button>
          <el-button size="small" @click="addOperation('EQUAL')">等于</el-button>
          <el-button size="small" @click="addOperation('GREATER')">大于</el-button>
          <el-button size="small" @click="addOperation('LESS')">小于</el-button>
          <el-button size="small" @click="addOperation('GREATER_EQUAL')">大于等于</el-button>
          <el-button size="small" @click="addOperation('LESS_EQUAL')">小于等于</el-button>
          <el-button size="small" @click="addOperation('AND')">并且</el-button>
          <el-button size="small" @click="addOperation('OR')">或者</el-button>
          <el-button size="small" @click="addOperation('ADD')">加</el-button>
          <el-button size="small" @click="addOperation('SUBTRACTION')">减</el-button>
          <el-button size="small" @click="addOperation('MULTIPLICATION')">乘</el-button>
          <el-button size="small" @click="addOperation('DIVISION')">除</el-button>
          <el-button size="small" @click="addOperation('IS')">等于</el-button>
          <el-button size="small" @click="addOperation('LONG')">做多</el-button>
          <el-button size="small" @click="addOperation('SHORT')">做空</el-button>
          <el-button size="small" @click="promptForNumber">数字</el-button>
        </div>
      </div>
      
      <div class="toolbar-section">
        <h4>K线数据</h4>
        <div class="button-group">
          <el-dropdown @command="addKLineData">
            <el-button size="small">开盘价<i class="el-icon-arrow-down el-icon--right"></i></el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="open[0]">当前周期</el-dropdown-item>
                <el-dropdown-item 
                  v-for="n in 80" 
                  :key="`open-${n}`" 
                  :command="`open[-${n}]`">
                  前{{ n }}个周期
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <el-dropdown @command="addKLineData">
            <el-button size="small">最高价<i class="el-icon-arrow-down el-icon--right"></i></el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="high[0]">当前周期</el-dropdown-item>
                <el-dropdown-item 
                  v-for="n in 80" 
                  :key="`high-${n}`" 
                  :command="`high[-${n}]`">
                  前{{ n }}个周期
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <el-dropdown @command="addKLineData">
            <el-button size="small">最低价<i class="el-icon-arrow-down el-icon--right"></i></el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="low[0]">当前周期</el-dropdown-item>
                <el-dropdown-item 
                  v-for="n in 80" 
                  :key="`low-${n}`" 
                  :command="`low[-${n}]`">
                  前{{ n }}个周期
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <el-dropdown @command="addKLineData">
            <el-button size="small">收盘价<i class="el-icon-arrow-down el-icon--right"></i></el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="close[0]">当前周期</el-dropdown-item>
                <el-dropdown-item 
                  v-for="n in 80" 
                  :key="`close-${n}`" 
                  :command="`close[-${n}]`">
                  前{{ n }}个周期
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <el-dropdown @command="addKLineData">
            <el-button size="small">成交量<i class="el-icon-arrow-down el-icon--right"></i></el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="volume[0]">当前周期</el-dropdown-item>
                <el-dropdown-item 
                  v-for="n in 80" 
                  :key="`volume-${n}`" 
                  :command="`volume[-${n}]`">
                  前{{ n }}个周期
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <div class="toolbar-section">
        <h4>指标</h4>
        <div class="button-group indicators-group" v-if="indicators.length > 0">
          <el-button 
            v-for="indicator in indicators" 
            :key="indicator.name"
            size="small" 
            @click="selectIndicator(indicator)">
            {{ indicator.cnName || indicator.name }}
          </el-button>
        </div>
        <div v-else class="empty-indicators">
          <el-alert
            title="未找到指标"
            type="info"
            :closable="false"
            description="请确保已成功加载指标数据。">
          </el-alert>
        </div>
      </div>
    </div>
    
    <!-- 公式显示区域 -->
    <div class="formula-display">
      <h4>公式预览</h4>
      <pre class="formula-code" v-html="displayFormula"></pre>
      
      <div class="formula-actions">
        <el-button type="danger" size="small" @click="clearFormula">清空公式</el-button>
        <el-button type="primary" size="small" @click="validateFormula">验证公式</el-button>
      </div>
    </div>
    
    <!-- 指标参数配置 -->
    <div class="indicator-params" v-if="currentIndicator">
      <h4>{{ currentIndicator.cnName || currentIndicator.name }} 参数配置</h4>
      <el-form :model="currentIndicatorParams" label-width="120px" size="small">
        <el-form-item 
          v-for="(param, key) in currentIndicator.params" 
          :key="key" 
          :label="param.description || key">
          <el-input 
            v-model="currentIndicatorParams[key]" 
            :placeholder="`输入${param.description || key}`">
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="addIndicatorToFormula">添加到公式</el-button>
          <el-button @click="cancelIndicatorSelection">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 用户输入数字 -->
    <div class="number-input" v-if="showNumberInput">
      <h4>输入数字</h4>
      <el-form inline>
        <el-form-item>
          <el-input v-model="numberValue" placeholder="请输入数值" type="number"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addNumberToFormula">添加</el-button>
          <el-button @click="cancelNumberInput">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  indicators: {
    type: Array,
    default: () => []
  },
  formula: {
    type: String,
    default: ''
  },
  initialData: {
    type: Object,
    default: () => ({
      formula: '',
      actions: [],
      labels: [],
      bars: []
    })
  }
})

const emit = defineEmits(['update:formula', 'formula-change'])

// 监听formula属性变化
watch(() => props.formula, (newValue) => {
  if (newValue !== displayFormula.value) {
    // 如果外部formula变化且与内部不同，更新内部显示
    displayFormula.value = newValue
  }
}, { immediate: true })

// 监听initialData变化
watch(() => props.initialData, (newValue) => {
  if (newValue) {
    console.log('Formula Builder收到初始数据:', newValue);
    
    // 如果有actions数据，则使用它替换当前actions
    if (newValue.actions && Array.isArray(newValue.actions) && newValue.actions.length > 0) {
      formulaActions.value = [...newValue.actions];
    }
    
    // 如果有labels数据，则使用它替换当前labels
    if (newValue.labels && Array.isArray(newValue.labels) && newValue.labels.length > 0) {
      formulaLabels.value = [...newValue.labels];
    }
    
    // 如果有bars数据，则使用它替换当前bars
    if (newValue.bars && Array.isArray(newValue.bars) && newValue.bars.length > 0) {
      formulaBars.value = [...newValue.bars];
    }
    
    // 更新显示的公式
    if (newValue.formula) {
      displayFormula.value = newValue.formula;
    } else {
      // 如果没有现成的formula文本，但有actions数据，则重新生成formula
      updateDisplayFormula();
    }
  }
}, { deep: true, immediate: true })

// 更新formula并触发事件
const updateFormula = (newFormula) => {
  displayFormula.value = newFormula
  emit('update:formula', newFormula)
  emit('formula-change', newFormula)
}

// 操作符映射
const operationMap = {
  FI: "if",
  ELIF: "elif",
  ELSE: "else",
  EQUAL: "==",
  GREATER: ">",
  LESS: "<",
  GREATER_EQUAL: ">=",
  LESS_EQUAL: "<=",
  END: ":",
  AND: "and",
  OR: "or",
  ADD: "+",
  SUBTRACTION: "-",
  MULTIPLICATION: "*",
  DIVISION: "/",
  METHOD: "m",
  BAR: "b",
  ENTER: "e",
  RETURN: "return",
  IS: "=",
  LONG: "1",
  SHORT: "0",
  BACK: "k",
  TD: "td"
}

// 操作符显示名称映射（中文）
const operationDisplayMap = {
  FI: "如果",
  ELIF: "附加条件",
  ELSE: "否则",
  EQUAL: "等于",
  GREATER: "大于",
  LESS: "小于",
  GREATER_EQUAL: "大于等于",
  LESS_EQUAL: "小于等于",
  END: "：",
  AND: "并且",
  OR: "或者",
  ADD: "+",
  SUBTRACTION: "-",
  MULTIPLICATION: "*",
  DIVISION: "/",
  METHOD: "", // 将由具体指标替换
  BAR: "", // 将由具体K线数据替换
  ENTER: "\n",
  RETURN: "", // 不显示"返回"操作符
  IS: "=",
  LONG: "做多",
  SHORT: "做空",
  BACK: "", // 缩进控制，不显示
  TD: "TD"
}

// 公式相关数据
const formulaActions = ref([])     // 存储操作
const formulaLabels = ref([])      // 存储指标
const formulaBars = ref([])        // 存储K线数据
const indentLevel = ref(0)         // 当前缩进级别
const displayFormula = ref('')     // 用于显示的公式文本

// 当前选中的指标和参数
const currentIndicator = ref(null)
const currentIndicatorParams = ref({})
const showNumberInput = ref(false)
const numberValue = ref('')

// 将操作转换为可读的公式文本
const updateDisplayFormula = () => {
  let formula = ''
  let currentIndent = 0
  let skipNextEnter = false // 用于跳过ELSE后的ENTER
  
  for (let i = 0; i < formulaActions.value.length; i++) {
    const action = formulaActions.value[i]
    
    // 处理缩进
    if (action === 'BACK' || action === 'k') { // 回退缩进
      if (currentIndent > 0) currentIndent--
      continue
    }
    
    // 添加当前缩进
    if (i === 0 || 
        (formulaActions.value[i-1] === 'END' && action !== 'ELSE') || 
        (action === 'ELIF' || action === 'ELSE')) {
      // 如果是ELIF或ELSE，先添加换行和缩进
      if (action === 'ELIF' || action === 'ELSE') {
        formula += '\n' + '  '.repeat(currentIndent)
        
        // 如果是ELSE，标记跳过下一个ENTER
        if (action === 'ELSE') {
          skipNextEnter = true
          // 预先增加缩进，因为我们不会处理ELSE后面的ENTER了
          currentIndent++
        }
      } else {
        formula += '  '.repeat(currentIndent)
      }
    }
    
    // 特殊处理if条件语句后的冒号，添加换行和缩进
    if (action === 'END') {
      currentIndent++
      continue
    }
    
    // 处理换行
    if (action === '\n' || action === 'ENTER' || action === 'e') {
      // 如果需要跳过这个ENTER（跟在ELSE后面），直接跳过
      if (skipNextEnter) {
        skipNextEnter = false
        continue
      }
      
      formula += '\n' + '  '.repeat(currentIndent)
      continue
    }
    
    // 处理K线数据
    if ((action === 'BAR' || action === 'b') && i + 1 < formulaActions.value.length) {
      const barIndex = parseInt(formulaActions.value[i + 1])
      const barData = formulaBars.value[barIndex]
      
      if (barData) {
        // 解析K线数据格式: "open[0]" 或 "close[-1]" 等
        const matches = barData.match(/([a-z]+)\[(-?\d+)\]/)
        if (matches) {
          const dataType = matches[1]
          const periodOffset = parseInt(matches[2])
          
          // 转换为中文显示
          let dataTypeCn = ''
          switch (dataType) {
            case 'open': dataTypeCn = '开盘价'; break
            case 'high': dataTypeCn = '最高价'; break
            case 'low': dataTypeCn = '最低价'; break
            case 'close': dataTypeCn = '收盘价'; break
            case 'volume': dataTypeCn = '成交量'; break
            default: dataTypeCn = dataType
          }
          
          // 转换周期描述
          let periodDescription = ''
          if (periodOffset === 0) {
            periodDescription = '(当前)'
          } else if (periodOffset < 0) {
            periodDescription = `(前${Math.abs(periodOffset)}个周期)`
          } else {
            periodDescription = `(后${periodOffset}个周期)`
          }
          
          // 前后添加空格，使用绿色显示K线数据
          formula += ' <span style="color: #67c23a;">' + dataTypeCn + periodDescription + '</span> '
          i++ // 跳过下一个操作，因为已经处理了
          continue
        }
      }
    }
    
    // 处理指标
    if ((action === 'METHOD' || action === 'm') && i + 1 < formulaActions.value.length) {
      const methodIndex = parseInt(formulaActions.value[i + 1])
      const methodData = formulaLabels.value[methodIndex]
      
      if (methodData) {
        // 获取指标的中文名称
        const methodName = methodData.cnName || methodData.name
        
        // 显示指标名称及参数，使用橙色显示指标
        formula += ' <span style="color: #e6a23c;">' + methodName
        
        const params = methodData.params
        if (params && Object.keys(params).length > 0) {
          formula += '('
          // 查找原始指标定义，获取参数描述
          const originalIndicator = props.indicators.find(ind => ind.name === methodData.name)
          
          // 构建参数数组，使用参数描述
          const paramsArray = []
          
          for (const key in params) {
            let paramDesc = key
            
            if (originalIndicator && originalIndicator.params && originalIndicator.params[key]) {
              paramDesc = originalIndicator.params[key].description || key
            }
            
            paramsArray.push(`${paramDesc}=${params[key]}`)
          }
          
          formula += paramsArray.join(', ')
          formula += ')'
        }
        
        formula += '</span> ' // 关闭span标签
        i++ // 跳过下一个操作，因为已经处理了
        continue
      }
    }
    
    // 查找动作的显示名称
    let displayText = ''
    
    if (operationDisplayMap[action]) {
      // 使用中文显示名称
      displayText = operationDisplayMap[action]
    } else {
      // 如果没有直接映射，尝试通过operationMap找到对应的别名
      displayText = action
    }
    
    // 不为空才添加
    if (displayText.trim() !== '') {
      // 根据操作类型使用不同颜色
      // 条件语句 - 蓝色
      if (['如果', '附加条件', '否则', '：'].includes(displayText)) {
        formula += `<span style="color: #409EFF;">${displayText}</span>`
      } 
      // 比较操作符 - 紫色
      else if (['等于', '大于', '小于', '大于等于', '小于等于', '='].includes(displayText)) {
        formula += `<span style="color: #9c27b0;">${displayText}</span>`
      }
      // 逻辑运算符 - 红色
      else if (['并且', '或者'].includes(displayText)) {
        formula += `<span style="color: #f56c6c;">${displayText}</span>`
      }
      // 算术运算符 - 深蓝色
      else if (['+', '-', '*', '/'].includes(displayText)) {
        formula += `<span style="color: #007bff;">${displayText}</span>`
      }
      // 操作指令 - 红褐色
      else if (['做多', '做空'].includes(displayText)) {
        formula += `<span style="color: #d81b60; font-weight: bold;">${displayText}</span>`
      }
      // 其它 - 默认颜色
      else {
        formula += displayText
      }
    }
    
    // 在特定操作后添加空格
    if (['FI', 'ELIF', 'ELSE', 'EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'AND', 'OR'].includes(action)) {
      formula += ' '
    }
  }
  
  updateFormula(formula)
}

// 添加操作到公式
const addOperation = (operation) => {
  // 检查"否则"后只能添加"做多"或"做空"
  if (formulaActions.value.length >= 2 && 
      formulaActions.value[formulaActions.value.length - 2] === 'ELSE' && 
      formulaActions.value[formulaActions.value.length - 1] === 'ENTER') {
    
    // 如果不是做多或做空，阻止添加
    if (operation !== 'LONG' && operation !== 'SHORT') {
      ElMessage.warning('"否则"语句后面只能跟做多或做空')
      return
    }
  }
  
  // 检查操作符不能相邻
  const operators = ['EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'AND', 'OR', 'ADD', 'SUBTRACTION', 'MULTIPLICATION', 'DIVISION', 'IS']
  
  if (operators.includes(operation) && 
      formulaActions.value.length > 0 && 
      operators.includes(formulaActions.value[formulaActions.value.length - 1])) {
    
    ElMessage.warning('操作符之间不能相邻')
    return
  }
  
  if (operation === 'FI') { // if 或 elif
    formulaActions.value.push(operation)
  } 
    else if(operation === "ELIF") {
      formulaActions.value.push('END')
      formulaActions.value.push('BACK')
      formulaActions.value.push(operation)
  }
    else if (operation === 'ELSE') { // else
    formulaActions.value.push('END')
    formulaActions.value.push('BACK')
    formulaActions.value.push(operation)

  } else if (operation === 'RETURN') { // return
    formulaActions.value.push('END')
    formulaActions.value.push(operation)
  } else if (operation === 'BACK') { // 回退缩进
    formulaActions.value.push(operation)
  } else if (operation === 'LONG' || operation === 'SHORT') { // 做多/做空
    // 在当前位置添加空格和操作符
    formulaActions.value.push(operation)
  } else if (['EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'AND', 'OR', 'ADD', 'SUBTRACTION', 'MULTIPLICATION', 'DIVISION', 'IS'].includes(operation)) {
    // 普通操作符，前后添加空格
    formulaActions.value.push(operation)
  }
  
  updateDisplayFormula()
  emitFormulaChange()
}

// 添加数字
const promptForNumber = () => {
  showNumberInput.value = true
}

const addNumberToFormula = () => {
  if (numberValue.value !== '') {
    formulaActions.value.push(numberValue.value)
    updateDisplayFormula()
    emitFormulaChange()
  }
  cancelNumberInput()
}

const cancelNumberInput = () => {
  showNumberInput.value = false
  numberValue.value = ''
}

// 添加K线数据
const addKLineData = (dataWithIndex) => {
  // 检查是否已存在
  const barIndex = formulaBars.value.indexOf(dataWithIndex)
  
  if (barIndex === -1) {
    // 添加新的K线数据
    formulaBars.value.push(dataWithIndex)
    formulaActions.value.push('BAR')
    formulaActions.value.push((formulaBars.value.length - 1).toString())
  } else {
    // 复用已有的K线数据
    formulaActions.value.push('BAR')
    formulaActions.value.push(barIndex.toString())
  }
  
  updateDisplayFormula()
  emitFormulaChange()
}

// 选择指标
const selectIndicator = (indicator) => {
  currentIndicator.value = JSON.parse(JSON.stringify(indicator))
  currentIndicatorParams.value = {}
  
  // 初始化参数为默认值
  if (indicator.params) {
    Object.keys(indicator.params).forEach(key => {
      currentIndicatorParams.value[key] = indicator.params[key].defaultValue || ''
    })
  }
}

// 添加指标到公式
const addIndicatorToFormula = () => {
  if (!currentIndicator.value) return
  
  // 首先验证参数是否都已填写
  let allParamsFilled = true
  let missingParam = ''
  
  if (currentIndicator.value.params) {
    for (const key in currentIndicator.value.params) {
      const value = currentIndicatorParams.value[key]
      if (value === undefined || value === null || value === '') {
        allParamsFilled = false
        missingParam = currentIndicator.value.params[key].description || key
        break
      }
    }
  }
  
  if (!allParamsFilled) {
    ElMessage.warning(`请填写参数"${missingParam}"`)
    return
  }
  
  // 创建指标对象
  const indicatorWithParams = {
    name: currentIndicator.value.name,
    cnName: currentIndicator.value.cnName,
    params: { ...currentIndicatorParams.value }
  }
  
  // 检查是否已存在相同的指标+参数组合
  const existingIndex = formulaLabels.value.findIndex(label => {
    if (label.name !== indicatorWithParams.name) return false
    
    const paramsMatch = Object.keys(label.params).every(key => 
      label.params[key] === indicatorWithParams.params[key]
    )
    
    return paramsMatch
  })
  
  if (existingIndex === -1) {
    // 添加新指标
    formulaLabels.value.push(indicatorWithParams)
    formulaActions.value.push('METHOD')
    formulaActions.value.push((formulaLabels.value.length - 1).toString())
  } else {
    // 复用已有指标
    formulaActions.value.push('METHOD')
    formulaActions.value.push(existingIndex.toString())
  }
  
  updateDisplayFormula()
  emitFormulaChange()
  
  // 清空当前选择
  currentIndicator.value = null
  currentIndicatorParams.value = {}
}

// 取消指标选择
const cancelIndicatorSelection = () => {
  currentIndicator.value = null
  currentIndicatorParams.value = {}
}

// 清空公式
const clearFormula = () => {
  formulaActions.value = []
  formulaActions.value.push('FI')
  formulaLabels.value = []
  formulaBars.value = []
  indentLevel.value = 0
  updateDisplayFormula()
  emitFormulaChange()
}

// 验证公式
const validateFormula = () => {
  let valid = true
  let errorMsg = ''
  
  // 1. 检查是否包含做多或做空
  const hasLongOrShort = formulaActions.value.some(action => 
    action === 'LONG' || action === 'SHORT'
  )
  
  if (!hasLongOrShort) {
    valid = false
    errorMsg = '公式必须包含开仓方向（做多或做空）'
  }
  
  // 2. 检查操作符是否相邻
  const operators = ['EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'AND', 'OR', 'ADD', 'SUBTRACTION', 'MULTIPLICATION', 'DIVISION', 'IS']
  
  for (let i = 0; i < formulaActions.value.length - 1; i++) {
    const currAction = formulaActions.value[i]
    const nextAction = formulaActions.value[i+1]
    
    // 如果当前元素和下一个元素都是操作符，则不合法
    if (operators.includes(currAction) && operators.includes(nextAction)) {
      valid = false
      errorMsg = '操作符之间不能相邻'
      break
    }
  }
  
  // 3. 检查K线数据是否相邻
  for (let i = 0; i < formulaActions.value.length - 3; i++) {
    // 检查是否有两个相邻的K线数据
    if (formulaActions.value[i] === 'BAR' && 
        formulaActions.value[i+2] === 'BAR') {
      valid = false
      errorMsg = 'K线数据之间不能相邻，请添加操作符'
      break
    }
  }
  
  // 4. 检查指标是否相邻
  for (let i = 0; i < formulaActions.value.length - 3; i++) {
    // 检查是否有两个相邻的指标
    if (formulaActions.value[i] === 'METHOD' && 
        formulaActions.value[i+2] === 'METHOD') {
      valid = false
      errorMsg = '指标之间不能相邻，请添加操作符'
      break
    }
  }
  
  // 5. 检查K线数据和指标是否相邻
  for (let i = 0; i < formulaActions.value.length - 3; i++) {
    // 检查K线数据后面是否紧跟指标
    if ((formulaActions.value[i] === 'BAR' && 
        formulaActions.value[i+2] === 'METHOD') ||
        (formulaActions.value[i] === 'METHOD' && 
        formulaActions.value[i+2] === 'BAR')) {
      valid = false
      errorMsg = 'K线数据和指标之间不能相邻，请添加操作符'
      break
    }
  }
  
  // 6. 检查"否则"后面是否只跟做多或做空
  for (let i = 0; i < formulaActions.value.length - 2; i++) {
    if (formulaActions.value[i] === 'ELSE' && formulaActions.value[i+1] === 'ENTER') {
      // 找到ELSE语句后面的实际内容
      let j = i + 2
      // 跳过缩进和空格
      while (j < formulaActions.value.length && 
             (formulaActions.value[j] === ' ' || 
              formulaActions.value[j] === '\t' || 
              formulaActions.value[j] === '  ')) {
        j++
      }
      
      // 如果后面的内容不是做多或做空
      if (j < formulaActions.value.length && 
          formulaActions.value[j] !== 'LONG' && 
          formulaActions.value[j] !== 'SHORT') {
        valid = false
        errorMsg = '"否则"语句后面只能跟做多或做空'
        break
      }
    }
  }
  
  // 7. 检查指标参数是否填写
  for (const label of formulaLabels.value) {
    const params = label.params
    
    // 如果有参数定义
    if (params && Object.keys(params).length > 0) {
      // 检查每个参数是否都有值
      for (const key in params) {
        const value = params[key]
        if (value === undefined || value === null || value === '') {
          valid = false
          errorMsg = `指标"${label.cnName || label.name}"的参数"${key}"必须填写`
          break
        }
      }
    }
  }
  
  if (valid) {
    ElMessage.success('公式验证通过')
  } else {
    ElMessage.warning(errorMsg)
  }
  
  return valid
}

// 触发公式变更事件
const emitFormulaChange = () => {
  // 创建完整的公式数据对象，包含所有必要的数据结构
  const formulaData = {
    formula: displayFormula.value,
    actions: formulaActions.value,
    labels: formulaLabels.value,
    bars: formulaBars.value
  }
  
  // 添加详细的调试日志
  console.log('FormulaBuilder 发送数据:', {
    formulaText: formulaData.formula,
    actionsCount: formulaData.actions.length,
    labelsCount: formulaData.labels.length,
    barsCount: formulaData.bars.length
  });
  
  console.log('FormulaBuilder 发送的完整数据:', {
    actions: formulaData.actions,
    labels: formulaData.labels,
    bars: formulaData.bars
  });
  
  // 确保每个数组都是有效的数组
  if (!Array.isArray(formulaData.actions)) formulaData.actions = [];
  if (!Array.isArray(formulaData.labels)) formulaData.labels = [];
  if (!Array.isArray(formulaData.bars)) formulaData.bars = [];
  
  // 传递完整的公式数据对象
  emit('formula-change', formulaData);
  emit('update:formula', formulaData.formula);
}

// 添加空格
const addSpace = () => {
  formulaActions.value.push(' ')
  updateDisplayFormula()
  emitFormulaChange()
}

// 添加换行和缩进
const addNewLine = () => {
  formulaActions.value.push('ENTER')
  updateDisplayFormula()
  emitFormulaChange()
}

// 组件挂载
onMounted(() => {
  // 检查是否有初始数据
  if (props.initialData && props.initialData.actions && props.initialData.actions.length > 0) {
    // 使用初始数据
    console.log('使用初始数据初始化公式构建器');
  } else {
    // 自动添加FI (if)
    formulaActions.value.push('FI');
    formulaActions.value.push(' '); // 添加空格
  }
  
  updateDisplayFormula();
  emitFormulaChange();
})
</script>

<style scoped>
.formula-builder {
  width: 100%;
  height: 100%;
  min-height: 500px;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 20px;
  overflow: auto;
}

h3 {
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  border-bottom: 2px solid #ebeef5;
  padding-bottom: 12px;
}

h4 {
  margin: 12px 0;
  font-size: 16px;
  font-weight: 500;
  color: #409EFF;
}

.toolbar {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-bottom: 24px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9fafc;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.02);
}

.toolbar-section {
  margin-bottom: 12px;
  padding: 10px;
  border-radius: 6px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.button-group .el-button {
  transition: all 0.3s;
}

.button-group .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.indicators-group {
  max-height: 200px;
  overflow-y: auto;
  padding-right: 5px;
  scrollbar-width: thin;
}

.indicators-group::-webkit-scrollbar {
  width: 6px;
}

.indicators-group::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.indicators-group::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.indicators-group::-webkit-scrollbar-thumb:hover {
  background: #aaa;
}

.formula-display {
  margin: 20px 0;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  background-color: #fff;
}

.formula-code {
  min-height: 150px;
  max-height: 300px;
  overflow-y: auto;
  background-color: #f5f7fa;
  border-radius: 6px;
  padding: 15px;
  font-family: 'Courier New', Courier, monospace;
  white-space: pre-wrap;
  line-height: 1.6;
  color: #444;
  font-size: 14px;
  box-shadow: inset 0 1px 5px rgba(0, 0, 0, 0.05);
}

/* 允许在pre标签中使用v-html */
.formula-code :deep(span) {
  display: inline;
  font-family: 'Courier New', Courier, monospace;
}

.formula-actions {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.indicator-params,
.number-input {
  margin-top: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 15px;
  background-color: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.3s ease-in-out;
}

.empty-indicators {
  padding: 15px;
  border-radius: 6px;
  background-color: #fcfcfc;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 改进下拉菜单样式 */
:deep(.el-dropdown-menu) {
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-dropdown-item) {
  padding: 8px 15px;
}

:deep(.el-dropdown-item:hover) {
  background-color: #f0f7ff;
}

/* 表单样式优化 */
:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input__inner) {
  border-radius: 4px;
}

:deep(.el-input__inner:focus) {
  border-color: #409EFF;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

/* 按钮颜色分类 */
.toolbar-section:nth-child(1) .el-button {
  background-color: #ecf5ff;
  border-color: #d9ecff;
  color: #409EFF;
}

.toolbar-section:nth-child(2) .el-button {
  background-color: #f0f9eb;
  border-color: #e1f3d8;
  color: #67c23a;
}

.toolbar-section:nth-child(3) .el-button {
  background-color: #fdf6ec;
  border-color: #faecd8;
  color: #e6a23c;
}
</style>