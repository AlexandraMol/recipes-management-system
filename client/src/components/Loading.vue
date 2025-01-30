<template>
  <div class="loading-container">
    <v-progress-circular
      indeterminate
      color="black"
      size="50"
      width="5"
    ></v-progress-circular>
    <p>Loading...</p>
  </div>
</template>

<script>
import { VProgressCircular } from "vuetify/components";

export default {
  name: "Loading",
  components: {
    VProgressCircular,
  },
};
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
  gap: 10px;
}
</style>
