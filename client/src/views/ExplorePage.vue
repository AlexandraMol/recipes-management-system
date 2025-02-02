<template>
  <Loading v-if="loading"></Loading>
  <div v-else>
    <Filters />
    <div class="recipe-container">
      <span
        class="element"
        v-for="(recipe, index) in filteredRecipes"
        :key="index"
      >
        <RecipeCard
          v-bind:key="recipe.id"
          :recipe="recipe"
          :isOwnRecipe="false"
        ></RecipeCard>
      </span>
    </div>
  </div>
</template>
<script>
import RecipeCard from "@/components/RecipeCard.vue";
import axios from "axios";
import { mapGetters } from "vuex";
import Loading from "@/components/Loading.vue";
import Filters from "@/components/Filters.vue";

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
    Loading,
    Filters,
  },

  computed: {
    ...mapGetters(["currentUser", "getSelectedFilters"]),
    filteredRecipes() {
      return this.getSelectedFilters.length
        ? this.recipes.filter((recipe) =>
            this.getSelectedFilters.every((filter) =>
              recipe.category.includes(filter)
            )
          )
        : this.recipes;
    },
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
