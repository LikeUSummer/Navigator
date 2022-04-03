<template>
    <chart-card
      :chart-data="points"
      :chart-type="'Line'"
      :data-background-color="color">
      <template slot="content">
        <h4 class="title">{{title}}</h4>
      </template>
      <template slot="footer">
        <div class="stats">
          <md-icon>access_time</md-icon>
          {{"当前值 "+values[values.length-1].toFixed(3)}}
        </div>
      </template>
    </chart-card>
</template>

<script>
import { ChartCard } from "@/components";
export default {
  components: {
    ChartCard
  },
  props: {
    title: String,
    values: Array,
    color:{
      type: String,
      default: 'blue'
    }
  },
  computed: {
    points: function() {
      return {
        labels:["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        series:[this.values]
      }
    }
  },
  data() {
    return {
      options: {
        lineSmooth: this.$Chartist.Interpolation.cardinal({
          tension: 0
        }),
        low: 0,
        high: 30,
        chartPadding: {
          top: 0,
          right: 0,
          bottom: 0,
          left: 0
        }
      }
    };
  }
};
</script>
