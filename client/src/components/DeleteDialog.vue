<template>
  <v-dialog v-model="dialog" max-width="500">
    <template v-slot:activator="{ props: activatorProps }">
      <span class="card-button" v-bind="activatorProps">🗑️</span>
    </template>

    <v-card title="Delete Confirmation">
      <v-card-text> Are you sure you want to delete this recipe? </v-card-text>

      <v-card-actions>
        <v-btn text="Cancel" @click="dialog = false"></v-btn>
        <v-btn text="Delete" color="red" @click="confirmDelete"></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  VCard,
  VDialog,
  VCardTitle,
  VCardText,
  VCardSubtitle,
  VCardActions,
  VBtn,
} from "vuetify/components";

export default {
  name: "DeleteDialog",
  components: {
    VCard,
    VDialog,
    VCardTitle,
    VCardText,
    VCardSubtitle,
    VCardActions,
    VBtn,
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    confirmDelete() {
      this.$emit("confirmDelete");
      this.dialog = false;
    },
  },
};
</script>
<style>
.card-button {
  cursor: pointer;
  padding: 5px;
}
.card-button:hover {
  background-color: antiquewhite;
}
</style>
