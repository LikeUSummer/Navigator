<template>
  <md-card>
    <md-card-header data-background-color="green">
      <h4 class="title">船型参数</h4>
    </md-card-header>
    <md-card-content>
      <div class="md-layout">
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>船体长度(m)</label>
            <md-input v-model="ship.length"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>船体宽度(m)</label>
            <md-input v-model="ship.width"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>重心位置x,y,z(m)</label>
            <md-input v-model="ship.phy_center"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>中心位置x,y,z(m)</label>
            <md-input v-model="ship.geo_center"></md-input>
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
