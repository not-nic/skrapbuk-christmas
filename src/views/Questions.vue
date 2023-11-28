<script lang="ts">
import {defineComponent} from 'vue'
import Grid from "../components/ui/Grid.vue";
import SignupStage from "../components/signup/SignupStage.vue";
import ProfileCard from "../components/ui/ProfileCard.vue";
import axios from "axios";
import Logout from "../components/ui/Logout.vue";
import {Answers} from "../ts/Answers.ts";

export default defineComponent({
  name: "Questions",
  components: {Logout, ProfileCard, SignupStage, Grid},

  data() {
    const answers: Answers = {
      game: "",
      colour: "",
      song: "",
      film: "",
      food: "",
      hobby: "",
    };

    return {
      questions: [
        {question: "Let's start with something easy, Gom would like to know what is your all time favourite game?"},
        {question: "Sweet! Now tell me, what is your favourite colour?"},
        {question: "Very nice! What is your favourite tune to jam out to? (What's your favourite song)"},
        {question: "I love that too! What is your favourite film to watch?"},
        {question: "Amazing! What is your favourite food to eat?"},
        {question: "Okay last one! What are some of your hobbies and interests?"}
      ],

      answers,
      answersSubmitted: false,
      currentQuestionIndex: 0,
      showErrorMessage: false,
      errorMessage: "",
    }
  },

  methods: {
    /**
     * Function to control the user progressing through questions.
     */
    nextQuestion() {
      // check if answer is not null before letting user move on.
      if (this.answers[this.currentQuestionKey] == "") {
        this.errorMessage = "Your answer can't be empty!";
        this.showErrorMessage = true;
      }
      // check if answer is > 4 characters before letting them move on.
      else if (this.answers[this.currentQuestionKey].length < 4) {
        this.errorMessage = "That answer is a bit too short, could you be a little more descriptive? (Min 4 Characters)";
        this.showErrorMessage = true;
      }
      else if (this.answers[this.currentQuestionKey].length > 280) {
        this.errorMessage = "Woah, that answer is quite long! Maybe you could shorten it? (Max 280 Characters)";
        this.showErrorMessage = true;
      }
      else {
        // answer passed checks, increment question index and take user to next question.
        this.currentQuestionIndex++;
      }
    },

    /**
     * If a user caused an error message, focusing on the input box makes it disappear.
     */
    reshowQuestion() {
      this.showErrorMessage = false
    },

    /**
     * Push router to the final stage of sign up - join page.
     */
    showJoinPage() {
      this.$router.push("join")
    },

    /**
     * Function to submit user answers to database during signup.
     */
    async submitAnswers() {
      try {
        const request = await axios.post("/api/users/answers", this.answers, {withCredentials: true})
        console.log(request.data);
        this.answersSubmitted = true;
        this.$router.push("/join")
      } catch (error: any) {
        console.error(error.response.data.error)
        this.errorMessage = `Sorry! An error has occurred: ${error.response.data.error}`
        this.showErrorMessage = true;
      }
      console.log(this.answers)
    },
  },

  computed: {
    currentQuestionKey(): keyof Answers {
      const keys = Object.keys(this.answers);
      return keys[this.currentQuestionIndex] as keyof Answers;
    },

    showCounter(): boolean {
      return this.currentQuestionIndex < this.questions.length;
    },

    isLastQuestion(): boolean {
      return this.currentQuestionIndex === this.questions.length - 1;
    }
  }
})
</script>

<template>
  <Grid></Grid>
  <Logout></Logout>
  <div class="questions">
    <SignupStage :active-stage="{highlight: 2, name: 'Questions!'}"></SignupStage>
    <div class="info">
      <div class="header">
        <ProfileCard title="" end="'s question time!" :show-name="true"></ProfileCard>
        <h1 class="counter" v-show="showCounter">
          <span class="red">{{ `${currentQuestionIndex + 1}` }}</span>
          <span>{{ `/${questions.length}` }}</span>
        </h1>
      </div>
      <div class="question-container" v-if="!answersSubmitted">
        <p v-if="showErrorMessage" class="red">{{errorMessage}}</p>
        <p v-else>{{ questions[currentQuestionIndex].question }}</p>
        <div class="user-input">
          <input v-model="answers[currentQuestionKey]" @click="reshowQuestion" type="text" />
          <button v-show="!isLastQuestion" @click="nextQuestion">Next Question</button>
          <button v-show="isLastQuestion" class="submit" @click="submitAnswers">Submit Answers!</button>
        </div>
      </div>
      <div v-else-if="showErrorMessage" class="question-container">
        <p v-if="showErrorMessage" class="red">{{errorMessage}}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.counter {
  margin: 0;
  color: #FFF2DB;
  font-family: 'Fredoka', sans-serif;
}

.red {
  color: #FF7A6F;
}

.questions {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5rem;
  max-width: 1184px;
  margin: auto;
  width: 100%;
}

.question-container {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.user-input {
  width: 100%;
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 4rem;
}

p {
  font-size: 1.3rem;
  color: #FFF6E7;
  padding: 0 0 1rem 0;
}

input {
  border-radius: 10px;
  border: 3px transparent;
  width: 100%;
  height: 64px;
  padding: 1rem;
  box-sizing: border-box;
  font-family: 'Sniglet', sans-serif;
  font-size: 1.2rem;
  color: #2f2f2f;
  background-color: #FFF6E7;
  transition: border 0.1s;
  box-shadow: 5px 5px 0 rgba(0, 0, 0, 0.10)
}

input:focus {
  border: 3px solid #FF7A6F;
  outline: none;
}

button {
  width: 30%;
  background-color: #7165e3;
  color: #FFF2DB;
  max-height: 64px;
  min-width: 240px;
  white-space: nowrap;
}

button:hover {
  border-color: #0000001A;
}

.submit {
  min-width: 260px;
  text-align: center;
  color: #fff9f3;
  background-color: #FF7A6F;
}

@media screen and (max-width: 600px) {
  .counter {
    display: none;
  }

  p {
    text-align: center;
  }

  .question-container {
    flex-direction: column;
  }

  .user-input {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    width: 100%;
  }

  button {
    width: 100%;
  }
}
</style>