<script lang="ts">
import {defineComponent} from 'vue'
import {useUserStore} from "../../../stores/UserStore.ts";

export default defineComponent({
  name: "PartnerAnswers",

  data() {
    return {
      userStore: useUserStore(),
      loading: true,
    }
  },

  mounted() {
    this.awaitPartnerAnswers();
  },

  methods: {
    async awaitPartnerAnswers() {
      try {
        await this.userStore.getPartner();
      } catch (error) {
        console.error("Error getting partner details: ", error);
      } finally {
        this.loading = false;
      }
    },

  }
})
</script>

<template>
  <div class="partner-answers">
    <h2>Recipient Answers:</h2>
    <div v-if="loading" class="answers">
      <p>loading...</p>
    </div>
    <div v-else class="answers" :class="{ 'blur': userStore.revealedCard }">
      <p class="question">Their favourite Game:</p>
      <p class="answer">{{ userStore.partner.answers.game }}</p>
      <p class="question">Their favourite Colour:</p>
      <p class="answer">{{ userStore.partner.answers.colour }}</p>
      <p class="question">Their favourite Song:</p>
      <p class="answer">{{ userStore.partner.answers.song }}</p>
      <p class="question">Their favourite Film:</p>
      <p class="answer">{{ userStore.partner.answers.film }}</p>
      <p class="question">Their favourite Food:</p>
      <p class="answer">{{ userStore.partner.answers.food }}</p>
      <p class="question">Their hobbies & interests:</p>
      <p class="answer">{{ userStore.partner.answers.hobby }}</p>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Redacted&display=swap');

.partner-answers {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  max-height: 600px;
  border-radius: 14px;
  box-shadow: 6px 6px 0 0 rgba(0, 0, 0, 0.10);
  padding: 1rem;
  background-color: #2c2760;

  display: flex;
  flex-direction: column;
  justify-content: start;
  gap: 1rem;

  overflow: auto;
}

h2 {
  margin: 0;
  text-align: start;
  font-family: 'Fredoka', sans-serif;
  color: #FFF2DB;
  letter-spacing: 0.06rem;
}

.answers {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.blur > p {
  font-family: 'redacted', sans-serif;
}

.question {
  color: #FF7A6F;
}

.answer {
  word-wrap: anywhere;
  padding-bottom: 1rem;
}
</style>