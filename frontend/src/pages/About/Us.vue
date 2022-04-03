<template>
  <md-card class="md-card-profile">
    <div class="md-card-avatar">
      <img class="img" :src="cardUserImage" />
    </div>

    <md-card-content>
      <h6 class="category text-gray">大航海家</h6>
      <h4 class="card-title">航速优化系统</h4>
      <p class="card-description">
        未经作者授权，请勿商用，否则将追究法律责任
      </p>
      <md-button class="md-round md-success" href="https://www.zhihu.com/people/da-xia-tian-60">
        联系作者
      </md-button>
    </md-card-content>
  </md-card>
</template>

<script>
export default {
  name: "user-card",
  props: {
    cardUserImage: {
      type: String,
      default: require("@/assets/img/about.png")
    }
  },
  data() {
    return {}
  }
};
</script>
