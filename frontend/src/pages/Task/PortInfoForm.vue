<template>
  <md-card>
    <md-card-header data-background-color="green">
        <h4 class="title">港区概况</h4>
    </md-card-header>
    <md-card-content>
      <div class="md-layout">
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>泊位数量</label>
            <md-input v-model="ship.berth_num"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>码头数量</label>
            <md-input v-model="ship.port_num"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>拖轮数量</label>
            <md-input v-model="ship.tug_num"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-50">
          <md-field>
            <label>拖轮配置文件</label>
            <md-file v-model="ship.tug_config_file" />
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
};
</script>
<style></style>
