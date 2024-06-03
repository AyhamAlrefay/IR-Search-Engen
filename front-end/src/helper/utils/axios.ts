import axios from 'axios'
import { ERROR_CODE_TYPE } from '@/helper/types/error-code-type'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: '/api',
  timeout: 60000
})


service.interceptors.request.use(
  config => {
    
    return config
  },
  err => {
    console.log(err)
    return Promise.reject(err)
  }
)

service.interceptors.response.use(
  res => {
    const CODE = res.data['code'] || 200
    if (CODE === 200) {
      return Promise.resolve(res.data)
    } else {
      const MSG =
        ERROR_CODE_TYPE(CODE) || res.data['msg'] || ERROR_CODE_TYPE('default')
      ElMessage.error(MSG)
      return Promise.reject(res.data)
    }
  },
  err => {
    console.log(err)
    let { message } = err
    if (message == 'Network Error') {
    } else if (message.includes('timeout')) {
      message = 'Time out'
    } else if (message.includes('Request failed with status code')) {
      message = `${message.substr(message.length - 3)}`
    }
    ElMessage.error({
      message: message,
      duration: 5 * 1000
    })
    return Promise.reject(err)
  }
)

export default service
