<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "Grid"
})
</script>

<template>
  <div class="grid-bg"></div>
</template>

<style scoped>
  .grid-bg {
    z-index: -9999999;
    height: 100vh;
    background: url("../../assets/dotsbg.png");
    background-size: 40px;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    opacity: .25;
  }
</style>