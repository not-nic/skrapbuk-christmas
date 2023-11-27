<script lang="ts">
import {defineComponent} from 'vue'
import {useUserStore} from "../../stores/UserStore.ts";

export default defineComponent({
  name: "UserMenuElements",

  data() {
    return {
      userStore: useUserStore()
    }
  }
})
</script>

<template>
  <div class="item">
    <p>USER OPTIONS</p>
    <button @click="userStore.selectMenuItem('partner')">Your Recipient</button>
    <button @click="userStore.selectMenuItem('answers')">Your Answers</button>
    <button @click="userStore.selectMenuItem('upload')">Your Upload</button>
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