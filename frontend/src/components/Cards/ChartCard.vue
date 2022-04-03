<template>
  <md-card>
    <md-card-header class="card-chart" :data-background-color="dataBackgroundColor">
      <div :id="chartId" class="ct-chart" :trigger="trigger"></div>
    </md-card-header>

    <md-card-content>
      <slot name="content"></slot>
    </md-card-content>

    <md-card-actions md-alignment="left">
      <slot name="footer"></slot>
    </md-card-actions>
  </md-card>
</template>

<script>
  export default {
    name: "chart-card",
    props: {
      footerText: {
        type: String,
        default: ""
      },
      headerTitle: {
        type: String,
        default: "Chart title"
      },
      chartType: {
        type: String,
        default: "Line" // Line | Pie | Bar
      },
      chartOptions: {
        type: Object,
        default: () => {
          return {}
        }
      },
      chartResponsiveOptions: {
        type: Array,
        default: () => {
          return []
        }
      },
      chartData: {
        type: Object,
        default: () => {
          return {
            labels: [],
            series: []
          }
        }
      },
      dataBackgroundColor: {
        type: String,
        default: ""
      }
    },
    data() {
      return {
        chartId: "no-id",
        chart: null // 记录Chartist对象
      }
    },
    computed: {
      // 利用 computed 机制让图表内容可动态更新
      trigger: function () {
        let min = Math.min.apply(null, this.chartData.series[0])
        let max = Math.max.apply(null, this.chartData.series[0])
        this.chartOptions.low = min
        this.chartOptions.high = max
        if (this.chart)
          this.chart.update(this.chartData, this.chartOptions)
        return ""
      }
    },
    created() {
      this.chartId = this.uuid()
      import("chartist").then(Chartist => {
        let ChartistLib = Chartist.default || Chartist
        this.$nextTick(() => {
          let chartIdQuery = `#${this.chartId}`
          this.chart = ChartistLib[this.chartType](chartIdQuery, this.chartData, this.chartOptions)
        })
      })
    }
  }
</script>
