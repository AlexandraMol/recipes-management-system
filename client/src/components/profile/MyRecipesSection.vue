<template>
  <div class="my-recipes-section">
    <div class="toolbar">
      <v-text-field
        v-model="search"
        label="Search your recipes"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        density="comfortable"
        hide-details
      />

      <v-select
        v-model="selectedCategory"
        :items="categories"
        label="Category"
        variant="outlined"
        density="comfortable"
        hide-details
        clearable
      />

      <v-select
        v-model="selectedDifficulty"
        :items="difficulties"
        label="Difficulty"
        variant="outlined"
        density="comfortable"
        hide-details
        clearable
      />
    </div>

    <div v-if="filteredRecipes.length" class="recipes-grid">
      <RecipeCard
        class="profile-recipe-card"
        v-for="recipe in filteredRecipes"
        :key="recipe.id"
        :recipe="recipe"
        :isOwnRecipe="true"
        @recipe-deleted="$emit('recipe-deleted', $event)"
      />
    </div>

    <div v-else class="empty-state">
      <v-icon size="42">mdi-food-fork-drink</v-icon>
      <h3>No recipes found</h3>
      <p>Try changing your search filters or add a new recipe.</p>

      <v-btn class="primary-btn" @click="$router.push('/add-recipe')">
        <v-icon start>mdi-plus</v-icon>
        Add recipe
      </v-btn>
    </div>
  </div>
</template>

<script>
import { VTextField, VSelect, VBtn, VIcon } from "vuetify/components";

import RecipeCard from "@/components/RecipeCard.vue";

export default {
  name: "MyRecipesSection",

  components: {
    VTextField,
    VSelect,
    VBtn,
    VIcon,
    RecipeCard,
  },
  emits: ["recipe-deleted"],
  props: {
    recipes: {
      type: Array,
      default: () => [],
    },
  },

  data() {
    return {
      search: "",
      selectedCategory: null,
      selectedDifficulty: null,
      categories: ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"],
      difficulties: ["Easy", "Medium", "Hard"],
    };
  },

  computed: {
    filteredRecipes() {
      return this.recipes.filter((recipe) => {
        const matchesSearch =
          !this.search ||
          recipe.name?.toLowerCase().includes(this.search.toLowerCase());

        const matchesCategory =
          !this.selectedCategory ||
          recipe.category?.includes(this.selectedCategory);

        const matchesDifficulty =
          !this.selectedDifficulty ||
          recipe.difficulty === this.selectedDifficulty;

        return matchesSearch && matchesCategory && matchesDifficulty;
      });
    },
  },
};
</script>

<style scoped>
.profile-recipe-card {
  min-width: 350px;
}
.my-recipes-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.toolbar {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr;
  gap: 14px;
}

.recipes-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.empty-state {
  border: 1px dashed #d9c8b8;
  border-radius: 20px;
  padding: 32px;
  text-align: center;
  background: #fffaf5;
  color: #756d66;
}

.empty-state h3 {
  color: #14235e;
  margin-top: 10px;
  font-weight: 900;
}

.primary-btn {
  background: #c23000 !important;
  color: white !important;
  border-radius: 999px;
  font-weight: 800;
  margin-top: 12px;
}

@media (max-width: 1000px) {
  .toolbar,
  .recipes-grid {
    grid-template-columns: 1fr;
  }
}
</style>
