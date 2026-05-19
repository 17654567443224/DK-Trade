import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

// 预加载CreateStrategy视图
const CreateStrategyView = () => import(
  /* webpackChunkName: "create-strategy" */
  /* webpackPrefetch: true */
  '../views/CreateStrategy.vue'
)

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/strategy/:id',
    name: 'StrategyDetail',
    component: () => import('../views/StrategyDetail.vue'),
    meta: { title: '策略详情' }
  },
  {
    path: '/user',
    name: 'UserCenter',
    component: () => import('../views/UserCenter.vue'),
    meta: { title: '个人中心', requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/create-strategy',
    name: 'CreateStrategy',
    component: CreateStrategyView,
    meta: { title: '创建策略', requiresAuth: true }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue'),
    meta: { title: '关于我们' }
  },
  {
    path: '/update-plans',
    name: 'UpdatePlans',
    component: () => import('../views/UpdatePlans.vue'),
    meta: { title: '更新计划' }
  }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title} - 量化交易平台`
  
  // 检查是否需要登录权限
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查用户是否已登录
    const token = localStorage.getItem('token')
    if (!token) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router 