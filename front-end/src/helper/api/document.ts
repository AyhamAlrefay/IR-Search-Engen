import request from '@/helper/utils/axios'

// document search
export const documentSearch = (params: Object, body: Object) =>
    request({
        url: '/search',
        method: 'post',
        data: body,
        params
    })

// guess your like
export const getSuggestion = (params: Object, body: Object) =>
    request({
        url: '/query-suggestion',
        method: 'post',
        data: body,
        params
    })
