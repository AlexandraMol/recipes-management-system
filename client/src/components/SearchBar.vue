<template>
  <div class="smart-search">
    <div class="search-bar" @click="expanded = true">
      <v-text-field
        v-model="filters.searchText"
        label="Search recipes or ingredients..."
        prepend-inner-icon="mdi-magnify"
        hide-details
        @keyup.enter="searchRecipes"
      />

      <v-btn icon @click.stop="expanded = !expanded">
        <v-icon>mdi-tune</v-icon>
      </v-btn>
    </div>

    <v-expand-transition>
      <div v-if="expanded" class="advanced-panel">
        <v-text-field
          v-model="ingredientInput"
          label="Ingredients you have / Recipe name"
          @keyup.enter="addIncludedIngredient"
        />

        <div class="chips">
          <v-chip
            v-for="ingredient in filters.includedIngredients"
            :key="ingredient"
            closable
            @click:close="removeIncludedIngredient(ingredient)"
          >
            {{ ingredient }}
          </v-chip>
        </div>

        <v-text-field
          v-model="exclusionInput"
          label="Exclude ingredients"
          @keyup.enter="addExcludedIngredient"
        />

        <div class="chips">
          <v-chip
            v-for="ingredient in filters.excludedIngredients"
            :key="ingredient"
            closable
            color="red"
            @click:close="removeExcludedIngredient(ingredient)"
          >
            {{ ingredient }}
          </v-chip>
        </div>

        <v-select
          v-model="filters.categories"
          :items="categories"
          label="Category"
          multiple
          chips
        />

        <v-select
          v-model="filters.difficulties"
          :items="difficulties"
          label="Difficulty"
          multiple
          chips
        />

        <v-text-field
          v-model="filters.maxPreparationTime"
          label="Max preparation time"
          type="number"
          suffix="min"
        />

        <div class="actions">
          <v-btn variant="text" @click="clearFilters"> Clear </v-btn>

          <v-btn color="black" @click="searchRecipes"> Search </v-btn>
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
  VChipGroup,
  VChip,
  VSelect,
  VBtn,
  VExpandTransition,
  VIcon,
} from "vuetify/components";

export default {
  name: "SmartSearchBar",

  emits: ["results"],

  computed: {
    ...mapGetters(["currentUser"]),
  },
  components: {
    VTextField,
    VChipGroup,
    VChip,
    VSelect,
    VBtn,
    VExpandTransition,
    VIcon,
  },

  data() {
    return {
      expanded: false,

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

  methods: {
    addIncludedIngredient() {
      const value = this.ingredientInput.trim().toLowerCase();

      if (value && !this.filters.includedIngredients.includes(value)) {
        this.filters.includedIngredients.push(value);
      }

      this.ingredientInput = "";
    },

    removeIncludedIngredient(ingredient) {
      this.filters.includedIngredients =
        this.filters.includedIngredients.filter((item) => item !== ingredient);
    },

    addExcludedIngredient() {
      const value = this.exclusionInput.trim().toLowerCase();

      if (value && !this.filters.excludedIngredients.includes(value)) {
        this.filters.excludedIngredients.push(value);
      }

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
        excludedIngredients: [],
        categories: [],
        difficulties: [],
        maxPreparationTime: null,
      };

      this.ingredientInput = "";
      this.exclusionInput = "";
    },

    async searchRecipes() {
      const token = await this.currentUser.getIdToken();

      const response = await axios.post(
        "http://localhost:5000/api/recipe/search",
        this.filters,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      this.$emit("results", response.data.data);
      this.expanded = false;
    },
  },
};
</script>
<style>
.smart-search {
  width: 100%;
  max-width: 850px;
  position: relative;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.advanced-panel {
  position: absolute;
  top: 100%;
  left: 0;

  width: 100%;

  z-index: 1000;
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
</style>
