<script lang="ts">
import {defineComponent} from 'vue'
export default defineComponent({
  name: "SignupStage",

  data() {
    return {
      totalStages: 3
    }
  },

  props: {
    activeStage: {
      type: Object as () => {
        highlight: number;
        name?: string; // Make the 'name' property optional
      },
      required: true
    }
  }
})
</script>

<template>
  <div class="stage">
    <div class="circles" v-for="stage in totalStages" :key="stage">
      <div class="circle" :class="{ 'highlighted': activeStage.highlight === stage }">
        <h3>{{stage}}</h3>
      </div>
      <h3 class="active" v-if="activeStage.highlight === stage">{{activeStage.name}}</h3>
    </div>
  </div>
</template>

<style scoped>
.stage {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 5rem;
}

.circles {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 2rem;
  font-family: 'Fredoka', sans-serif;
  font-size: 2rem;
}

h3 {
  margin: 0;
}

.active {
  filter: drop-shadow(5px 5px 0 rgba(0, 0, 0, 0.10));
}

.circle {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  width: 4rem;
  height: 4rem;

  border-radius: 50%;
  background-color: #FFF2DB;
  box-shadow: 5px 5px 0 rgba(0, 0, 0, 0.10);
  color: #7669E4;

  font-family: 'Fredoka', sans-serif;
  font-size: 1.5rem;
}

.highlighted {
  opacity: 1;
}

.circle:not(.highlighted) {
  opacity: 0.5; /* You can adjust the opacity value as needed */
}

@media screen and (max-width: 600px) {
  .stage {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 5rem;
  }
}
</style>