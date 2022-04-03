// 在本文件中添加Vue全局指令
import {
  directive as vClickOutside
} from "vue-clickaway"

const GlobalDirectives = {
  install(Vue) {
    Vue.directive("click-outside", vClickOutside)
  }
}

export default GlobalDirectives