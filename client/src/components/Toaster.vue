<template>
  <v-snackbar v-model="visible" :timeout="3000" color="error">
    <v-icon left>mdi-alert-circle</v-icon>
    {{ message }}
  </v-snackbar>
</template>

<script>
import { VSnackbar, VIcon } from "vuetify/components";

export default {
  data() {
    return {
      visible: false,
      message: "",
    };
  },
  components: { VSnackbar, VIcon },
  methods: {
    showToast(message) {
      this.message = message;
      this.visible = true;
    },
  },
};
</script>
