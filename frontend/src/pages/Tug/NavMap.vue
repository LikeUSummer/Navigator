<template>
  <div style="margin-bottom:20px;">
    <div id="navmap"></div>
  </div>
</template>

<script>
  import {SeaMap} from 'seamap/seamap.min.js'
  import 'seamap/seamap.min.css'
  export default {
    mounted() {
      let vue = this
      this.map = new SeaMap.Map('navmap', {
        zoom: 4,
        center: [34.44, 113.42],
        zoomAnimation: false,
        pmIgnore: false,
        attributionControl: false, // 是否显示版权控件
        showZoomIndicator: true,
        maxBounds: []
      })
      // 设置海图瓦片服务地址
      // 常见的商用地址：
      // 'http://218.28.185.236:9001/seamap/google/{z}/{y}/{x}.png'
      // 'http://112.126.96.159/Ship/Map?z={z}&y={y}&x={x}'
      // 默认使用本地建立的 WMS，请解压 map_tile_server.zip 并执行其中的脚本，即可启动一个测试用的地图瓦片服务
      let map_tile_url = 'http://127.0.0.1:8081/{z}/{x}/{y}.png'  
      SeaMap.tileLayer(map_tile_url, { // 添加瓦片图层
        detectRetina: true
      }).addTo(this.map)

      // 添加辅助控件
      // 比例尺控件
      SeaMap.control.scale({useUnitChinese: true}).addTo(this.map)
      // 鼠标位置控件
      SeaMap.control.mousePosition({position:'bottomright'}).addTo(this.map)
      // 全屏控件
      SeaMap.control.fullScreen({position:'bottomright'}).addTo(this.map)
      // 绘图控件
      this.map.pm.addControls({position: 'bottomright'})
      // 测量控件
      // SeaMap.measure({}).addTo(this.map)
      // 拉框缩放工具
      let boxZoom = SeaMap.Lib.boxZoom(this.map, {
        boxStyle: {
          lineStyle: 'dashed',
          lineWeight: 2,
          lineColor: '#14c4ba',
          fillColor: '#14c4ba',
          opacity: 0.5
        },
        autoClose: false
      })

      // 创建船舶图层
      new SeaMap.Service.CanvasShipService(this.map, {
        labelTextColor: '#1d374c',
        labelLineColor: 'rgba(255, 255, 255, 0.8)',
        labelLineFillColor: 'rgba(255, 255, 255, 0.8)',
        labelFont: '500 12px Arial'
      })
      // 当前视野内船舶数量监测控件
      SeaMap.control.zoomShipCount({}).addTo(this.map)
      // 创建船舶对象
      let ships = []
      this.ship = new SeaMap.CanvasShip({
        id: 'Summer2020', // 船舶ID
        mmsi: 20201215, // 编号
        callsign: 1000,
        lng: 121.91958238,
        lat: 31.0642421,
        type: 1,// 类型
        name: 'SummerEast', // 名称
        nameCN: '东方盛夏', // 中文名称
        width: 8, // 船宽
        length: 36, // 船长
        rotation: 30, // 旋转角度
        outOfChina: false, // 是否已离境
        sog: 8.71, // 航速
        rot: 5, // 转头速率
        // 船艏向
        hdg: 7,
        cog: 6,
        trail: 190,
        navistate: 0,
        isFollowing: true,
        state: 2,
        isAIS: true
      })
      ships.push(this.ship)
      this.map.shipService.addShips(ships) // 将船舶加入船舶图层管理器

      // 在创建连线完成后，发出更新航迹事件，通知父组件更新
      this.map.on('pm:create',(e) => {
        if(e.shape == 'Line') {
          vue.$emit('updatePath', e.layer.getLatLngs().map((x) => {
              return [x.lat,x.lng]
          }))
          e.layer.remove()
        }
      })
      // 处理绘图事件以协调船舶图层的显示
      this.map.on('pm:drawstart', (e) => {
        let shape = e.shape, workingLayer = e.workingLayer
        this.map.shipService && (this.map.shipService.setUnclickable(),
            this.map.shipService.setZIndex(399))
        let tooltip = workingLayer.getTooltip()
        if (tooltip) {
          tooltip.options.direction = 'top'
          if (shape === 'CircleMarker') {
            tooltip.options.offset = [0, -15]
          }
        }
      })
      this.map.on('pm:drawend', (e) => {
        if (!this.map.shipService) {
            return
        }
        this.map.shipService.setUnclickable(false)
        this.map.shipService.restoreZIndex()
      })
      this.map.on('pm:globaleditmodetoggled pm:globaldragmodetoggled pm:globalremovalmodetoggled',
        (e) => {
        if (!this.map.shipService) {
            return
        }
        if (e.enabled) {
          this.map.shipService.setUnclickable()
          this.map.shipService.setZIndex(399)
        }
        else {
          this.map.shipService.setUnclickable(false)
          this.map.shipService.restoreZIndex()
        }
      })

      // 初始化本组件需要的地图元素
      this.line_pre = SeaMap.polyline([],
        {color: '#333333', weight: 2, dashArray: '6,3'}).addTo(this.map)
      this.line_plan = SeaMap.polyline([], {color: 'red',weight:2}).addTo(this.map)
      // 添加自定义控件
      // 创建信息提示控件
      this.text = SeaMap.control({position:"topleft"})
      this.text.onAdd = function(map) {
        this._div = SeaMap.DomUtil.create('div', 'navmap-text')
        this.update(vue.info)
        return this._div
      }
      this.text.update = function(v) {
        this._div.innerHTML = v
      }
      this.text.addTo(this.map)
      // 创建跟踪选项控件
      let track = SeaMap.control({position:"bottomleft"})
      track.onAdd = function(map) {
        this._div = SeaMap.DomUtil.create('div', 'navmap-track')
        this._span = document.createElement('span')
        this._span.innerHTML = "开启跟踪"
        this._btn = document.createElement('input')
        this._btn.type = 'checkbox'
        this._span.appendChild(this._btn)
        this._div.appendChild(this._span)
        this._btn.onclick = function(e) {
          vue.track = this.checked
        }
        return this._div
      }
      track.addTo(this.map)
    },
    data() {
      return {
        map: Object,
        ship: Object,
        line_pre: Object,
        line_plan: Object,
        text: Object,
        track: false
      }
    },
    watch: {
      path_pre: {
        handler(list, oldVal) {
          this.ship.lng = this.loc[1]
          this.ship.lat = this.loc[0]
          if(this.track)
            this.map.setView(this.loc)
          this.ship.rotation = list.length ?
              90 - 180 / 3.1415926 * Math.atan((list[1][0] - list[0][0]) /
              (list[1][1] - list[0][1])) : 0
          this.line_pre.setLatLngs(list)
          if(this.map.shipService)
            this.map.shipService.updateShip(this.ship)
        },
        deep: true
      },
      path_plan: {
        handler(list, oldVal) {
          this.line_plan.setLatLngs(list)
        },
        deep: true
      },
      info(val) {
        this.text.update(val)
      }
    },
    props: {
      path_plan: Array,
      path_pre: Array,
      info:{
        type:String,
        default: '推荐航速：0.0&nbsp&nbsp&nbsp&nbsp当前航速：0.0&nbsp&nbsp&nbsp&nbsp当前位置：0,0'
      },
      loc: {
        type: Array,
        default: () => {return [0, 0]}
      },
      center: {
        type: Object,
        default: () => { return {
          lng: 121.845001,
          lat: 31.154579
        }}
      }
    }
  }
</script>

<style>
  #navmap {
    width: 100%;
    height: 540px;
    overflow: hidden;
  }
  .navmap-text {
    padding: 6px 8px;
    font: 18px Arial, Helvetica, sans-serif;
    color: #FF8833;
    background: rgba(255,255,255,0.8);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
  }
  .navmap-track {
    padding: 3px 6px;
    font: 14px Arial, Helvetica, sans-serif;
    background: rgba(255,255,255,0.8);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
  }
</style>