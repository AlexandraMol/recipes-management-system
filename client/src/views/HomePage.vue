<template>
  <div v-if="loading">Loading...</div>
  <div v-else class="recipe-container">
    <span class="element" v-for="(recipe, index) in recipes" :key="index">
      <RecipeCard
        v-bind:key="recipe.id"
        :recipe="recipe"
        :isOwnRecipe="true"
      ></RecipeCard>
    </span>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
import RecipeCard from "@/components/RecipeCard.vue";

export default {
  name: "HomePage",
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
      try {
        const token = await this.currentUser.getIdToken();
        const response = await axios.get(
          `http://localhost:3000/api/recipe/${this.currentUser.displayName}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );
        if (response.status === 200) {
          this.recipes = response.data.data;
        }
      } catch (error) {
        console.log(error);
        this.recipes = [];
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style>
.recipe-container {
  display: grid;
  gap: 1px;
  grid-template-columns: repeat(3, 1fr);
}

.element {
  margin: 10px;
}

@media (max-width: 1000px) {
  .recipe-container {
    display: block;
  }
}
</style>
