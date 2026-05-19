/* eslint-disable */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module '*.svg'
declare module '*.png'
declare module '*.jpg'
declare module '*.jpeg'
declare module '*.gif'
declare module '*.bmp'
declare module '*.tiff'

// 声明Element Plus中文语言包
declare module 'element-plus/dist/locale/zh-cn.mjs' {
  const zhCn: {
    name: string;
    el: Record<string, any>;
  };
  
  export default zhCn;
} 