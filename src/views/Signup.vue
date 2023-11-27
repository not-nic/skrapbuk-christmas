<script lang="ts">
import {defineComponent} from 'vue'
import SignupStage from "../components/signup/SignupStage.vue";
import Grid from "../components/ui/Grid.vue";
import ProfileCard from "../components/ui/ProfileCard.vue";
import Logout from "../components/ui/Logout.vue";

export default defineComponent({
  name: "Signup",
  components: {Logout, ProfileCard, Grid, SignupStage},

  methods: {
    /**
     * Push user to /questions endpoint
     */
    showQuestions() {
      this.$router.push('questions')
    }
  }
})
</script>

<template>
  <Grid></Grid>
  <Logout></Logout>
  <div class="sign-up">
    <SignupStage :active-stage="{highlight: 1, name: 'Get Ready!'}"></SignupStage>
    <div class="info">
      <ProfileCard></ProfileCard>
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
  max-width: 1184px;
  margin: auto;
}

button {
  background-color: #7165e3;
  color: #FFF2DB;
}

button:hover {
  border-color: #0000001A;
}

@media screen and (max-width: 600px) {
  p {
    text-align: center;
  }
}
</style>
