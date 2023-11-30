<script lang="ts">
import {capitalize, defineComponent} from 'vue'
import axios from "axios";
import {Answers} from "../../../ts/Answers.ts";

export default defineComponent({
  name: "AnswersProfile",

  data() {
    return {
      answers: {} as Answers,
      successMessage: "",
      showSuccessMessage: false,
      invalidAnswers: [] as string[],

      showErrorMessage: false,
      errorMessage: "",
      loading: true,
    }
  },

  methods: {
    capitalize,

    async getAnswers() {
      try {
        const response = await axios.get("/api/users/answers", {withCredentials: true});
        this.answers = response.data;
        this.loading = false

      } catch (error: any) {
        console.error(error.response.data.error)
      }
    },

    async updateAnswers() {
      // clear previous invalid answers
      this.invalidAnswers = []
      this.showSuccessMessage = false

      // iterate over each key, value in the answers object
      Object.entries(this.answers).forEach(([key, value]) => {
        if (value.length < 4 || value.length > 280) {
          // add any invalid objects to list
          this.invalidAnswers.push(key)
        }
      })

      // if there are invalid answers, early return and show borders.
      if (this.invalidAnswers.length > 0) {
        return
      }

      try {
        const request = await axios.post("/api/users/answers",
            this.answers, {withCredentials: true});

        this.successMessage = `${request.data.message}`;
        this.showSuccessMessage = true

        // hide the success message after 3 seconds.
        setTimeout(() => {
          this.showSuccessMessage = false
        }, 3000)

      } catch (error: any) {
        console.error(error)
      }
    },

    isLastItem(index: number): boolean {
      const keys = Object.keys(this.answers);
      return index === keys.length - 1;
    }
  },

  mounted() {
    this.getAnswers()
  }
})
</script>

<template>
  <div class="content">
    <div v-if="showSuccessMessage" class="answers success">
      <h1>{{ successMessage }}</h1>
    </div>
    <div v-else class="answers">
      <div v-if="loading" class="response">
        <p>loading...</p>
      </div>
      <div
          v-else
          v-for="(answer, key, index) in answers"
          :key="key"
          class="response">
          <label :for="key" class="question">Favourite {{ capitalize(key) }}:</label>
          <div
              @click="console.log(answer)"
              class="answer"
              :class="{ 'last': isLastItem(index) }">
            <textarea
              :class="{ 'has-error': invalidAnswers.includes(key) }"
              v-model="answers[key]">
              :id="key"
            </textarea>
            <button v-if="isLastItem(index)" @click="updateAnswers">Update answers!</button>
          </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.content {
  flex: 1;
  display: flex;
  flex-direction: row;
  gap: 1rem;
}

h1, h2 {
  text-align: start;
  color: #FF7A6F;
  font-family: 'Fredoka', sans-serif;
  margin: 0;
  letter-spacing: 0.1rem;
}

.answers {
  box-sizing: border-box;
  width: 100%;
  height: 600px;
  border-radius: 14px;
  background-color: #2c2760;
  box-shadow: 6px 6px 0 0 rgba(0, 0, 0, 0.10);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
  overflow: auto;
}

.success {
  justify-content: center;
  align-items: center;
}

.response {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  padding: 0 1rem 0 1rem;
}

.answer {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.last {
  flex-direction: row;
  gap: 1rem;
}

.last > textarea {
  flex: 1;
}

.question {
  color: #FFF6E7;
}

textarea {
  resize: none;
  color: #FFF6E7;
  background-color: #211d48;
  border: 3px transparent;
  border-radius: 10px;
  padding: 1rem;
  font-family: 'Sniglet', sans-serif;
  height: 1rem;
  overflow: hidden;
}

textarea:focus {
  outline: none;
}

button {
  text-align: center;
  font-family: 'Fredoka', sans-serif;
  padding: 0.4em 2em;
  font-size: 1.2rem;
  letter-spacing: 0.06rem;
  border-radius: 6px;
  color: #FFF2DB;
  background-color: #544ab3;
}

button:hover {
  background-color: #7165e3;
  border-color: #0000001A;
}

.has-error {
  border: 3px solid #FF7A6F;
}

label {
  text-align: start;
}

@media screen and (max-width: 600px) {
  button {
    margin: 0 0 0 0;
  }

  .response {
    padding: 0 0 0 0;
  }

  textarea {
    overflow: hidden;
    height: 100%;
  }

  .answers {
    height: 100%;
  }

  .last {
    flex-direction: column;
    gap: 1rem;
  }

  .last > textarea {
    flex: 1;
  }
}
</style>