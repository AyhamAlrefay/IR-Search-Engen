import request from '@/helper/utils/axios'

// document search
export const documentSearch = (params: Object) =>
  request({
    url: '/search',
    method: 'get',
    params
  })

// guess your like
export const guessYourLike = (params: Object) =>
  request({
    url: '/get_guess_you_like',
    method: 'get',
    params
  })
