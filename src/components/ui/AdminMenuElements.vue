<script lang="ts">
import {defineComponent} from 'vue'
import {useUserStore} from "../../stores/UserStore.ts";

export default defineComponent({
  name: "AdminMenuElements",

  data() {
    return {
      userStore: useUserStore()
    }
  }
})
</script>

<template>
  <div v-show="userStore.user.is_admin" class="item">
    <p>ADMIN OPTIONS</p>
    <button>Start Event</button>
    <button>View All Users</button>
    <button>View Submissions</button>
    <button>Ban User</button>
  </div>
</template>

<style scoped>
.disabled {
  opacity: 0.4;
}

button {
  background-color: #9b5579;
}

.item > button:focus {
  background-color: #FF7A6F;
}

.item > button:hover {
  border-color: #0000001A;
}
</style>