<script lang="ts">
import axios from "axios";
import {defineComponent} from "vue";
import Grid from "../components/Grid.vue";
import Logout from "../components/Logout.vue";
import ProfileCard from "../components/ProfileCard.vue";
import {useUserStore} from "../stores/UserStore.ts";
import UserOptions from "../components/UserOptions.vue";
import AdminOptions from "../components/AdminOptions.vue";
import PartnerCard from "../components/PartnerCard.vue";

export default defineComponent({
  components: {PartnerCard, AdminOptions, UserOptions, ProfileCard, Logout, Grid},
  data() {
    return {
      countdown: "",
      userStore: useUserStore(),
      image: null as File | null,
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

    // changeImage(event: Event) {
    //   const target = event.target as HTMLInputElement;
    //
    //   if (target.files && target.files.length > 0) {
    //     this.image = target.files[0];
    //   } else {
    //     this.image = null;
    //   }
    // },
    //
    // async uploadImage() {
    //   if (this.image) {
    //     try {
    //       const formData = new FormData();
    //       {
    //         formData.append('image', this.image);
    //
    //         const response = await axios.post('/api/users/upload', formData, {
    //           headers: {
    //             'Content-Type': 'multipart/form-data',
    //             withCredentials: true
    //           }
    //         });
    //         console.log(response.data);
    //       }
    //     } catch (error: object) {
    //       console.error('Error uploading file:', error.response.data.error)
    //     }
    //   }
    // }
  }
})
</script>

<template>
  <Grid></Grid>
  <logout></logout>
  <div class="profile-container">
    <div class="info">
      <div class="profile">
        <ProfileCard title="" end="'s profile!" increased-size show-profile-text></ProfileCard>
        <div class="content-container">
          <div class="nav">
            <user-options></user-options>
            <admin-options></admin-options>
          </div>
          <div class="content">
            <PartnerCard></PartnerCard>
          </div>
        </div>
      </div>
    </div>
  </div>

<!-- USER IMAGE UPLOAD -->
<!--  <div class="upload">-->
<!--    <input type="file" @change="changeImage" ref="image" />-->
<!--    <button @click="uploadImage" :disabled="!image">Upload Image</button>-->
<!--  </div>-->
<!--  <img style="max-width: 500px" src="http://localhost:8080/users/artwork" />-->
</template>

<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5rem;
  max-width: 1400px;
  margin: auto;
  width: 100%;
}

.info {
  max-height: none;
}

.profile {
  width: 100%;
}

.content-container {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  width: 100%;
}

.content {
  flex: 1;
}

.nav {
  min-width: 270px;
  gap: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
}

@media screen and (max-width: 600px) {
  .content-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }
}
</style>