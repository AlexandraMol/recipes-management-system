<template>
  <div class="profile-recipe-section">
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
        v-for="recipe in recipes"
        :key="recipe.id"
        :recipe="recipe"
        :isOwnRecipe="false"
      />
    </div>

    <div v-else class="empty-state">
      <v-icon size="42">{{ icon }}</v-icon>

      <h3>{{ emptyTitle }}</h3>
      <p>{{ emptyText }}</p>

      <v-btn class="primary-btn" @click="$router.push('/explore')">
        <v-icon start>mdi-compass-outline</v-icon>
        Explore recipes
      </v-btn>
    </div>
  </div>
</template>

<script>
import { VTextField, VSelect, VBtn, VIcon } from "vuetify/components";
import RecipeCard from "@/components/RecipeCard.vue";

export default {
  name: "ProfileRecipeSection",

  components: {
    RecipeCard,
    VTextField,
    VSelect,
    VBtn,
    VIcon,
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

  props: {
    recipes: {
      type: Array,
      default: () => [],
    },
    emptyTitle: {
      type: String,
      default: "No recipes yet",
    },
    emptyText: {
      type: String,
      default: "Explore recipes and save the ones you like.",
    },
    icon: {
      type: String,
      default: "mdi-food-fork-drink",
    },
  },
};
</script>

<style scoped>
.profile-recipe-section {
  width: 100%;
}

.recipes-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.empty-state {
  border: 1px dashed #d9c8b8;
  border-radius: 20px;
  padding: 34px;
  text-align: center;
  background: #fffaf5;
  color: #756d66;
}

.empty-state h3 {
  color: #14235e;
  margin-top: 10px;
  font-weight: 900;
}

.empty-state p {
  margin: 8px 0 18px;
}

.toolbar {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr;
  gap: 14px;
}

.primary-btn {
  background: #c23000 !important;
  color: white !important;
  border-radius: 999px;
  font-weight: 800;
}

@media (max-width: 1100px) {
  .recipes-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 650px) {
  .toolbar,
  .recipes-grid {
    grid-template-columns: 1fr;
  }
}
</style>
