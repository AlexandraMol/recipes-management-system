<template>
  <v-card :key="recipe.id" class="mx-auto" max-width="344">
    <v-img
      height="200px"
      src="https://images.pexels.com/photos/691114/pexels-photo-691114.jpeg?cs=srgb&dl=pexels-dana-tentis-118658-691114.jpg&fm=jpg"
      cover
    ></v-img>

    <v-card-title> {{ recipe.name }} </v-card-title>

    <v-card-subtitle>
      {{ recipe.category.join(", ") }}
    </v-card-subtitle>

    <v-card-actions>
      <v-btn color="black" text="Explore" @click="explore"></v-btn>
      <div v-if="isOwnRecipe">
        <span class="card-button" @click="remove">🗑️</span>
        <span class="card-button" @click="edit">✏️</span>
      </div>
    </v-card-actions>
  </v-card>
</template>

<script>
import {
  VCard,
  VImg,
  VCardTitle,
  VCardSubtitle,
  VCardActions,
  VBtn,
} from "vuetify/components";

export default {
  name: "HomePage",
  props: {
    recipe: Object,
    isOwnRecipe: Boolean,
  },
  components: {
    VCard,
    VImg,
    VCardTitle,
    VCardSubtitle,
    VCardActions,
    VBtn,
  },
  methods: {
    explore() {
      //to do redirect to page
      console.log("se apasa pe explore");
    },
    edit() {
      //to do edit
      console.log("se apasa pe edit");
    },
    remove() {
      //to do remove
      console.log("se apasa pe remove");
    },
  },
};
</script>
<style>
.v-card-actions {
  display: flex;
  justify-content: space-between;
}

.card-button {
  cursor: pointer;
  padding: 5px;
}

.card-button:hover {
  background-color: antiquewhite;
}
</style>
