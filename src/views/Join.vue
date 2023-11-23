<script lang="ts">
import {defineComponent} from 'vue'
import Grid from "../components/Grid.vue";
import SignupStage from "../components/SignupStage.vue";
import SignupCard from "../components/SignupCard.vue";
import axios, {request} from "axios";

export default defineComponent({
  name: "Join",
  components: {SignupCard, SignupStage, Grid},

  data() {
    return {
      successMessage: "",
      errorMessage: "",
      showErrorMessage: false
    }
  },

  methods: {
    async join() {
      try {
        const response = await axios.get("/api/users/join", {withCredentials: true})
        console.log(response.data)
        this.successMessage = response.data.message
        setTimeout(() => {
          this.$router.push("profile")
        }, 5000)

      } catch (error: any) {

        if (error.response.data.joined) {
          this.successMessage = "You're already in! Redirecting you to your profile in 5 seconds."
          setTimeout(() => {
            this.$router.push("profile")
          }, 5000)
        }

        else {
          this.errorMessage = `${error.response.data.error}`
          this.showErrorMessage = true;
        }
        console.error(error.response.data.error)
      }
    }
  }
})
</script>

<template>
<div>
  <Grid></Grid>
  <div class="join">
    <SignupStage :active-stage="{highlight: 3, name: 'Join in!'}"></SignupStage>
    <div class="info">
      <SignupCard title="" end=" it's time to join!" :show-name="true"></SignupCard>
      <p>
        That was easy! All your answers have been submitted, so all that’s left to do is join the event!
        <br>Once you join, you’ll be taken to a profile we’ve set up for you.
        So, when the countdown is over, this is where you will be able to see your assigned partner!
      </p>
      <p class="red" v-if="showErrorMessage">{{errorMessage}}</p>
      <p v-else class="mint">{{successMessage}}</p>
      <button @click="join">Join Skrapbuk Christmas!</button>
    </div>
  </div>

</div>
</template>

<style scoped>
.info {
  max-height: none;
}

.red {
  color: #FF7A6F;
}

.mint {
  color: #6FFFCB;
}

.join {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5rem;
  max-width: 1184px;
  margin: auto;
  width: 100%;
}

button:hover {
  color: #FFF2DB;
  border-color: #0000001A;
}
</style>