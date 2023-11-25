<script lang="ts">
import {defineComponent} from 'vue'
import {useUserStore} from "../stores/UserStore.ts";

export default defineComponent({
  name: "ProfileCard",

  data() {
    return {
      userStore: useUserStore(),
    }
  },

  props: {
    title: {
      type: String,
      required: false,
      default: "Ready to get started"
    },

    end: {
      type: String,
      required: false,
      default: "?"
    },

    showName: {
      type: Boolean,
      required: false,
      default: true
    },

    showSnowflake: {
      type: Boolean,
      required: false,
      default: false
    },

    showProfileText: {
      type: Boolean,
      required: false,
      default: false
    },

    increasedSize: {
      type: Boolean,
      required: false,
      default: false
    }
  },

  mounted() {
    this.userStore.getUser()
  }
})
</script>

<template>
  <div class="tag">
    <img
        @click="userStore.spinAvatar()"
        :style="`transform: rotate(${userStore.rotateDeg}deg)`"
        :src="userStore.user.avatar_url || userStore.defaultImg"
        alt="Your discord profile picture"/>
    <div class="header">
      <h1 v-if="increasedSize" class="increase">{{title}}<span v-if="showName" class="red">{{" " + userStore.user.username}}</span>{{end}}</h1>
      <h1 v-else>{{title}}<span v-if="showName" class="red">{{" " + userStore.user.username}}</span>{{end}}</h1>
      <p v-show="showProfileText">Here’s your profile, you can use this to view and update your answers, check your recipient info and upload your artwork!</p>
      <div v-show="showSnowflake" class="snowflake-container">
        <p>
            ID: <span
            @mouseover="userStore.showCopy = true"
            @mouseout="userStore.showCopy = false"
            @click="userStore.copySnowflake(userStore.user.snowflake)"
            class="red copy">{{userStore.user.snowflake}}</span>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tag {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding-bottom: 1rem;
}

.header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: first baseline;
}

img {
  max-width: 128px;
  transition-duration: 0.8s;
  transition-property: transform;
  border: 0.5rem solid rgb(0, 0, 0, 0.3);
  border-radius: 50%;
}

h1 {
  margin: 0;
  color: #FFF2DB;
  font-family: 'Fredoka', sans-serif;
}

.increase {
  font-size: 4rem;
}

p {
  font-size: 1.3rem;
  color: rgba(255, 242, 219, 0.90);
}

.red {
  color: #FF7A6F;
}

.snowflake-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.copy {
  opacity: 0.6;
  cursor: pointer;
}

.copy:hover {
  opacity: 1;
}

@media screen and (max-width: 600px) {
  .tag {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding-bottom: 1rem;
  }

  .header {
    flex-direction: column;
  }
}
</style>