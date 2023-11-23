<script lang="ts">
import {defineComponent} from 'vue'
import Landing from "../components/Landing.vue";

export default defineComponent({
  name: "Home",
  components: {Landing},
})
</script>

<template>
<div class="container">
  <Landing></Landing>
</div>
</template>

<style scoped>
</style>