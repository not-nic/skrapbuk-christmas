<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "UserOptions"
})
</script>

<template>
  <div class="item">
    <p>USER OPTIONS</p>
    <button>Your Recipient</button>
    <button>Your Answers</button>
    <button>Your Upload</button>
  </div>
</template>

<style scoped>
button {
  background-color: #544ab3;
}

.item > button:focus {
  background-color: #7165e3;
}

.item > button:hover {
  border-color: #0000001A;
}
</style>