import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    // 浏览器请求 /api/... 时，Vite 转发给 FastAPI。
    // 对浏览器而言，请求仍然来自同一个地址，所以开发时不需要配置跨域。
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
