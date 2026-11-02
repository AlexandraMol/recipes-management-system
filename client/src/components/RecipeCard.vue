<template>
  <v-card :key="recipe.id" class="recipe-card" max-width="344">
    <v-img height="200px" :src="recipe.imageUrl" cover></v-img>

    <div class="title-section">
      <v-card-title> {{ recipe.name }} </v-card-title>
      <div v-if="hasMatchPercentage" class="match-badge">
        {{ recipe.matchPercentage }}% match
      </div>
    </div>
    <v-card-subtitle> {{ recipe?.category?.join(", ") }} </v-card-subtitle>

    <v-card-actions>
      <v-btn color="black" text="Explore" @click="explore"></v-btn>
      <div v-if="isOwnRecipe">
        <DeleteDialog @confirmDelete="remove" />
        <span class="card-button" @click="edit">✏️</span>
      </div>
      <div v-else>
        <span
          >{{ recipe?.averageRating || 0 }} ⭐ ({{
            recipe?.numberOfRatings || 0
          }}</span
        >)
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
import DeleteDialog from "@/components/DeleteDialog.vue";
import { mapGetters } from "vuex";
import axios from "axios";

export default {
  name: "RecipeCard",
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
    DeleteDialog,
  },
  computed: {
    ...mapGetters(["currentUser"]),
    hasMatchPercentage() {
      return (
        this.recipe.matchPercentage !== null &&
        this.recipe.matchPercentage !== undefined
      );
    },
  },
  emits: ["recipe-deleted"],
  methods: {
    explore() {
      this.$router.push(`/recipe/${this.recipe.id}`);
    },
    edit() {
      this.$router.push(`/recipe/edit/${this.recipe.id}`);
    },
    async remove() {
      try {
        const token = await this.currentUser.getIdToken();

        await axios.delete(
          `http://localhost:5000/api/recipe/remove/${this.recipe.id}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          },
        );

        this.$emit("recipe-deleted", this.recipe.id);
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style scoped>
.recipe-card {
  border: 1px solid black;
  width: 100%;
  height: 100%;
  min-width: 0;
}

.v-card-actions {
  display: flex;
  justify-content: space-between;
}

.title-section {
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

.match-badge {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  margin: 2px;
  padding: 6px 10px;
  border-radius: 999px;

  background: var(--color-secondary);
  color: var(--color-dark);

  font-size: 12px;
  font-weight: 800;
}
</style>
