import { defineStore } from 'pinia'

interface Strategy {
  id: number
  name: string
  description: string
  category: string
  author: string
  authorAvatar?: string
  isHot?: boolean
  status: 'running' | 'stopped' | 'error'
  performance: {
    annualReturn: number
    totalReturn: number
    maxDrawdown: number
    sharpeRatio: number
  }
  parameters: {
    stockSelection: Record<string, any>
    entry: Record<string, any>
    stopLoss: Record<string, any>
    position: Record<string, any>
  }
}

interface StrategyState {
  strategies: Strategy[]
  userStrategies: Strategy[]
  currentStrategy: Strategy | null
  categories: string[]
}

// 示例策略数据
const sampleStrategies: Strategy[] = [
  {
    id: 1,
    name: '均线突破策略',
    description: '基于均线交叉信号的趋势跟踪策略，适合中长期投资者。',
    category: '趋势跟踪',
    author: '量化大师',
    authorAvatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    isHot: true,
    status: 'running',
    performance: {
      annualReturn: 0.215,
      totalReturn: 0.876,
      maxDrawdown: 0.125,
      sharpeRatio: 1.85
    },
    parameters: {
      stockSelection: {},
      entry: {},
      stopLoss: {},
      position: {}
    }
  },
  {
    id: 2,
    name: '价值投资策略',
    description: '基于基本面分析的价值投资策略，寻找被低估的优质股票。',
    category: '价值投资',
    author: '巴菲特粉丝',
    authorAvatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    isHot: true,
    status: 'running',
    performance: {
      annualReturn: 0.185,
      totalReturn: 0.925,
      maxDrawdown: 0.145,
      sharpeRatio: 1.65
    },
    parameters: {
      stockSelection: {},
      entry: {},
      stopLoss: {},
      position: {}
    }
  },
  {
    id: 3,
    name: '日内波段交易',
    description: '利用日内价格波动进行高频交易，适合短线交易者。',
    category: '日内交易',
    author: '短线高手',
    authorAvatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    isHot: true,
    status: 'stopped',
    performance: {
      annualReturn: 0.325,
      totalReturn: 0.456,
      maxDrawdown: 0.225,
      sharpeRatio: 1.35
    },
    parameters: {
      stockSelection: {},
      entry: {},
      stopLoss: {},
      position: {}
    }
  },
  {
    id: 4,
    name: '期现套利策略',
    description: '利用期货与现货之间的价格差异进行无风险套利。',
    category: '套利策略',
    author: '套利达人',
    authorAvatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    isHot: true,
    status: 'running',
    performance: {
      annualReturn: 0.125,
      totalReturn: 0.356,
      maxDrawdown: 0.075,
      sharpeRatio: 2.15
    },
    parameters: {
      stockSelection: {},
      entry: {},
      stopLoss: {},
      position: {}
    }
  },
  {
    id: 5,
    name: '多因子选股策略',
    description: '结合多种因子进行选股，平衡风险与收益。',
    category: '量化对冲',
    author: '因子专家',
    authorAvatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    isHot: true,
    status: 'running',
    performance: {
      annualReturn: 0.175,
      totalReturn: 0.756,
      maxDrawdown: 0.115,
      sharpeRatio: 1.95
    },
    parameters: {
      stockSelection: {},
      entry: {},
      stopLoss: {},
      position: {}
    }
  },
  {
    id: 6,
    name: '网格交易策略',
    description: '在价格区间内设置网格，自动执行高抛低吸。',
    category: '趋势跟踪',
    author: '网格大师',
    authorAvatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    isHot: true,
    status: 'running',
    performance: {
      annualReturn: 0.195,
      totalReturn: 0.656,
      maxDrawdown: 0.135,
      sharpeRatio: 1.75
    },
    parameters: {
      stockSelection: {},
      entry: {},
      stopLoss: {},
      position: {}
    }
  }
];

export const useStrategyStore = defineStore('strategy', {
  state: (): StrategyState => ({
    strategies: sampleStrategies, // 使用示例数据
    userStrategies: [],
    currentStrategy: null,
    categories: ['趋势跟踪', '套利策略', '日内交易', '价值投资', '量化对冲']
  }),

  getters: {
    getStrategyById: (state) => {
      return (id: number) => state.strategies.find(s => s.id === id)
    },
    getUserStrategies: (state) => state.userStrategies,
    getCategories: (state) => state.categories
  },

  actions: {
    setStrategies(strategies: Strategy[]) {
      this.strategies = strategies
    },

    setUserStrategies(strategies: Strategy[]) {
      this.userStrategies = strategies
    },

    setCurrentStrategy(strategy: Strategy) {
      this.currentStrategy = strategy
    },

    addUserStrategy(strategy: Strategy) {
      this.userStrategies.push(strategy)
    },

    updateStrategyParameters(id: number, parameters: Strategy['parameters']) {
      const strategy = this.userStrategies.find(s => s.id === id)
      if (strategy) {
        strategy.parameters = parameters
      }
    },

    updateStrategyStatus(id: number, status: Strategy['status']) {
      const strategy = this.userStrategies.find(s => s.id === id)
      if (strategy) {
        strategy.status = status
      }
    }
  }
}) 