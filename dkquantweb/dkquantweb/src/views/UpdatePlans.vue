<template>
  <div class="update-plans-container">
    <div class="page-header">
      <h1 class="page-title">项目更新计划</h1>
      <!-- 添加管理员操作按钮 -->
      <el-button v-if="isAdmin" type="primary" @click="showAddPlanDialog">
        添加更新计划
      </el-button>
    </div>
    
    <el-tabs v-model="activeTab">
      <el-tab-pane label="全部计划" name="all"></el-tab-pane>
      <el-tab-pane label="进行中" name="inProgress"></el-tab-pane>
      <el-tab-pane label="已完成" name="completed"></el-tab-pane>
      <el-tab-pane label="计划中" name="planned"></el-tab-pane>
    </el-tabs>
    
    <div class="filter-sort-bar">
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索更新计划..."
          prefix-icon="Search"
          clearable
          @input="filterPlans"
        />
      </div>
      <div class="sort-options">
        <el-select v-model="sortOption" placeholder="排序方式" @change="sortPlans">
          <el-option label="按发布日期排序" value="date" />
          <el-option label="按计划完成日期排序" value="dueDate" />
        </el-select>
      </div>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>
    
    <div v-else-if="filteredPlans.length === 0" class="empty-state">
      <el-empty description="暂无更新计划" />
    </div>
    
    <div v-else class="plans-list">
      <el-card v-for="plan in filteredPlans" :key="plan.id" class="plan-card">
        <div class="plan-header">
          <h2 class="plan-title">{{ plan.title }}</h2>
          <el-tag :type="getStatusType(plan.status)">{{ getStatusText(plan.status) }}</el-tag>
        </div>
        
        <div class="plan-content">
          <p class="plan-description">{{ plan.description }}</p>
          
          <div class="plan-progress">
            <span class="progress-text">完成进度：{{ plan.progress }}%</span>
            <el-progress :percentage="plan.progress" :status="getProgressStatus(plan.progress)" />
          </div>
          
          <div class="plan-meta">
            <div class="plan-dates">
              <div class="date-item">
                <el-icon><Calendar /></el-icon>
                <span>发布日期: {{ formatDate(plan.createTime) }}</span>
              </div>
              <div class="date-item">
                <el-icon><Clock /></el-icon>
                <span>预计完成: {{ formatDate(plan.dueDate) }}</span>
              </div>
            </div>
            
            <div class="plan-tags">
              <el-tag v-for="tag in plan.tags" :key="tag" size="small" effect="plain" class="tag-item">
                {{ tag }}
              </el-tag>
            </div>
          </div>
        </div>
        
        <div class="plan-footer">
          <el-button 
            type="primary" 
            plain
            size="small"
            @click="showPlanDetails(plan)"
          >
            查看详情
          </el-button>
          
          <!-- 管理员操作按钮 -->
          <div v-if="isAdmin" class="admin-actions">
            <el-button 
              type="warning" 
              size="small"
              @click="showEditPlanDialog(plan)"
            >
              编辑
            </el-button>
            <el-button 
              type="danger" 
              size="small"
              @click="confirmDeletePlan(plan)"
            >
              删除
            </el-button>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[5, 10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalPlans"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    
    <!-- 计划详情对话框 -->
    <el-dialog
      v-model="detailsVisible"
      title="更新计划详情"
      width="700px"
      v-if="selectedPlan"
    >
      <div v-if="selectedPlan" class="plan-details">
        <h2 class="plan-title">{{ selectedPlan.title }}</h2>
        
        <div class="details-meta">
          <el-tag :type="getStatusType(selectedPlan.status)">{{ getStatusText(selectedPlan.status) }}</el-tag>
          <span class="details-date">发布于: {{ formatDate(selectedPlan.createTime) }}</span>
          <span class="details-date">预计完成: {{ formatDate(selectedPlan.dueDate) }}</span>
        </div>
        
        <div class="details-progress">
          <span class="progress-text">完成进度：{{ selectedPlan.progress }}%</span>
          <el-progress :percentage="selectedPlan.progress" :status="getProgressStatus(selectedPlan.progress)" />
        </div>
        
        <div class="details-section">
          <h3>计划描述</h3>
          <p>{{ selectedPlan.description }}</p>
        </div>
        
        <div class="details-section">
          <h3>详细内容</h3>
          <div v-html="selectedPlan.content"></div>
        </div>
        
        <div class="details-section" v-if="selectedPlan.updates && selectedPlan.updates.length > 0">
          <h3>更新记录</h3>
          <el-timeline>
            <el-timeline-item
              v-for="update in selectedPlan.updates"
              :key="update.id"
              :timestamp="formatDate(update.updateTime)"
              :type="update.type"
            >
              {{ update.content }}
            </el-timeline-item>
          </el-timeline>
        </div>
        
        <div class="details-tags">
          <h3>相关标签</h3>
          <el-tag v-for="tag in selectedPlan.tags" :key="tag" class="tag-item" effect="plain">
            {{ tag }}
          </el-tag>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailsVisible = false">关闭</el-button>
          <!-- 管理员操作按钮 -->
          <template v-if="isAdmin">
            <el-button type="warning" @click="showEditPlanDialog(selectedPlan)">编辑</el-button>
            <el-button type="danger" @click="confirmDeletePlan(selectedPlan)">删除</el-button>
            <el-button type="success" @click="showAddUpdateRecordDialog(selectedPlan.id)">添加更新记录</el-button>
          </template>
        </div>
      </template>
    </el-dialog>
    
    <!-- 添加/编辑计划对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      :title="isEditing ? '编辑更新计划' : '添加更新计划'"
      width="700px"
    >
      <el-form :model="planForm" ref="planFormRef" :rules="planRules" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="planForm.title" placeholder="请输入计划标题" />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input v-model="planForm.description" type="textarea" :rows="3" placeholder="请输入计划描述" />
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="planForm.status" placeholder="请选择状态">
            <el-option label="计划中" value="planned" />
            <el-option label="进行中" value="inProgress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="完成进度" prop="progress">
          <el-slider
            v-model="planForm.progress"
            :min="0"
            :max="100"
            :step="5"
            show-input
          />
        </el-form-item>
        
        <el-form-item label="预计完成" prop="dueDate">
          <el-date-picker
            v-model="planForm.dueDate"
            type="date"
            placeholder="选择预计完成日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item label="标签" prop="tags">
          <el-select
            v-model="planForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请输入标签，回车确认"
          >
            <el-option
              v-for="tag in availableTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="详细内容" prop="content">
          <el-input
            v-model="planForm.content"
            type="textarea"
            :rows="10"
            placeholder="请输入计划详细内容，支持HTML格式"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitPlanForm">确认</el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 添加更新记录对话框 -->
    <el-dialog
      v-model="updateRecordVisible"
      title="添加更新记录"
      width="500px"
    >
      <el-form :model="recordForm" ref="recordFormRef" :rules="recordRules" label-width="100px">
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="recordForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入更新记录内容"
          />
        </el-form-item>
        
        <el-form-item label="类型" prop="type">
          <el-select v-model="recordForm.type" placeholder="请选择记录类型">
            <el-option label="功能更新" value="primary" />
            <el-option label="Bug修复" value="warning" />
            <el-option label="其他" value="info" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="updateRecordVisible = false">取消</el-button>
          <el-button type="primary" @click="submitRecordForm">确认</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, reactive } from 'vue'
