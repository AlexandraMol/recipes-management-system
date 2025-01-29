<template>
  <div v-if="loading">Loading...</div>
  <div v-else class="recipe-container">
    <span class="element" v-for="(recipe, index) in recipes" :key="index">
      <RecipeCard
        v-bind:key="recipe.id"
        :recipe="recipe"
        :isOwnRecipe="false"
      ></RecipeCard>
    </span>
  </div>
</template>
<script>
import RecipeCard from "@/components/RecipeCard.vue";
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  name: "Explore",
  data() {
    return {
      recipes: [],
      loading: true,
    };
  },
  components: {
    RecipeCard,
  },

  computed: {
    ...mapGetters(["currentUser"]),
  },

  mounted() {
    this.getRecipes();
  },

  methods: {
    async getRecipes() {
      const token = await this.currentUser.getIdToken();
      try {
        const response = await axios.get(
          `http://localhost:3000/api/recipe/otherRecipes/${this.currentUser.displayName}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );
        if (response.status === 200) {
          console.log(response);
          this.recipes = response.data.data;
        }
      } catch (error) {
        console.log(error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
