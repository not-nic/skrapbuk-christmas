<script lang="ts">
import {defineComponent} from 'vue'
import Grid from "../components/Grid.vue";
import SignupStage from "../components/SignupStage.vue";
import SignupCard from "../components/SignupCard.vue";
import axios from "axios";
import Logout from "../components/Logout.vue";

interface Answers {
  game: string;
  colour: string;
  song: string;
  film: string;
  food: string;
  hobby: string;
}

export default defineComponent({
  name: "Questions",
  components: {Logout, SignupCard, SignupStage, Grid},

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
      currentQuestionIndex: 0,
    }
  },

  methods: {
    nextQuestion() {
      this.currentQuestionIndex++;

      if (this.isLastQuestion) {
        this.submitAnswers();
      }
    },

    async submitAnswers() {
      try {
        const request = await axios.post("/api/users/answers", this.answers, {withCredentials: true})
        console.log(request.data);
      } catch (error) {
        console.error(error)
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
        <SignupCard title="" end="'s question time!" :show-name="true"></SignupCard>
        <h1 class="counter" v-show="showCounter">
          <span class="current">{{ `${currentQuestionIndex + 1}` }}</span>
          <span>{{ `/${questions.length}` }}</span>
        </h1>
      </div>
      <div class="question-container" v-if="showCounter">
        <p>{{ questions[currentQuestionIndex].question }}</p>
        <div class="user-input">
          <input v-model="answers[currentQuestionKey]" @keyup.enter="nextQuestion" type="text" />
          <button v-show="!isLastQuestion" @click="nextQuestion">Next Question</button>
          <button v-show="isLastQuestion" class="submit" @click="nextQuestion">Submit Answers!</button>
        </div>
      </div>
      <div v-else class="question-container">
        <p>All done, ready to move on?</p>
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

.current {
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