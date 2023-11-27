<script lang="ts">
import {defineComponent} from 'vue'
import PartnerRevealCard from "./PartnerRevealCard.vue";
import PartnerAnswers from "./PartnerAnswers.vue";
import {useUserStore} from "../../../stores/UserStore.ts";
import axios from "axios";

export default defineComponent({
  name: "PartnerProfile",
  components: {PartnerAnswers, PartnerRevealCard},

  data() {
    return {
      countdown: "",
      userStore: useUserStore()
    }
  },

  mounted() {
    this.fetchCountdown()
  },

  methods: {
    async fetchCountdown() {
      try {
        const response = await axios.get("/api/event/countdown", {withCredentials: true});
        this.countdown = response.data.countdown;
      } catch (error) {
        console.error(error);
      }
    },

  }
})
</script>

<template>
  <div v-if="this.userStore.showNoPartnerMessage" class="content">
    <div class="no-partner">
      <h1>{{ userStore.noPartnerMessage }}</h1>
      <h2>Time left: <span>{{ countdown }}</span></h2>
    </div>
  </div>
  <div v-else class="content">
    <partner-reveal-card></partner-reveal-card>
    <PartnerAnswers></PartnerAnswers>
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
  color: #FFF2DB;
  font-family: 'Fredoka', sans-serif;
  margin: 0;
}

.no-partner {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  min-height: 600px;
  border-radius: 14px;
  background-color: #2c2760;
  box-shadow: 6px 6px 0 0 rgba(0, 0, 0, 0.10);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

span {
  color: #FF7A6F;
}

@media screen and (max-width: 600px) {
  .content {
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
}
</style>