import { Calendar, Clock, Star, StarFilled, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { UpdatePlanAPI } from '../api'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)
const isAdmin = computed(() => userStore.getIsAdmin)

// 状态
const loading = ref(true)
const activeTab = ref('all')
const plans = ref<any[]>([])
const filteredPlans = ref<any[]>([])
const searchQuery = ref('')
const sortOption = ref('date')
const currentPage = ref(1)
const pageSize = ref(10)
const totalPlans = ref(0)
const detailsVisible = ref(false)
const selectedPlan = ref<any>(null)

// 编辑相关状态
const editDialogVisible = ref(false)
const isEditing = ref(false)
const planFormRef = ref<FormInstance>()
const planForm = reactive({
  id: 0,
  title: '',
  description: '',
  status: 'planned' as 'planned' | 'inProgress' | 'completed',
  progress: 0,
  dueDate: '',
  tags: [] as string[],
  content: ''
})

// 更新记录相关状态
const updateRecordVisible = ref(false)
const recordFormRef = ref<FormInstance>()
const recordForm = reactive({
  planId: 0,
  content: '',
  type: 'primary'
})

// 表单验证规则
const planRules = reactive<FormRules>({
  title: [
    { required: true, message: '请输入计划标题', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入计划描述', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择计划状态', trigger: 'change' }
  ],
  progress: [
    { required: true, message: '请设置完成进度', trigger: 'change' }
  ]
})

