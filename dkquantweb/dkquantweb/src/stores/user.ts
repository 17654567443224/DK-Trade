import { defineStore } from 'pinia'

interface UserState {
  token: string | null
  userInfo: {
    id: number
    username: string
    email: string
    balance: number
    avatar: string
  } | null
  isAdmin: boolean
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    token: localStorage.getItem('token'),
    userInfo: null,
    isAdmin: localStorage.getItem('isAdmin') === 'true'
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token,
    getUserInfo: (state) => state.userInfo,
    getIsAdmin: (state) => state.isAdmin
  },
  
  actions: {
    setToken(token: string) {
      this.token = token
      localStorage.setItem('token', token)
    },
    
    setUserInfo(userInfo: UserState['userInfo']) {
      this.userInfo = userInfo
    },
    
    setAdmin(isAdmin: boolean) {
      this.isAdmin = isAdmin
      localStorage.setItem('isAdmin', isAdmin.toString())
    },
    
    logout() {
      this.token = null
      this.userInfo = null
      this.isAdmin = false
      localStorage.removeItem('token')
      localStorage.removeItem('isAdmin')
    }
  }
}) 