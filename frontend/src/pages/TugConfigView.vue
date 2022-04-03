<template>
  <div class="content">
    <tug-form :ship="ship"></tug-form>
    <engine-form :ship="ship"></engine-form>
    <md-toolbar class="md-transparent">
      <span class="md-title">参数示意图</span>
    </md-toolbar>
    <img src="@/assets/img/tug.jpg" alt="People">
  </div>
</template>

<script>
import TugForm from "@/pages/Tug/TugForm.vue";
import EngineForm from "@/pages/Tug/EngineForm.vue"

export default {
  components: {
    TugForm,
    EngineForm
  },
  data() {
    return {
      ship: {
        length: 60,
        width: 12,
        phy_center:[1, 2, 3],
        geo_center:[2, 3, 4],
        engine_type:["MAN S35ME-B9-EGRBP","MAN S35ME-B9-HPSCR"],
        power:[1000, 1000],
        reduction:[3.2, 3.2],
        engine_eigen:[[0.1, 0.2, 0.5],[0.1, 0.2, 0.5]],
        engine_loc:[[30, -5, -2], [30, 5, -2]],
        berth_num: 66,
        port_num: 3,
        tug_num: 10,
        tug_config_file:"./config.json",
        tug_wait_time:25, // 等待时间
        tug_turn_time:10, // 任务衔接时间
        tug_release_time:5, // 提前释放时间
        tug_work_time_max:6000, // 最长工作时间
        tug_arrive_time_win:"16:30-17:30" // 到达时间窗
      } 
    };
  }
};
</script>
