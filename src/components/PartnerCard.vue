<script lang="ts">
import {defineComponent} from 'vue'
import {useUserStore} from "../stores/UserStore.ts";

export default defineComponent({
  name: "PartnerCard",

  data() {
    return {
      userStore: useUserStore()
    }
  },

  mounted() {
    this.userStore.revealPartner();
  }
})
</script>

<template>
<div class="card">
  <div v-if="userStore.revealedCard" @click="userStore.revealPartner" class="reveal">
    <h1>Click to Reveal</h1>
  </div>
  <div v-else class="revealed">
    <div class="profile-info">
      <img class="avatar" src="../assets/gom.webp" alt="partner discord icon"/>
      <h1>username</h1>
      <p>Member Since:</p>
    </div>
    <p>*Shhh, don’t tell anyone who your recipient is!*</p>
  </div>
</div>
</template>

<style scoped>
.card {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  max-width: 340px;
  min-height: 600px;
  border-radius: 14px;
  background: linear-gradient(175deg, #2C2760 43.54%, #373268 43.54%, #373268 96.92%);
  box-shadow: 6px 6px 0 0 rgba(0, 0, 0, 0.10);
  padding: 1rem;
}

.reveal {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.revealed {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

h1 {
  margin: 0;
  font-family: 'Fredoka', sans-serif;
  color: #FF7A6F;
}

.avatar {
  max-width: 128px;
  border: 0.5rem solid rgb(0, 0, 0, 0.3);
  border-radius: 50%;
}
</style>