<script lang="ts">
import axios from "axios";
import {defineComponent} from "vue";

export default defineComponent({
  data() {
    return {
      data: "",
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
        const response = await axios.get("/api/time", {withCredentials: true});
        let time = response.data.the_time;
        this.data = time;
        console.log(time);

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
    <p>Time: {{data}}</p>
  </div>
</template>

<style scoped>
p {
  font-family: 'Sniglet', cursive;
  font-size: 18px;
}
</style>
