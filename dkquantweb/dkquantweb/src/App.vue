<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from './stores/user'
import { Search, User, Message, Phone } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
// @ts-ignore
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import logoImage from './assets/logo.png'
import { AuthAPI } from './api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const searchQuery = ref('')

// 初始化用户信息
const initUserInfo = async () => {
  const token = localStorage.getItem('token')
  if (token) {
    userStore.setToken(token)
    
    try {
      // 获取用户信息和管理员状态，以静默模式调用API
      const userInfoRes = await AuthAPI.getUserInfo(true)
      
      if (userInfoRes.code === 200) {
        // 设置用户基本信息
        if (userInfoRes.data) {
          userStore.setUserInfo(userInfoRes.data)
        }
        
        // 从返回的数据中提取管理员状态，或从localStorage恢复
        if (userInfoRes.data && userInfoRes.data.admin !== undefined) {
          userStore.setAdmin(!!userInfoRes.data.admin)
        } else {
          // 如果获取管理员状态失败，从localStorage恢复
          const isAdmin = localStorage.getItem('isAdmin') === 'true'
          userStore.setAdmin(isAdmin)
        }
      } else {
        // 处理错误响应但不显示错误提示
        console.warn('获取用户信息返回非200状态码:', userInfoRes.code, userInfoRes.msg)
        
        // 从localStorage恢复
        const isAdmin = localStorage.getItem('isAdmin') === 'true'
        userStore.setAdmin(isAdmin)
      }
    } catch (error: any) {
      // 捕获错误但不显示错误提示
      console.error('获取用户信息失败', error)
      
      // 如果API调用失败，尝试从localStorage恢复
      const isAdmin = localStorage.getItem('isAdmin') === 'true'
      userStore.setAdmin(isAdmin)
      
      // 如果token无效，清除token并跳转到登录页面
      // 但不弹出错误提示框
      if (error.response && (error.response.status === 401 || error.response.status === 403)) {
        userStore.logout()
        // 避免无限循环跳转
        if (route.path !== '/login') {
          router.push('/login')
        }
      }
    }
  }
}

onMounted(() => {
  initUserInfo()
})

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/',
      query: { search: searchQuery.value }
    })
  }
}

const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/user')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      userStore.logout()
      router.push('/login')
      ElMessage.success('已退出登录')
      break
  }
}
</script>

<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-left">
        <router-link to="/" class="logo">
          <img :src="logoImage" alt="Logo" />
          <span>量化交易平台</span>
        </router-link>
        
        <el-menu
          mode="horizontal"
          :router="true"
          :default-active="route.path"
          class="nav-menu"
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/update-plans">更新计划</el-menu-item>
          <el-menu-item index="/about">关于我们</el-menu-item>
        </el-menu>
      </div>
      
      <div class="header-right">
        <el-input
          v-model="searchQuery"
          placeholder="搜索策略..."
          :prefix-icon="Search"
          class="search-input"
          @keyup.enter="handleSearch"
        />
        
        <template v-if="userStore.isLoggedIn">
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="32">
                <User />
              </el-avatar>
              <span class="username">用户</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="settings">账户设置</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" @click="$router.push('/login')">登录</el-button>
        </template>
      </div>
    </el-header>
    
    <!-- 主要内容区域 -->
    <el-main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>
    
    <!-- 页脚 -->
    <footer class="site-footer">
      <div class="footer-container">
        <div class="footer-content">
          <div class="footer-section">
            <h4>关于我们</h4>
            <p>专业的量化交易平台，为您提供全方位的量化投资解决方案。</p>
          </div>
          
          <div class="footer-section">
            <h4>联系方式</h4>
            <p>
              <el-icon><Message /></el-icon>
              <span>邮箱：cosm9629@gmail.com</span>
            </p>
            <p>
              <el-icon><Phone /></el-icon>
              <span>作者微信：i520Dark</span>
            </p>
          </div>
          
          <div class="footer-section">
            <h4>快速链接</h4>
            <div class="quick-links">
              <router-link to="/help" class="footer-link">帮助中心</router-link>
              <router-link to="/terms" class="footer-link">服务条款</router-link>
              <router-link to="/privacy" class="footer-link">隐私政策</router-link>
            </div>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>&copy; 2024 量化交易平台. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped lang="scss">
/* 全局样式重置，确保页面没有默认边距 */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  overflow-x: hidden;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
  overflow-x: hidden;
}

/* 为避免页脚宽度问题，使用更严格的方式设置页脚样式 */
.site-footer {
  background-color: #2c3e50;
  color: #fff;
  padding: 40px 20px 20px;
  width: 100%;
  box-sizing: border-box;
  position: relative;
  margin: 0;
  
  /* 这些样式可以确保页脚完全覆盖整个宽度 */
  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100vw;
    right: -100vw;
    bottom: 0;
    background-color: #2c3e50;
    z-index: -1;
  }
  
  .footer-container {
    max-width: 1200px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }
  
  .footer-content {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 40px;
    margin-bottom: 40px;
    
    @media (max-width: 768px) {
      grid-template-columns: 1fr;
      gap: 30px;
    }
    
    .footer-section {
      h4 {
        font-size: 18px;
        margin-bottom: 20px;
        color: #fff;
        position: relative;
        padding-bottom: 10px;
        
        &:after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 0;
          width: 40px;
          height: 2px;
          background-color: #409EFF;
        }
      }
      
      p {
        color: #b3c0d1;
        margin-bottom: 10px;
        line-height: 1.6;
        display: flex;
        align-items: center;
        gap: 8px;
        
        .el-icon {
          color: #409EFF;
        }
      }
      
      .quick-links {
        display: flex;
        flex-direction: column;
        gap: 10px;
        
        .footer-link {
          color: #b3c0d1;
          text-decoration: none;
          display: block;
          
          &:hover {
            color: #fff;
            transform: translateX(5px);
            transition: all 0.3s ease;
          }
        }
      }
    }
  }
  
  .footer-bottom {
    text-align: center;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    
    p {
      color: #b3c0d1;
      margin: 0;
    }
  }
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  
  .header-left {
    display: flex;
    align-items: center;
    
    .logo {
      display: flex;
      align-items: center;
      text-decoration: none;
      margin-right: 40px;
      
      img {
        height: 32px;
        margin-right: 10px;
      }
      
      span {
        font-size: 20px;
        font-weight: bold;
        color: #409EFF;
      }
    }
    
    .nav-menu {
      border-bottom: none;
    }
  }
  
  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .search-input {
      width: 200px;
    }
    
    .user-info {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      
      .username {
        color: #606266;
      }
    }
  }
}

.main-content {
  margin-top: 60px;
  flex: 1;
  background-color: #f5f7fa;
  padding: 20px;
  min-height: calc(100vh - 60px - 250px); /* 减去header和footer的高度 */
  overflow: visible;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
