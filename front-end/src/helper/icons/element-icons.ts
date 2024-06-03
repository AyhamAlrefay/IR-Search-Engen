import type { App } from 'vue'
import * as icons from '@element-plus/icons-vue'
export default {
  install: (app: App<Element>) => {
    for (const [key, component] of Object.entries(icons)) {
      app.component(key, component)
    }
  }
}
