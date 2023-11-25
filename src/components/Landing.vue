<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "Landing",

  methods: {
    start() {
      window.location.href=`/api/`;
    }
  }
})
</script>

<template>
  <div class="landing">
    <div class="header">
      <button @click="start">Lets Go!</button>
    </div>
    <div class="content">
      <div class="splash-container">
        <img class="splash-art" src="../assets/skrapbuk-christmas-splash.svg" alt="Scrapbook Splash Image."/>
        <div class="nav">
          <button>Home</button>
          <button>Welcome</button>
          <button>How it Works</button>
          <button>FAQs</button>
        </div>
      </div>
    </div>
    <div class="wave-container">
      <img class="wave-svg" src="../assets/wave.svg" alt="wave"/>
    </div>
  </div>
</template>

<style scoped>
.landing {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;

  height: 100vh;
  background: linear-gradient(180deg, #FFF6E6 0%, #FFF8ED 100%);
}

.header {
  box-sizing: border-box;
  width: 100%;
  padding: 25px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.splash-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.splash-art {
  width: 45vw;
  height: 45vh;
}

.nav {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  justify-content: center;
}

.wave-container {
  display: flex;
}

.wave-svg {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
</style>