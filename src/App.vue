<script lang="ts">
import axios from "axios";
import {defineComponent} from "vue";

export default defineComponent({
  data() {
    return {
      countdown: "",
      user: {}
    }
  },

  mounted() {
    this.fetchTime()
    this.getUser()
  },

  methods: {
    async fetchTime() {
      try {
        const response = await axios.get("/api/countdown", {withCredentials: true});
        this.countdown = response.data.countdown;
      } catch (error) {
        console.error(error);
      }
    },

    async getUser() {
      try {
        const response = await axios.get("/api/user", {withCredentials: true})

        console.log(response.data)
        this.user = response.data;

      } catch (error) {
        console.error(error)
      }
    },

    redirect(route: string) {
      window.location.href= `http://localhost:8080/${route}`;
    }
  }
})
</script>

<template>
  <div>
    <img src="./assets/sb.svg" alt="Skrapbuk Logo">
  </div>
  <div class="user">
    <span>{{user}}</span>
  </div>
  <div>
    <p>Countdown: {{countdown}}</p>
  </div>
  <div class="buttons">
    <button @click="redirect('join')">join</button>
    <button @click="redirect('start')">start</button>
    <button @click="redirect('users')">users</button>
  </div>
</template>

<style scoped>
p {
  font-family: 'Sniglet', cursive;
  font-size: 18px;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
