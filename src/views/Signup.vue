<script lang="ts">
import {defineComponent} from 'vue'
import axios from "axios";
import SignupStage from "../components/SignupStage.vue";

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
  name: "Signup",
  components: {SignupStage},

  data() {
    return {
      user: {} as Profile,
      rotateDeg: 0
    }
  },

  methods: {
    /**
     * Easter egg function to spin the users avatar when clicked.
     */
    spinAvatar() {
      this.rotateDeg += 360;
    },

    /**
     * Push user to /questions endpoint
     */
    showQuestions() {
      this.$router.push('questions')
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
  <div class="sign-up">
    <SignupStage :active-stage="{highlight: 1, name: 'Questions'}"></SignupStage>
    <div class="info">
      <div class="tag">
        <img @click="spinAvatar" :style="`transform: rotate(${rotateDeg}deg)`" :src="user.avatar_url" alt="Your discord profile picture"/>
        <h1>Ready to get Started <span class="name">{{user.username}}</span>?</h1>
      </div>
      <p>
        Looks like you're all logged in!
        Just make sure you've read through <a href="/">Gom's Guide</a>
        before you get started with the festive fun by answering some questions!
      </p>
      <button @click="showQuestions">Show Questions!</button>
    </div>
  </div>
</template>

<style scoped>
.sign-up {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5rem;
}

.info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;
  gap: 1rem;
  max-width: 1024px;
  height: 100%;
  padding: 3rem 5rem 3rem 5rem;

  border-radius: 32px;
  background: #383083;
  box-shadow: 15px 10px 0 rgba(0, 0, 0, 0.10)
}

.tag {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  padding-bottom: 1rem;
}

img {
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

p {
  margin: 0;
  font-size: 1.2rem;
  text-align: left;
  line-height: 175%;
}

button {
  background-color: #7165e3;
  color: #FFF2DB;
}

button:hover {
  border-color: #0000001A;
}

@media screen and (max-width: 600px) {
  .info {
    align-items: center;
    width: 100%;
    height: 100%;
    border-radius: 0;
    box-shadow: none;
    padding: 3rem 0 3rem 0;
  }

  .tag {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding-bottom: 1rem;
  }

  p {
    text-align: center;
  }
}
</style>