const recordRules = reactive<FormRules>({
  content: [
    { required: true, message: '请输入更新记录内容', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择记录类型', trigger: 'change' }
  ]
})

// 可用标签列表（可从已有计划中提取）
const availableTags = computed(() => {
  const tags = new Set<string>()
  plans.value.forEach(plan => {
    if (plan.tags && Array.isArray(plan.tags)) {
      plan.tags.forEach((tag: string) => tags.add(tag))
    }
  })
  return Array.from(tags)
})

// 获取更新计划列表
const fetchPlans = async () => {
  loading.value = true
  try {
    // 创建符合后端参数结构的请求对象
    const params = {
      status: activeTab.value === 'all' ? '' : activeTab.value,
      page: currentPage.value,
      pageSize: pageSize.value,
      // 显式设置sort参数
      sort: sortOption.value
    }
    
    const res = await UpdatePlanAPI.getUpdatePlans(params)
    if (res.code === 200) {
      plans.value = res.rows.map((plan: any) => ({
        ...plan,
        // 确保tags是数组格式
        tags: typeof plan.tags === 'string' ? 
          (plan.tags ? plan.tags.split(',') : []) : 
          (plan.tags || [])
      }))
      totalPlans.value = res.total
      filterPlans()
    } else {
      ElMessage.error(res.msg || '获取更新计划失败')
    }
  } catch (error) {
    console.error('获取更新计划失败', error)
    ElMessage.error('获取更新计划失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 筛选计划
const filterPlans = () => {
  if (!searchQuery.value) {
    filteredPlans.value = [...plans.value]
    return
  }
  
  const query = searchQuery.value.toLowerCase()
  filteredPlans.value = plans.value.filter(plan => 
    plan.title.toLowerCase().includes(query) || 
    plan.description.toLowerCase().includes(query) ||
    (plan.tags && plan.tags.some((tag: string) => tag.toLowerCase().includes(query)))
  )
}

// 排序计划
const sortPlans = () => {
  // 当排序选项变化时，重新获取服务器数据
  fetchPlans()
  
  // 同时也对本地数据进行排序（如果需要的话）
  const sorted = [...filteredPlans.value]
  
  if (sortOption.value === 'date') {
    sorted.sort((a, b) => new Date(b.createTime).getTime() - new Date(a.createTime).getTime())
  } else if (sortOption.value === 'dueDate') {
    sorted.sort((a, b) => new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime())
  }
  
  filteredPlans.value = sorted
}

// 显示计划详情
const showPlanDetails = async (plan: any) => {
  selectedPlan.value = plan
  
  // 如果需要，可以在这里加载更详细的计划信息
  try {
    const res = await UpdatePlanAPI.getUpdatePlanDetail(plan.id)
    if (res.code === 200) {
      // 处理tags格式，确保是数组
      const detailData = {
        ...res.data,
        tags: typeof res.data.tags === 'string' ? 
          (res.data.tags ? res.data.tags.split(',') : []) : 
          (res.data.tags || [])
      }
      
      selectedPlan.value = {
        ...plan,
        ...detailData
      }
    }
  } catch (error) {
    console.error('获取计划详情失败', error)
  }
  
  detailsVisible.value = true
}

// 显示添加计划对话框
const showAddPlanDialog = () => {
  isEditing.value = false
  resetPlanForm()
  editDialogVisible.value = true
}

// 显示编辑计划对话框
const showEditPlanDialog = (plan: any) => {
  isEditing.value = true
  resetPlanForm()
  
  // 填充表单数据
  planForm.id = plan.id
  planForm.title = plan.title
  planForm.description = plan.description
  planForm.status = plan.status
  planForm.progress = plan.progress
  planForm.dueDate = plan.dueDate
  
  // 处理tags，确保是数组
  if (typeof plan.tags === 'string') {
    planForm.tags = plan.tags ? plan.tags.split(',') : []
  } else {
    planForm.tags = Array.isArray(plan.tags) ? [...plan.tags] : []
  }
  
  planForm.content = plan.content || ''
  
  editDialogVisible.value = true
}

// 确认删除计划
const confirmDeletePlan = (plan: any) => {
  ElMessageBox.confirm(
    `确定要删除更新计划"${plan.title}"吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    deletePlan(plan.id)
  }).catch(() => {
    // 用户取消删除
  })
}

// 删除计划
const deletePlan = async (id: number) => {
  try {
    const res = await UpdatePlanAPI.deleteUpdatePlan(id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      
      // 关闭详情对话框（如果打开的是当前删除的计划）
      if (selectedPlan.value && selectedPlan.value.id === id) {
        detailsVisible.value = false
      }
      
      // 重新获取计划列表
      fetchPlans()
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch (error) {
    console.error('删除计划失败', error)
    ElMessage.error('删除失败，请稍后重试')
  }
}

// 重置计划表单
const resetPlanForm = () => {
  planForm.id = 0
  planForm.title = ''
  planForm.description = ''
  planForm.status = 'planned'
  planForm.progress = 0
  planForm.dueDate = ''
  planForm.tags = []
  planForm.content = ''
  
  // 如果表单实例存在，重置验证状态
  if (planFormRef.value) {
    planFormRef.value.resetFields()
  }
}

// 提交计划表单
const submitPlanForm = async () => {
  if (!planFormRef.value) return
  
  await planFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        // 创建API可接受的数据对象
        const apiData: Partial<UpdatePlanAPI.UpdatePlan> = {
          id: planForm.id,
          title: planForm.title,
          description: planForm.description,
          status: planForm.status,
          progress: planForm.progress,
          dueDate: planForm.dueDate,
          content: planForm.content,
          // 将tags数组转换为逗号分隔的字符串
          tags: Array.isArray(planForm.tags) ? planForm.tags.join(',') : ''
        }
        
        let res
        if (isEditing.value) {
          // 编辑现有计划
          res = await UpdatePlanAPI.updateUpdatePlan(apiData)
        } else {
          // 添加新计划
          res = await UpdatePlanAPI.addUpdatePlan(apiData)
        }
        
        if (res.code === 200) {
          ElMessage.success(isEditing.value ? '更新成功' : '添加成功')
          editDialogVisible.value = false
          fetchPlans()
        } else {
          ElMessage.error(res.msg || (isEditing.value ? '更新失败' : '添加失败'))
        }
      } catch (error) {
        console.error(isEditing.value ? '更新计划失败' : '添加计划失败', error)
        ElMessage.error(isEditing.value ? '更新失败，请稍后重试' : '添加失败，请稍后重试')
      }
    }
  })
}

// 显示添加更新记录对话框
const showAddUpdateRecordDialog = (planId: number) => {
  recordForm.planId = planId
  recordForm.content = ''
  recordForm.type = 'primary'
  
  if (recordFormRef.value) {
    recordFormRef.value.resetFields()
  }
  
  updateRecordVisible.value = true
}

// 提交更新记录表单
const submitRecordForm = async () => {
  if (!recordFormRef.value) return
  
  await recordFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        const res = await UpdatePlanAPI.addUpdateRecord(recordForm)
        
        if (res.code === 200) {
          ElMessage.success('添加更新记录成功')
          updateRecordVisible.value = false
          
          // 重新加载计划详情，以显示新添加的记录
          if (selectedPlan.value) {
            showPlanDetails(selectedPlan.value)
          }
        } else {
          ElMessage.error(res.msg || '添加更新记录失败')
        }
      } catch (error) {
        console.error('添加更新记录失败', error)
        ElMessage.error('添加更新记录失败，请稍后重试')
      }
    }
  })
}

// 获取状态样式
const getStatusType = (status: string) => {
  switch (status) {
    case 'inProgress':
      return 'primary'
    case 'completed':
      return 'success'
    case 'planned':
      return 'info'
    default:
      return 'info'
  }
}

// 获取状态文本
const getStatusText = (status: string) => {
  switch (status) {
    case 'inProgress':
      return '进行中'
    case 'completed':
      return '已完成'
    case 'planned':
      return '计划中'
    default:
      return '未知'
  }
}

// 获取进度状态
const getProgressStatus = (progress: number) => {
  if (progress === 100) return 'success'
  if (progress >= 80) return 'success'
  if (progress >= 50) return ''
  return 'warning'
}

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '未设置'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

// 分页处理
const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchPlans()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  fetchPlans()
}

// 监听标签页切换
watch(activeTab, () => {
  currentPage.value = 1
  fetchPlans()
})

// 监听排序选项变化
watch(sortOption, () => {
  if (plans.value.length > 0) {
    fetchPlans()
  }
})

// 初始化
onMounted(() => {
  fetchPlans()
})
</script>

<style scoped lang="scss">
.update-plans-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 60px - 40px);
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    
    .page-title {
      font-size: 28px;
      color: #303133;
      margin: 0;
    }
  }
  
  .filter-sort-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 20px 0;
    
    .search-bar {
      width: 300px;
    }
  }
  
  .loading-container {
    padding: 20px;
  }
  
  .empty-state {
    margin: 40px 0;
    text-align: center;
  }
  
  .plans-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
    
    .plan-card {
      height: 100%;
      display: flex;
      flex-direction: column;
      
      .plan-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 15px;
        
        .plan-title {
          font-size: 18px;
          font-weight: 600;
          margin: 0;
          flex: 1;
        }
      }
      
      .plan-content {
        flex: 1;
        
        .plan-description {
          color: #606266;
          margin-bottom: 15px;
          display: -webkit-box;
          -webkit-line-clamp: 3;
          -webkit-box-orient: vertical;
          overflow: hidden;
          line-height: 1.6;
        }
        
        .plan-progress {
          margin-bottom: 15px;
          
          .progress-text {
            display: block;
            margin-bottom: 5px;
            color: #606266;
          }
        }
        
        .plan-meta {
          margin-top: 15px;
          
          .plan-dates {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 10px;
            
            .date-item {
              display: flex;
              align-items: center;
              gap: 5px;
              color: #909399;
              font-size: 14px;
            }
          }
          
          .plan-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
          }
        }
      }
      
      .plan-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
        
        .admin-actions {
          display: flex;
          gap: 10px;
        }
      }
    }
  }
  
  .pagination-container {
    display: flex;
    justify-content: center;
    margin-top: 30px;
  }
  
  // 详情样式
  .plan-details {
    .plan-title {
      font-size: 22px;
      margin-bottom: 15px;
    }
    
    .details-meta {
      display: flex;
      gap: 15px;
      margin-bottom: 20px;
      align-items: center;
      flex-wrap: wrap;
      
      .details-date {
        color: #909399;
        font-size: 14px;
      }
    }
    
    .details-progress {
      margin-bottom: 25px;
      
      .progress-text {
        display: block;
        margin-bottom: 5px;
      }
    }
    
    .details-section {
      margin-bottom: 25px;
      
      h3 {
        font-size: 16px;
        margin-bottom: 10px;
        color: #303133;
        font-weight: 600;
      }
      
      p {
        color: #606266;
        line-height: 1.6;
      }
    }
    
    .details-tags {
      margin-top: 20px;
      
      h3 {
        font-size: 16px;
        margin-bottom: 10px;
      }
      
      .tag-item {
        margin-right: 8px;
        margin-bottom: 8px;
      }
    }
  }
  
  // 编辑表单样式
  .el-form {
    .el-form-item {
      margin-bottom: 20px;
    }
  }
  
  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }
}
</style> 