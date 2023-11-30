<script lang="ts">
import {defineComponent} from 'vue'
import {useUserStore} from "../../../stores/UserStore.ts";

export default defineComponent({
  name: "PartnerRevealCard",

  data() {
    return {
      userStore: useUserStore(),
      loading: true,
      defaultImage: '../src/assets/gom.webp'
    }
  },

  mounted() {
    this.awaitPartnerDetails();
    this.userStore.revealPartner();
  },

  methods: {
    /**
     * Function to ensure that user details have been fetched and stored in pinia
     * before attempting to display them to the page.
     */
    async awaitPartnerDetails() {
      try {
        await this.userStore.getPartner();
      } catch (error) {
        console.error("Error getting partner details: ", error);
      } finally {
        this.loading = false;
      }
    },

    /**
     * Function to convert a discord snowflake into an account created timestamp.
     * @param snowflake {number} - The Discord snowflake.
     * @returns {string} - Returns string of day/month/year date.
     */
    snowflakeToTimestamp(snowflake: number): string {
      const DISCORD_EPOCH = 1420070400000 // Discord epoch (01-01-2015)

      // shift & discard 22 bits of the 64-bit integer,
      // keeping 42 where the timestamp is stored.
      const milliseconds = BigInt(snowflake) >> 22n
      const timestamp = new Date(Number(milliseconds) + DISCORD_EPOCH)

      // create new date, padding any days / month that start with 0
      const date = new Date(timestamp)
      const day = date.getDate().toString().padStart(2, '0');
      const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Months are zero-indexed
      const year = date.getFullYear();

      return `${day}/${month}/${year}`;
    }
  },

  computed: {
    details() {
      return this.userStore.partner ? this.userStore.partner.details : null;
    }
  }

})
</script>

<template>
<div class="card">
  <div v-if="userStore.revealedCard" @click="userStore.revealPartner" class="reveal">
    <h1>Click to Reveal</h1>
  </div>
  <div v-else class="revealed">
    <div v-if="loading" class="profile-info">
      <p>Loading...</p>
    </div>
    <div v-else class="profile-info">
      <img class="avatar" :src="details ? details.avatar_url : defaultImage" alt="recipient discord icon"/>
      <h1>{{ details ? details.username : 'Unknown' }}</h1>
      <p v-if="details"> Member Since: <span class="red">{{ snowflakeToTimestamp(details.snowflake) }}</span></p>
    </div>
    <p class="shh">*Shhh, don’t tell anyone who your recipient is!*</p>
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
  background: linear-gradient(-195deg, #2C2760 36.34%, #373268 36.34%, #373268 95.9%);
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
  justify-content: space-between;
  align-items: center;
}

.profile-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

h1 {
  margin: 0;
  font-family: 'Fredoka', sans-serif;
  color: #FF7A6F;
}

span {
  color: #FF7A6F;
}

.shh {
  text-align: center;
  font-size: 1.1rem;
  color: #cdc2be;
}

.avatar {
  max-width: 128px;
  border: 0.5rem solid rgb(0, 0, 0, 0.3);
  border-radius: 50%;
}

@media screen and (max-width: 600px) {
  .card {
    width: 100%;
    height: 100%;
    max-width: none;
    min-height: 0;
  }

}
</style>