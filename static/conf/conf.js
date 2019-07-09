Vue.use(iview);
Vue.prototype.$copy = function (val) {
    return JSON.parse(JSON.stringify(val))
};
Vue.prototype.$apply = function (data) {
    return Object.assign({}, data, data);
};
axios.defaults.baseURL = site_url;
Vue.prototype.$http = axios;
axios.interceptors.response.use(response => {
    if (response.status !== 200) {
        return {
            code: response.status,
            message: '请求异常，请刷新重试',
            result: false
        }
    }
    return response.data
});
