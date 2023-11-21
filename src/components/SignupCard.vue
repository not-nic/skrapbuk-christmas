<script lang="ts">
import {defineComponent} from 'vue'
import axios from "axios";

interface Profile {
  username: string,
  snowflake: number,
  avatar_url: string,
  in_server: boolean,
  is_admin: boolean,
  is_banned: boolean,
  partner: number
}

export default defineComponent({
  name: "SignupCard",

  data() {
    return {
      user: {} as Profile,
      rotateDeg: 0,
      defaultImg: "../src/assets/gom.webp",
      clickCount: 0
    }
  },

  props: {
    title: {
      type: String,
      required: false,
      default: "Ready to get started"
    },

    end: {
      type: String,
      required: false,
      default: "?"
    },

    showName: {
      type: Boolean,
      required: false,
      default: true
    }
  },

  methods: {
    /**
     * Easter egg function to spin the users avatar when clicked.
     */
    spinAvatar() {
      this.rotateDeg += 360;
      this.clickCount += 1;

      if (this.clickCount > 25) {
        this.clickCount = 0;
        this.user.avatar_url = this.defaultImg;
      }
    },

    /**
     * Asynchronous to get an authorised users discord details from Flask.
     */
    async getUser() {
      try {
        // if authed, get the user's details and add them to the user object.
        const response = await axios.get("/api/users/me", {withCredentials: true})
        this.user = response.data;
      } catch (error: any) {

        // check if the user is unauthorised, if so redirect them to the login page.
        if (error.response?.status === 401) {
          window.location.href = "http://localhost:8080";
        } else {
          console.error('Non-401 error:', error);
        }
      }
    }
  },

  mounted() {
    this.getUser()
  }
})
</script>

<template>
  <div class="tag">
    <img
        @click="spinAvatar"
        :style="`transform: rotate(${rotateDeg}deg)`"
        :src="user.avatar_url || defaultImg"
        alt="Your discord profile picture"/>
    <h1>{{title}}<span v-if="showName" class="name">{{" " + user.username}}</span>{{end}}</h1>
  </div>
</template>

<style scoped>
.tag {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  padding-bottom: 1rem;
}

img {
  max-width: 128px;
  transition-duration: 0.8s;
  transition-property: transform;
  border: 0.5rem solid rgb(0, 0, 0, 0.3);
  border-radius: 50%;
}

h1 {
  margin: 0;
  color: #FFF2DB;
  font-family: 'Fredoka', sans-serif;
}

.name {
  color: #FF7A6F;
}

@media screen and (max-width: 600px) {
  .tag {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding-bottom: 1rem;
  }
}
</style>