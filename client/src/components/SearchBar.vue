<template>
  <div class="smart-search">
    <!-- Quick search -->
    <div class="search-bar">
      <v-text-field
        v-model="filters.searchText"
        label="Search recipes, ingredients or categories..."
        prepend-inner-icon="mdi-magnify"
        hide-details
        @keyup.enter="searchRecipes"
      />

      <v-btn icon @click.stop="expanded = !expanded">
        <v-icon>mdi-tune</v-icon>
      </v-btn>
    </div>

    <!-- Advanced filters -->
    <v-expand-transition>
      <div v-if="expanded" class="advanced-panel">
        <!-- Available ingredients -->
        <v-text-field
          class="text-field"
          v-model="ingredientInput"
          label="Ingredients you have"
          placeholder="e.g. chicken, rice, tomato"
          hint="Separate multiple ingredients with commas"
          persistent-hint
          @keyup.enter="addIncludedIngredient"
        />

        <div v-if="filters.includedIngredients.length" class="chips">
          <v-chip
            v-for="ingredient in filters.includedIngredients"
            :key="ingredient"
            closable
            @click:close="removeIncludedIngredient(ingredient)"
          >
            {{ ingredient }}
          </v-chip>
        </div>

        <!-- Temporary exclusions -->
        <div class="filter-group">
          <v-text-field
            class="text-field"
            v-model="exclusionInput"
            label="Excluded ingredients"
            placeholder="e.g. peanuts, mushrooms"
            hint="Your saved preferences are included by default. Remove them for this search if needed."
            persistent-hint
            @keyup.enter="addExcludedIngredient"
          />

          <div v-if="filters.excludedIngredients.length" class="chips">
            <v-chip
              v-for="ingredient in filters.excludedIngredients"
              :key="ingredient"
              closable
              class="excluded-chip"
              @click:close="removeExcludedIngredient(ingredient)"
            >
              {{ ingredient }}
            </v-chip>
          </div>
        </div>

        <!-- Category -->
        <v-select
          v-model="filters.categories"
          :items="categories"
          label="Category"
          multiple
          chips
          clearable
        />

        <!-- Difficulty -->
        <v-select
          v-model="filters.difficulties"
          :items="difficulties"
          label="Difficulty"
          multiple
          chips
          clearable
        />

        <!-- Preparation time -->
        <v-text-field
          v-model="filters.maxPreparationTime"
          label="Maximum preparation time"
          type="number"
          suffix="min"
          min="1"
        />

        <div class="actions">
          <v-btn variant="text" @click="clearFilters"> Clear </v-btn>

          <v-btn class="primary-btn" @click="searchRecipes"> Search </v-btn>
        </div>
      </div>
    </v-expand-transition>

    <div v-if="expanded" class="search-backdrop" @click="expanded = false" />
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

import {
  VTextField,
  VChip,
  VSelect,
  VBtn,
  VExpandTransition,
  VIcon,
} from "vuetify/components";

export default {
  name: "SmartSearchBar",

  components: {
    VTextField,
    VChip,
    VSelect,
    VBtn,
    VExpandTransition,
    VIcon,
  },

  emits: ["results"],

  data() {
    return {
      expanded: false,

      profileExcludedIngredients: [],

      ingredientInput: "",
      exclusionInput: "",

      categories: ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"],

      difficulties: ["Easy", "Medium", "Hard"],

      filters: {
        searchText: "",
        includedIngredients: [],
        excludedIngredients: [],
        categories: [],
        difficulties: [],
        maxPreparationTime: null,
      },
    };
  },

  computed: {
    ...mapGetters(["currentUser"]),
  },

  mounted() {
    this.getUserPreferences();
  },

  methods: {
    addIncludedIngredient() {
      const ingredients = this.ingredientInput
        .split(",")
        .map((ingredient) => ingredient.trim().toLowerCase())
        .filter(Boolean);

      ingredients.forEach((ingredient) => {
        if (!this.filters.includedIngredients.includes(ingredient)) {
          this.filters.includedIngredients.push(ingredient);
        }
      });

      this.ingredientInput = "";
    },

    removeIncludedIngredient(ingredient) {
      this.filters.includedIngredients =
        this.filters.includedIngredients.filter((item) => item !== ingredient);
    },

    addExcludedIngredient() {
      const ingredients = this.exclusionInput
        .split(",")
        .map((ingredient) => ingredient.trim().toLowerCase())
        .filter(Boolean);

      ingredients.forEach((ingredient) => {
        if (!this.filters.excludedIngredients.includes(ingredient)) {
          this.filters.excludedIngredients.push(ingredient);
        }
      });

      this.exclusionInput = "";
    },

    removeExcludedIngredient(ingredient) {
      this.filters.excludedIngredients =
        this.filters.excludedIngredients.filter((item) => item !== ingredient);
    },

    clearFilters() {
      this.filters = {
        searchText: "",
        includedIngredients: [],
        excludedIngredients: [...this.profileExcludedIngredients],
        categories: [],
        difficulties: [],
        maxPreparationTime: null,
      };

      this.ingredientInput = "";
      this.exclusionInput = "";

      this.searchRecipes();
    },

    async getUserPreferences() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.get(
          "http://localhost:5000/api/user/preferences",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        const excludedIngredients =
          response.data.data?.excludedIngredients || [];

        this.profileExcludedIngredients = [...excludedIngredients];

        this.filters.excludedIngredients = [...excludedIngredients];
      } catch (error) {
        console.error("Failed to load user preferences:", error);
      }
    },

    async searchRecipes() {
      try {
        // Add text still present in the ingredient fields
        // before performing the search.
        if (this.ingredientInput.trim()) {
          this.addIncludedIngredient();
        }

        if (this.exclusionInput.trim()) {
          this.addExcludedIngredient();
        }

        const token = await this.currentUser.getIdToken();

        const response = await axios.post(
          `http://localhost:5000/api/recipe/search/${this.currentUser.displayName}`,
          this.filters,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          },
        );

        this.$emit("results", response.data.data);

        this.expanded = false;
      } catch (error) {
        console.error("Recipe search failed:", error);
      }
    },
  },
};
</script>

<style scoped>
.smart-search {
  width: 100%;
  max-width: 850px;
  position: relative;
  z-index: 1000;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.text-field {
  padding: 0;
  margin: 5px;
}

.advanced-panel {
  position: absolute;
  top: 100%;
  left: 0;

  width: 100%;

  z-index: 1001;
  margin-top: 12px;
  padding: 20px;

  border-radius: 18px;
  background: white;

  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.excluded-chip {
  background: #fff1f0 !important;
  color: var(--color-primary) !important;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.search-backdrop {
  position: fixed;
  inset: 0;

  background: rgba(0, 0, 0, 0.15);

  z-index: 999;
}

@media (max-width: 700px) {
  .advanced-panel {
    max-height: 75vh;
    overflow-y: auto;
  }
}
</style>
