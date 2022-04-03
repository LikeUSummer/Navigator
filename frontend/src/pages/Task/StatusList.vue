<template>
  <div>
    <md-toolbar class="md-transparent">
      <span class="md-title">任务列表</span>
    </md-toolbar>
    <md-list>
      <md-list-item v-for="(task, k) in data" @click="$emit('update:index', k);" :key="k">
        <md-icon :class="index == k ? 'md-primary' : ''">{{icon_type[task.status]}}</md-icon>
        <span class="md-list-item-text" style="position:unset;">{{task.title}}</span>
      </md-list-item>
    </md-list>
  </div>
</template>

<script>
  export default {
    name: 'status-list',
    props: {
      index: Number,
      data: Array
    },
    data() {
      return {
        icon_type: {
          run: "toys",
          wait: "access_alarms",
          stop: "pan_tool"
        },
        status_name: {
          run: "进行中",
          wait: "等待中",
          stop: "停止"
        }
      }
    }
  }
</script>
