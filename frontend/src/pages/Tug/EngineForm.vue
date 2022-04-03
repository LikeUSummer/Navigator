<template>
  <md-card>
    <md-card-header data-background-color="green">
        <h4 class="title">主机参数</h4>
    </md-card-header>
    <md-card-content>
      <div class="md-layout">
        <div class="md-layout-item md-small-size-100 md-size-50">
            <md-toolbar class="md-transparent">
                <span class="md-title">左推进器</span>
            </md-toolbar>
            <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
                <label for="type">型号</label>
                <md-select v-model="ship.engine_type[0]">
                    <md-option value="MAN S35ME-B9-EGRBP">MAN S35ME-B9-EGRBP</md-option>
                    <md-option value="MAN S35ME-B9-HPSCR">MAN S35ME-B9-HPSCR</md-option>
                    <md-option value="MAN S35ME-B9-LPSCR">MAN S35ME-B9-LPSCR</md-option>
                </md-select>
            </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
                <label>额定功率(kW)</label>
                <md-input v-model="ship.power[0]"></md-input>
            </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
                <label>齿轮箱减速比</label>
                <md-input v-model="ship.reduction[0]"></md-input>
            </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
                <label>主机特性曲线(a,b,c)</label>
                <md-input v-model="ship.engine_eigen[0]"></md-input>
            </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
                <label>主机位置x,y,z(m)</label>
                <md-input v-model="ship.engine_loc[0]"></md-input>
            </md-field>
            </div>
        </div>
        <div class="md-layout-item md-small-size-100 md-size-50">
            <md-toolbar class="md-transparent">
                <span class="md-title">右推进器</span>
            </md-toolbar>
            <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
                <label for="type">型号</label>
                <md-select v-model="ship.engine_type[1]">
                    <md-option value="MAN S35ME-B9-EGRBP">MAN S35ME-B9-EGRBP</md-option>
                    <md-option value="MAN S35ME-B9-HPSCR">MAN S35ME-B9-HPSCR</md-option>
                    <md-option value="MAN S35ME-B9-LPSCR">MAN S35ME-B9-LPSCR</md-option>
                </md-select>
            </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
                <label>额定功率(kW)</label>
                <md-input v-model="ship.power[1]"></md-input>
            </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
                <label>齿轮箱减速比</label>
                <md-input v-model="ship.reduction[1]"></md-input>
            </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
                <label>主机特性曲线(a,b,c)</label>
                <md-input v-model="ship.engine_eigen[1]"></md-input>
            </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
                <label>主机位置x,y,z(m)</label>
                <md-input v-model="ship.engine_loc[1]"></md-input>
            </md-field>
            </div>
        </div>
      </div>
    </md-card-content>
  </md-card>  
</template>

<script>
export default {
  name: "host-form",
  props: {
    ship: Object
  }
}
</script>
