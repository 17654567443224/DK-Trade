<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2 class="card-header">登录</h2>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="验证码" prop="code" v-if="captchaEnabled">
          <div class="captcha-container">
            <el-input
              v-model="loginForm.code"
              placeholder="请输入验证码"
              :prefix-icon="Key"
            />
            <img 
              class="captcha-img" 
              :src="captchaImg" 
              @click="refreshCaptcha"
              alt="验证码"
            />
          </div>
        </el-form-item>
        
        <div class="form-actions">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <el-link type="primary" @click="forgotPassword">忘记密码？</el-link>
        </div>
        
        <el-button
          type="primary"
          native-type="submit"
          :loading="loading"
          class="submit-btn"
        >
          登录
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, Key } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'
import { AuthAPI } from '../api'

const router = useRouter()
const userStore = useUserStore()

const loginForm = ref({
  username: '',
  password: '',
  code: '',
  uuid: ''
})

const rememberMe = ref(false)
const loading = ref(false)
const captchaEnabled = ref(false)
const captchaImg = ref('')

// 获取验证码
const getCaptcha = async () => {
  try {
    console.log('正在获取验证码...')
    const res = await AuthAPI.getCaptchaImage()
    console.log('验证码响应:', res)
    captchaEnabled.value = res.captchaEnabled
    if (captchaEnabled.value) {
      captchaImg.value = 'data:image/jpeg;base64,' + res.img
      loginForm.value.uuid = res.uuid
    }
  } catch (error: any) {
    console.error('获取验证码失败', error)
    if (error.response) {
      console.error('错误状态:', error.response.status)
      console.error('错误数据:', error.response.data)
    }
    ElMessage.error(`验证码获取失败: ${error.message || '未知错误'}`)
    // 验证码获取失败时，允许用户尝试不使用验证码登录
    captchaEnabled.value = false
  }
}

// 刷新验证码
const refreshCaptcha = () => {
  getCaptcha()
}

// 页面加载时获取验证码
onMounted(() => {
  getCaptcha()
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' }
  ]
}

const loginFormRef = ref<any>(null)

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true
      try {
        // 调用登录API
        const res = await AuthAPI.login({
          username: loginForm.value.username,
          password: loginForm.value.password,
          code: loginForm.value.code,
          uuid: loginForm.value.uuid
        })
        
        // 存储token
        userStore.setToken(res.token)
        
        // 检查并存储管理员状态
        if (res.admin !== undefined) {
          userStore.setAdmin(res.admin)
        }
        
        ElMessage.success('登录成功')
        
        // 如果有重定向地址，则跳转到重定向地址
        const redirect = router.currentRoute.value.query.redirect as string
        router.push(redirect || '/')
      } catch (error) {
        ElMessage.error('登录失败，请检查用户名、密码和验证码')
        // 刷新验证码
        refreshCaptcha()
      } finally {
        loading.value = false
      }
    }
  })
}

const forgotPassword = () => {
  ElMessage.info('密码重置功能开发中')
}
</script>

<style scoped lang="scss">
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  
  .login-card {
    width: 100%;
    max-width: 400px;
    
    .card-header {
      text-align: center;
      margin: 0;
      font-size: 24px;
      color: #303133;
    }
    
    .captcha-container {
      display: flex;
      align-items: center;
      
      .el-input {
        margin-right: 10px;
        flex: 1;
      }
      
      .captcha-img {
        height: 40px;
        cursor: pointer;
      }
    }
    
    .form-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    
    .submit-btn {
      width: 100%;
      margin-bottom: 20px;
    }
  }
}
</style> 