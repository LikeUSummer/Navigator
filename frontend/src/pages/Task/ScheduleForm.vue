<template>
  <md-card>
    <md-card-header data-background-color="green">
        <h4 class="title">调度参数设置</h4>
    </md-card-header>
    <md-card-content>
      <div class="md-layout">
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>优先级设定 等待时间>=(min)</label>
            <md-input v-model="ship.tug_wait_time"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>任务衔接时间</label>
            <md-input v-model="ship.tug_turn_time"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>拖轮提前释放时间</label>
            <md-input v-model="ship.tug_release_time"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>拖轮最长工作时间</label>
            <md-input v-model="ship.tug_work_time_max"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-100">
          <md-field>
            <label>到达时间窗</label>
            <md-input v-model="ship.tug_arrive_time_win"></md-input>
          </md-field>
        </div>
      </div>
    </md-card-content>
  </md-card>  
        
</template>
<script>
export default {
  name: "ship-form",
  props: {
    ship: Object,
    dataBackgroundColor: {
      type: String,
      default: ""
    }
  },
  data() {
    return {}
  }
}
</script>
<style></style>
