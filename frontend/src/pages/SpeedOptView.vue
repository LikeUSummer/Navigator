<template>
  <md-card style="margin-top: 0">
    <md-card-content>
      <div class="md-layout">
        <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-66">
          <nav-map
            :info="prompt"
            :loc="xy2LatLng(state)"
            :path_pre="
              points.map((p) => {
                return xy2LatLng(p)
              })"
            :path_plan="
              path.map((p) => {
                return xy2LatLng(p)
              })"
            @updatePath="updatePath"></nav-map>
          <div class="md-layout">
            <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
              <data-chart :title="'主机转速'" :values="rot_data" color="default"></data-chart>
            </div>
            <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
              <data-chart :title="'主机油耗'" :values="oil_data" color="orange"></data-chart>
            </div>
            <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-80">
              <md-field>
                <label>请输入规划路径的节点坐标，可使用任意符号分隔</label>
                <md-textarea v-model="path_input"></md-textarea>
              </md-field>
            </div>
            <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-20">
              <div>
                <md-button class="md-primary" @click="start()">启动优化</md-button>
                <md-button class="md-primary" @click="stop()">停止</md-button>
              </div>
            </div>
          </div>
        </div>
        <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-33">
          <data-chart :title="'缆绳角度'" :values="angle_data" color="green"></data-chart>
          <data-chart :title="'缆绳拉力'" :values="force_data" color="red"></data-chart>
          <data-chart :title="'对水航速'" :values="speed_data"></data-chart>
        </div>
      </div>
    </md-card-content>
  </md-card>
</template>

