import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementIcons from './helper/icons/element-icons'
import 'element-plus/theme-chalk/dark/css-vars.css'
import 'element-plus/theme-chalk/el-loading.css'
import 'element-plus/theme-chalk/el-message.css'

import './assets/style/main.css'

const app = createApp(App)

app.use(router)
app.use(ElementIcons)
app.mount('#app')
