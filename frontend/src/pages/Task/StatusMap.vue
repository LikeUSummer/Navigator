<template>
  <div>
    <md-toolbar class="md-transparent">
      <span class="md-title">图例1</span>
      <md-avatar>
        <img src="@/assets/img/boat-run.png" alt="Avatar">
      </md-avatar>
      <span>工作中</span>
      <md-avatar>
        <img src="@/assets/img/boat-will.png" alt="Avatar">
      </md-avatar>
      <span>即将结束</span>
      <md-avatar>
        <img src="@/assets/img/boat-wait.png" alt="Avatar">
      </md-avatar>
      <span>等待中</span>
      <md-avatar>
        <img src="@/assets/img/boat-stop.png" alt="Avatar">
      </md-avatar>
      <span>无法使用</span>
      <md-avatar>
        <img src="@/assets/img/ship.png" alt="Avatar">
      </md-avatar>
      <span>被拖船舶</span>
    </md-toolbar>
    <baidu-map :center="center" :zoom="11" :scroll-wheel-zoom="true" class="bm-view">
      <bm-marker v-for="(v, k) in info" :key="k"
        :position="{lng: v.path[5][0] + 0.1, lat : v.path[5][1]}"
        :dragging="false"
        :icon="{url: require('@/assets/img/boat-' + v.status + '.png'),
          size: {width: 16, height: 16}}">
      </bm-marker>
      <bm-marker v-if="info[index].status == 'run'"
        :position="{lng: path[5].lng + 0.04, lat: path[5].lat + 0.03}"
        :dragging="false"
        :icon="{url: require('@/assets/img/ship.png'), size: {width: 32, height: 32}}">
      </bm-marker>
      <bm-polyline :path="path" stroke-color="blue"
        :stroke-opacity="0.5" :stroke-weight="2" :editing="false">
      </bm-polyline>
    </baidu-map>
  </div>
</template>

<script>
  export default {
    name: "status-map",
    props: {
      index: Number,
      info: Array
    },
    created() {

    },
    computed: {
      path: function () {
        let temp = [];
        for (let i = 0; i < this.info[this.index].path.length; i++) {
          let loc = {};
          loc.lng = this.info[this.index].path[i][0] + 0.1;
          loc.lat = this.info[this.index].path[i][1];
          temp.push(loc);
        }
        return temp;
      }
    },
    data() {
      return {
        pos: 0,
        center: {
          lng: 121.845001,
          lat: 31.154579
        }
      }
    },
  };
</script>

<style>
  .bm-view {
    width: 100%;
    height: 500px;
  }
</style>