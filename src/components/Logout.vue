<script lang="ts">
import {defineComponent} from 'vue'
import axios from "axios";

export default defineComponent({
  name: "Logout",

  methods: {
    async logout() {
      try {
        await axios.get("/api/logout", {withCredentials: true})
      } catch (error) {
        if (error.response.status === 403) {
          console.log("User logged successfully!")
          // TODO: Instead of pushing to the home, push to a logout page.
          this.$router.push("/")
        } else {
          console.error(error)
        }
      }
    }
  }
})
</script>

<template>
  <div class="logout-container">
    <button @click="logout" class="logout">Log Out</button>
  </div>
</template>

<style scoped>
.logout-container {
  box-sizing: border-box;
  width: 100%;
  display: flex;
  justify-content: end;
  padding: 2rem 3rem 1rem 3rem;
}

.logout {
  color: #FFF2DB;
  background-color: #383083;
}

.logout:hover {
  color: #FF7A6F;
}
</style>