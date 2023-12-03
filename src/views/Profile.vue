<script lang="ts">
import {defineComponent} from "vue";
import Grid from "../components/ui/Grid.vue";
import Logout from "../components/ui/Logout.vue";
import ProfileCard from "../components/ui/ProfileCard.vue";
import {useUserStore} from "../stores/UserStore.ts";
import UserMenuElements from "../components/ui/UserMenuElements.vue";
import AdminMenuElements from "../components/ui/AdminMenuElements.vue";
import PartnerProfile from "../components/profile/partner/PartnerProfile.vue";
import AnswersProfile from "../components/profile/answers/AnswersProfile.vue";
import UploadProfile from "../components/profile/upload/UploadProfile.vue";

export default defineComponent({
  components: {
    UploadProfile,
    AnswersProfile, UserMenuElements, AdminMenuElements, PartnerProfile, ProfileCard, Logout, Grid},

  data() {
    return {
      countdown: "",
      userStore: useUserStore(),
      image: null as File | null,
    }
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
            <user-menu-elements></user-menu-elements>
            <admin-menu-elements></admin-menu-elements>
          </div>
          <partner-profile v-if="userStore.selectedMenuItem === 'partner'"></partner-profile>
          <answers-profile v-if="userStore.selectedMenuItem === 'answers'"></answers-profile>
          <upload-profile v-if="userStore.selectedMenuItem === 'upload'"></upload-profile>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5rem;
  max-width: 1600px;
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