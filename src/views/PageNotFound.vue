<script lang="ts">
import {defineComponent} from 'vue'
import Grid from "../components/Grid.vue";

export default defineComponent({
  name: "PageNotFound",
  components: {Grid}
})
</script>

<template>
  <div class="not-found">
    <Grid></Grid>
    <h1>404!</h1>
    <h3>Gom tried his hardest to find that page, but he couldn't! :(</h3>
  </div>
</template>

<style scoped>
.not-found {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>