<script lang="ts">
import axios from "axios";
import {defineComponent} from "vue";

export default defineComponent({
  data() {
    return {
      countdown: "",
      user: {},
      image: null as File | null,
    }
  },

  mounted() {
    this.fetchTime()
    this.getUser()
  },

  methods: {
    async fetchTime() {
      try {
        const response = await axios.get("/api/event/countdown", {withCredentials: true});
        this.countdown = response.data.countdown;
      } catch (error) {
        console.error(error);
      }
    },

    async getUser() {
      try {
        const response = await axios.get("/api/users/me", {withCredentials: true})

        console.log(response.data)
        this.user = response.data;

      } catch (error) {
        console.error(error)
      }
    },

    redirect(route: string) {
      window.location.href= `http://localhost:8080/${route}`;
    },

    async createQuestions() {
      try {
        const request = await axios.post("/api/users/answers",{
          game: 'Farming Simulator 22',
          colour: 'Orange',
          song: 'The Wombats: Tokyo',
          film: 'Hot Fuzz',
          food: 'Fish n Chips',
          hobby: "Programming & Being Bri''ish"
        }, {withCredentials: true})
        console.log(request)

      } catch(error) {
        console.error(error)
      }
    },

    changeImage(event: Event) {
      const target = event.target as HTMLInputElement;

      if (target.files && target.files.length > 0) {
        this.image = target.files[0];
      } else {
        this.image = null;
      }
    },

    async uploadImage() {
      if (this.image) {
        try {
          const formData = new FormData();
          {
            formData.append('image', this.image);

            const response = await axios.post('/api/users/upload', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
                withCredentials: true
              }
            });
            console.log(response.data);
          }
        } catch (error: object) {
          console.error('Error uploading file:', error.response.data.error)
        }
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
    <p>Countdown: {{countdown}}</p>
  </div>
  <div class="container">
    <div class="buttons">
      <button @click="redirect('users/join')">join</button>
      <button @click="redirect('event/start')">start</button>
      <button @click="redirect('users/all')">users</button>
      <button @click="createQuestions()">create questions</button>
    </div>
    <div class="upload">
      <input type="file" @change="changeImage" ref="image" />
      <button @click="uploadImage" :disabled="!image">Upload Image</button>
    </div>
    <img style="max-width: 500px" src="http://localhost:8080/users/artwork" />
  </div>
</template>

<style scoped>
p {
  font-family: 'Sniglet', cursive;
  font-size: 18px;
}

.container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>