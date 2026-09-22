<template>
  <Loading v-if="loading"></Loading>
  <div v-else>
    <div class="recipe-container">
      <SearchBar class="searchbar"></SearchBar>
      <div class="recipes-grid">
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
  </div>
</template>
<script>
import RecipeCard from "@/components/RecipeCard.vue";
import axios from "axios";
import { mapGetters } from "vuex";
import Loading from "@/components/Loading.vue";
import SearchBar from "@/components/SearchBar.vue";

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
    SearchBar,
  },

  computed: {
    ...mapGetters(["currentUser", "getSelectedFilters"]),
    filteredRecipes() {
      return this.getSelectedFilters.length
        ? this.recipes.filter((recipe) =>
            this.getSelectedFilters.every((filter) =>
              recipe.category.includes(filter),
            ),
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
          `http://localhost:5000/api/recipe/otherRecipes/${this.currentUser.displayName}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          },
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

<style scoped>
.recipe-container {
  display: flex;
  flex-direction: column;
  align-content: center;
  gap: 1em;
  margin: 24px;
}

.searchbar {
  align-self: center;
}
</style>
