<template>
    <stats-card :data-background-color="color">
      <template slot="header">
        <md-icon>{{icon}}</md-icon>
      </template>

      <template slot="content">
        <p class="category">{{title}}</p>
        <h4 class="title" :style="{color:color}">{{value}}</h4>
      </template>

      <template slot="footer">
        <div class="stats">
          <md-icon>local_offer</md-icon>
          {{footer}}
        </div>
      </template>
    </stats-card>
</template>

<script>
  import {StatsCard} from "@/components";
  export default {
    components: {
      StatsCard
    },
    props: {
      font_color: String,
      color: String,
      icon: String,
      title: String,
      value: String,
      footer: String
    }
  }
</script>