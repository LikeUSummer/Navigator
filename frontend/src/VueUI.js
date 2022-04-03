import SideBar from "./components/SidebarPlugin"

import VueMaterial from "vue-material"
import "vue-material/dist/vue-material.css"
import 'vue-material/dist/theme/default.css'
import "./assets/scss/material-dashboard.scss"
import "es6-promise/auto"

export default {
  install(Vue) {
    Vue.use(SideBar)
    Vue.use(VueMaterial)
  }
}
