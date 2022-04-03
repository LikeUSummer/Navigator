<template>
  <div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">
    <notifications></notifications>

    <side-bar
      :sidebar-item-color="sidebarBackground"
      :sidebar-background-image="sidebarBackgroundImage"
    >
      <sidebar-link to="/speed-opt">
        <md-icon>directions_boat</md-icon>
        <p>航速优化</p>
      </sidebar-link>
      <sidebar-link to="/tug-config">
        <md-icon>settings_input_component</md-icon>
        <p>拖轮参数设置</p>
      </sidebar-link>
      <sidebar-link to="/task-status">
        <md-icon>library_books</md-icon>
        <p>调度任务</p>
      </sidebar-link>
      <sidebar-link to="/task-config">
        <md-icon>dynamic_form</md-icon>
        <p>调度参数设置</p>
      </sidebar-link>
      <sidebar-link to="/about" class="active-pro">
        <md-icon>person</md-icon>
        <p>关于我们</p>
      </sidebar-link>
    </side-bar>

    <div class="main-panel">
      <main-content > </main-content>
      <content-footer></content-footer>
    </div>

  </div>
</template>

<script>
import ContentFooter from "./ContentFooter.vue";
import MainContent from "./MainContent.vue";

export default {
  components: {
    MainContent,
    ContentFooter
  },
  data() {
    return {
      sidebarBackground: "green",
      sidebarBackgroundImage: require("@/assets/img/sidebar-4.jpg")
    };
  }
};
</script>