<script>
import NavMap from "@/pages/Tug/NavMap.vue"
import { ResultCard, DataChart } from "@/components"
//let {request_get} = require("@/req.js")
export default {
  components: {
    ResultCard,
    DataChart,
    NavMap,
  },
  async created() {
    let t = 0
    setInterval(async () => {
      //从数据服务端获取传感器数据
      // let r = await this.$request_get("http://127.0.0.1:9876/data")
      // if(r.status!=200)
      //   return
      // r = JSON.parse(r)
      //根据当前数据服务端可提供的传感器信息，解开下面的部分注释
      // this.force_data = this.force_data.slice(1).concat([r.force]) // 拉力
      // this.angle_data = this.angle_data.slice(1).concat([r.angle]) // 缆绳角度
      // this.oil_data = this.oil_data.slice(1).concat([r.oil_temp]) // 油温
      // this.rot_data = this.rot_data.slice(1).concat([r.engine_rot]) // 转速
      // this.speed_data = this.speed_data.slice(1).concat([r.speed]) // 航速
      // this.state[0] = r.loc[1] // 坐标x-经度
      // this.state[1] = r.loc[0] // 坐标y-纬度
      // this.state[2] = r.heading // 航向
      // this.state[3] = r.speed*Math.cos(r.heading*Math.PI/180) // 速度分量x，请根据角度参考方向调整
      // this.state[4] = r.speed*Math.sin(r.heading*Math.PI/180) // 速度分量y，请根据角度参考方向调整

      //模拟数据
      this.force_data = this.force_data
        .slice(1)
        .concat([1200 + 100 * Math.sin(0.3 * t) + 10 * Math.random()]) // 拉力
      this.angle_data = this.angle_data
        .slice(1)
        .concat([20 + 3 * Math.cos(0.5 * t) + Math.random()]) // 缆绳角度
      this.oil_data = this.oil_data
        .slice(1)
        .concat([1.5 + 0.3 * Math.cos(t) + 0.2 * Math.random()]) // 油温
      this.rot_data = this.rot_data
        .slice(1)
        .concat([60 + 5 * Math.cos(1.2 * t) + 2 * Math.random()]) // 主机转速
      this.copy_json(this.state, this.state_pre) // 以预期状态作为当前状态进行仿真运动
      this.speed_data = this.speed_data
        .slice(1)
        .concat([this.norm2(this.state.slice(3, 5))]) // 以推荐航速作为当前航速
      t = (t + 1) % this.path.length
    }, 1000) // 修改此毫秒值以设置采样周期
  },
  data() {
    return {
      state: [5, 5, 0, 0.8, 0, 0], // 船舶实际状态
      state_pre: [5, 5, 0, 0.8, 0, 0], // 下一步预期状态
      speed_data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 航速传感器数据序列
      force_data: [1200, 1250, 1210, 1300, 1320, 1350, 1290, 1280, 1250, 1200], // 拉力传感器数据序列
      angle_data: [15, 15.8, 16.3, 16.8, 17.5, 17.9, 18.3, 18.8, 19.2, 19.5], // 缆绳角度传感器数据序列
      oil_data: [1.1, 1.15, 1.19, 1.21, 1.22, 1.25, 1.28, 1.31, 1.32, 1.3], // 油耗传感器数据序列
      rot_data: [60, 62, 65.5, 66, 64, 63.5, 61, 59, 57, 61], // 主机转速传感器数据序列

      path_input:
        "30.66424N，122.11958E\n30.66424N，122.31958E\n30.86424N，122.56958E", // 用户输入的规划航迹
      path: [ // 解析后的规划航迹坐标序列
        [0, 0],
        [40, 0],
        [90, 40]
      ],
      points: [], // 预测航迹坐标序列
      timer_handle: null, // 计算定时器
    }
  },
  computed: {
    prompt() {
      let realSpeed = this.speed_data[9].toFixed(4)
      let expSpeed = this.norm2(this.state_pre.slice(3, 5)).toFixed(4)
      let pos = this.loc2text(this.state)
      return `推荐航速<b>${expSpeed}</b>(knots)&nbsp&nbsp当前航速<b>${realSpeed}</b>(knots)&nbsp&nbsp当前位置<b>${pos}</b>`
    },
  },
  methods: {
    norm2(p) {
      return Math.sqrt(p[0] * p[0] + p[1] * p[1])
    },
    distance(p1, p2) {
      return this.norm2([p1[0] - p2[0], p1[1] - p2[1]])
    },
    xy2LatLng: function (xy) {
      return [xy[1] / 200 + 30.6642421, xy[0] / 200 + 122.11958238]
    },
    LatLng2xy: function (LatLng) {
      return [
        (LatLng[1] - 122.11958238) * 200,
        (LatLng[0] - 30.6642421) * 200,
      ]
    },
    loc2text: function (p) {
      let pos = this.xy2LatLng(p)
      return pos[0].toFixed(5) + "," + pos[1].toFixed(5)
    },
    copy_json(dst, src) {
      for (let k in src) {
        if (typeof src[k] == "Array" || typeof src[k] == "Object") {
          copy_json(dst[k], src[k])
        }
        else {
          this.$set(dst, k, src[k])
        }
      }
    },
    updatePath(path) {
      this.path = path.map((x) => {
        return [(x[1] - 122.11958238) * 200, (x[0] - 30.6642421) * 200]
      })
      this.path_input = path.join("\n")
    },
    async start() {
      // 解析用户输入的路径坐标序列，转换为数组
      let mat = this.path_input.match(/-?\d+\.?\d*/g)
      if (!mat || mat.length % 2) {
        alert("请按提示输入规范的坐标序列")
        return
      }
      this.path.splice(0, this.path.length)
      for (let i = 0; i < mat.length / 2; i++) {
        this.path.push(
          this.LatLng2xy([Number(mat[2 * i]), Number(mat[2 * i + 1])])
        )
      }

      // 检查计算实例是否存在
      if (this.$CSID == null) {
        let r = await this.$add({})
        if (r.status != 0) {
          return
        }
      }

      // 设置计算实例的规划航迹
      let r = await this.$modify({ rough_path: this.path })
      if (r.status == -1) {
        return
      }
      if (r.status == 1) {
        let s = await this.$add({})
        if (s.status != 0) {
          return
        }
        r = await this.$modify({ rough_path: this.path })
        if (r.status) {
          return
        }
      }

      // 启动优化计算定时器
      let err_counter = 0 // 记录连续请求错误次数
      this.timer_handle = setInterval(async () => {
        if (this.distance(this.state, this.path[this.path.length - 1]) > 2) {
          let r = await this.$update({ state: this.state })
          if (r.status != 0) {
            err_counter++
            if (r.status == 1 || err_counter > 10) {
              clearInterval(this.timer_handle)
              this.$CSID = null
              if (r.status == 1) {
                alert("计算实例丢失，服务端可能重启，请重新启动计算")
              }
              if (err_counter > 10) {
                alert("计算服务连续多次未响应，请检查计算服务端是否正常运行")
              }
            }
            return
          } else {
            err_counter = 0
          }
          // 短期预测轨迹
          this.copy_json(this.points, r.points)
          // 下一步预期状态
          this.state_pre = r.state
          // 也可以模拟实际驾驶情况，将预期状态做扰动后作为实际转移状态
          // this.state[0] += 0.1 * (Math.random() - 0.5)
          // this.state[1] += 0.1 * (Math.random() - 0.5)
          // this.state[3] += 0.2 * (Math.random() - 0.5)
          // this.state[4] += 0.2 * (Math.random() - 0.5)
        } else {
          // await this.$request_get("http://127.0.0.1:6789/delete?id=" + this.id)
          clearInterval(this.timer_handle)
        }
      }, 1000) // 修改此值改变优化计算周期，单位是毫秒
    },
    async stop() {
      // await this.$request_get("http://127.0.0.1:6789/delete?id=" + this.id)
      clearInterval(this.timer_handle)
    },
  },
}
</script>
