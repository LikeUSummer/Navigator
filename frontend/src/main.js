// Vue 核心库
import Vue from "vue"
import VueRouter from "vue-router"
// 单页应用根组件
import App from "./App"
// 路由
import routes from "./routes/routes"
// 自定义全局组件和指令等
import VueUI from "./VueUI"
import GlobalComponents from "./globalComponents"
import GlobalDirectives from "./globalDirectives"
import Notifications from "./components/NotificationPlugin"
// 第三方插件
import Chartist from "chartist"
import BaiduMap from 'vue-baidu-map'

// 初始化与注册
const router = new VueRouter({
  routes, 
  linkExactActiveClass: "nav-item active"
})
Vue.use(BaiduMap, {ak: 'LpS8ai3sVgoorKoa1IylV3cgM2UMNBqd'}) // 百度地图
Vue.use(VueRouter)
Vue.use(VueUI)
Vue.use(GlobalComponents)
Vue.use(GlobalDirectives)
Vue.use(Notifications)

// 全局变量
Vue.prototype.$Chartist = Chartist
Vue.prototype.$CSID = null // 计算服务实例ID
Vue.prototype.$CSIP = "http://127.0.0.1:6789/" // 计算服务地址
Vue.prototype.$net_status = 0 // 全局网络请求状态

// 全局函数
Vue.prototype.uuid = function() {
  let d = new Date().getTime()
  if (window.performance && typeof window.performance.now === "function") {
    d += performance.now() // use high-precision timer if available
  }
  let uuid = 'idxxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    let r = (d + Math.random() * 16) % 16 | 0
    d = Math.floor(d / 16)
    return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16)
  })
  return uuid
}

function request_get(url) {
  return new Promise((resolve, reject) => {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', url, true)
    xhr.timeout = 3000
    xhr.send()
    xhr.onreadystatechange = ()=> {
      if(xhr.readyState == 4) {
        if(xhr.status == 200) {
          Vue.prototype.$net_status = 200
          resolve(xhr.responseText)
        } else { // 在这里我们不使用 reject 抛出网络异常，引用处用 $net_status 判定状态，可简化请求的编写
          Vue.prototype.$net_status = xhr.status
          resolve(new Error(xhr.status))
        }
      }
    }
  })
}
Vue.prototype.$request_get = request_get

function request_post(url, json) {
  return new Promise((resolve, reject) => {
    let xhr = new XMLHttpRequest()
    xhr.open('POST', url, true)
    xhr.timeout = 3000
    xhr.setRequestHeader("Content-type","application/json")
    xhr.send(JSON.stringify(json))
    xhr.onreadystatechange = () => {
      if(xhr.readyState == 4) {
        if(xhr.status == 200) {
          Vue.prototype.$net_status = 200
          resolve(xhr.responseText)
        } else {
          Vue.prototype.$net_status = xhr.status
          resolve(new Error(xhr.status))
        }
      }
    }
  })
}
Vue.prototype.$request_post = request_post

Vue.prototype.$json2url = function(json) {
  return Object.keys(json).map((key) => {
    return encodeURIComponent(key) + "=" + encodeURIComponent(json[key])
  }).join("&")
}

Vue.prototype.$add = async function(data) {
  let r = await request_post(Vue.prototype.$CSIP + "add", data)
  if(Vue.prototype.$net_status != 200) {
    alert("请求计算服务失败，请检查计算服务端是否正常运行或稍后重试")
    return {status : -1}
  }
  r = JSON.parse(r)
  Vue.prototype.$CSID = r.id// 获取计算实例的ID，后续计算请求将带上此参数
  return {status : 0}
}

Vue.prototype.$modify = async function(data) {
  data.id = Vue.prototype.$CSID
  let r = await request_post(Vue.prototype.$CSIP + "modify", data)
  if(this.$net_status != 200) {
    alert("请求计算服务失败，请检查计算服务端是否正常运行或稍后重试")
    return {status : -1}
  }
  r = JSON.parse(r)
  if(r.status == 0) {
    return {status : 0}
  }
  return r
}

Vue.prototype.$update = async function(data) {
  data.id = Vue.prototype.$CSID
  let r = await request_post(Vue.prototype.$CSIP + "update", data)
  if(this.$net_status != 200) {
    return {status : -1}
  }
  return JSON.parse(r)
}

Vue.prototype.$delete = async function() {
  await request_get(Vue.prototype.$CSIP + "add?id=" + Vue.prototype.$CSID)
}

new Vue({
  el: "#app",
  render: h => h(App),
  router,
  data: {
    Chartist: Chartist
  }
})
