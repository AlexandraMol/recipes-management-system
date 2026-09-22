<template>
  <div class="recipes-section">
    <!-- Filters -->
    <div v-if="showFilters" class="recipe-toolbar">
      <v-text-field
        v-model="search"
        :label="searchLabel"
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

    <!-- Recipes -->
    <div v-if="filteredRecipes.length" class="recipes-grid">
      <RecipeCard
        v-for="recipe in filteredRecipes"
        :key="recipe.id"
        :recipe="recipe"
        :isOwnRecipe="isOwnRecipe"
        @recipe-deleted="handleRecipeDeleted"
      />
    </div>

    <!-- Empty state -->
    <div v-else class="empty-state">
      <v-icon size="42">
        {{ icon }}
      </v-icon>

      <h3>{{ emptyTitle }}</h3>
      <p>{{ emptyText }}</p>

      <v-btn
        v-if="showEmptyAction"
        class="primary-btn"
        @click="$router.push(emptyActionRoute)"
      >
        <v-icon start>
          {{ emptyActionIcon }}
        </v-icon>

        {{ emptyActionText }}
      </v-btn>
    </div>
  </div>
</template>

<script>
import { VTextField, VSelect, VBtn, VIcon } from "vuetify/components";

import RecipeCard from "@/components/RecipeCard.vue";

export default {
  name: "RecipeCollection",

  components: {
    RecipeCard,
    VTextField,
    VSelect,
    VBtn,
    VIcon,
  },

  emits: ["recipe-deleted"],

  props: {
    recipes: {
      type: Array,
      default: () => [],
    },

    isOwnRecipe: {
      type: Boolean,
      default: false,
    },

    showFilters: {
      type: Boolean,
      default: true,
    },

    searchLabel: {
      type: String,
      default: "Search recipes",
    },

    emptyTitle: {
      type: String,
      default: "No recipes found",
    },

    emptyText: {
      type: String,
      default: "Try changing your filters.",
    },

    icon: {
      type: String,
      default: "mdi-food-fork-drink",
    },

    showEmptyAction: {
      type: Boolean,
      default: true,
    },

    emptyActionText: {
      type: String,
      default: "Explore recipes",
    },

    emptyActionIcon: {
      type: String,
      default: "mdi-compass-outline",
    },

    emptyActionRoute: {
      type: String,
      default: "/explore",
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

  methods: {
    handleRecipeDeleted(recipeId) {
      if (this.isOwnRecipe) {
        this.$emit("recipe-deleted", recipeId);
      }
    },
  },
};
</script>

<style scoped>
.recipes-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
