<template>
  <main class="shopping-page">
    <v-card class="shopping-card" elevation="8">
      <div class="shopping-header">
        <div>
          <p class="eyebrow">Shopping assistant</p>
          <h1>Generate shopping list</h1>
          <p>
            Select recipes from your collection or favorites and generate one
            combined shopping list.
          </p>
        </div>
      </div>

      <div class="shopping-content">
        <section class="picker-section">
          <div class="section-title">
            <div>
              <h2>Select recipes</h2>
              <p>
                {{ selectedRecipeIds.length }} selected from
                {{ allRecipes.length }} available recipes
              </p>
            </div>
          </div>

          <v-text-field
            v-model="recipeSearch"
            prepend-inner-icon="mdi-magnify"
            label="Search by name, category or difficulty"
            variant="outlined"
            density="comfortable"
            hide-details
            class="search-input"
          />

          <div v-if="filteredRecipes.length" class="recipe-list">
            <div
              v-for="recipe in filteredRecipes"
              :key="recipe.id"
              class="recipe-row"
              :class="{ selected: selectedRecipeIds.includes(recipe.id) }"
              @click="toggleRecipe(recipe.id)"
            >
              <div class="recipe-left">
                <v-checkbox
                  :model-value="selectedRecipeIds.includes(recipe.id)"
                  hide-details
                  @click.stop
                  @update:modelValue="toggleRecipe(recipe.id)"
                />

                <v-img
                  :src="recipe.imageUrl"
                  width="72"
                  height="58"
                  cover
                  class="recipe-thumb"
                />

                <div class="recipe-meta">
                  <h4>{{ recipe.name }}</h4>

                  <p>
                    {{ recipe.category?.join(", ") || "No category" }}
                    <span>•</span>
                    {{ recipe.difficulty || "Unknown" }}
                    <span>•</span>
                    {{ recipe.preparationTime || 0 }} min
                  </p>
                </div>
              </div>

              <v-chip
                size="small"
                class="source-chip"
                :class="
                  recipe.source === 'Your recipe' ? 'own-chip' : 'favorite-chip'
                "
              >
                {{ recipe.source }}
              </v-chip>
            </div>
          </div>

          <div v-else class="empty-picker">
            <v-icon size="38">mdi-magnify-close</v-icon>
            <h3>No recipes found</h3>
            <p>Try searching for another recipe.</p>
          </div>
        </section>

        <div class="actions">
          <v-btn
            class="primary-btn"
            :disabled="selectedRecipeIds.length === 0"
            @click="generateShoppingList"
          >
            <v-icon start>mdi-format-list-checks</v-icon>
            Generate list
          </v-btn>

          <v-btn
            v-if="shoppingList.length"
            variant="outlined"
            class="secondary-btn"
            @click="copyShoppingList"
          >
            <v-icon start>mdi-content-copy</v-icon>
            Copy
          </v-btn>

          <v-btn
            v-if="shoppingList.length"
            variant="outlined"
            class="secondary-btn"
            @click="shareOnWhatsApp"
          >
            <v-icon start>mdi-whatsapp</v-icon>
            WhatsApp
          </v-btn>
        </div>

        <section v-if="shoppingList.length" class="shopping-list">
          <div class="list-header">
            <div>
              <h2>Shopping List</h2>
              <p>Combined ingredients from selected recipes.</p>
            </div>

            <span>{{ shoppingList.length }} items</span>
          </div>

          <v-list class="items">
            <v-list-item
              v-for="(item, index) in shoppingList"
              :key="index"
              class="shopping-item"
            >
              <div class="item-left">
                <span class="item-index">{{ index + 1 }}</span>
                <span class="item-name">{{ item.name }}</span>
              </div>

              <strong class="item-quantity">
                {{ item.quantity }} {{ item.unit }}
              </strong>
            </v-list-item>
          </v-list>
        </section>

        <section v-else class="empty-state">
          <v-icon size="46">mdi-cart-outline</v-icon>
          <h3>No shopping list yet</h3>
          <p>Select recipes to generate your ingredient list.</p>
        </section>
      </div>
    </v-card>
  </main>
</template>

<script>
import axios from "axios";
import {
  VBtn,
  VList,
  VListItem,
  VCard,
  VIcon,
  VTextField,
  VChip,
  VCheckbox,
  VImg,
} from "vuetify/components";

import { mapGetters } from "vuex";

export default {
  name: "GenerateShoppingList",

  components: {
    VBtn,
    VList,
    VListItem,
    VCard,
    VIcon,
    VTextField,
    VChip,
    VCheckbox,
    VImg,
  },

  data() {
    return {
      userRecipes: [],
      favoriteRecipes: [],
      recipeSearch: "",
      selectedRecipeIds: [],
      shoppingList: [],
    };
  },

  computed: {
    ...mapGetters(["currentUser"]),

    allRecipes() {
      const own = this.userRecipes.map((recipe) => ({
        ...recipe,
        source: "Your recipe",
      }));

      const favorites = this.favoriteRecipes.map((recipe) => ({
        ...recipe,
        source: "Favorite",
      }));

      return [...own, ...favorites].filter(
        (recipe, index, self) =>
          index === self.findIndex((item) => item.id === recipe.id),
      );
    },

    filteredRecipes() {
      const search = this.recipeSearch.toLowerCase().trim();

      if (!search) return this.allRecipes;

      return this.allRecipes.filter((recipe) => {
        const name = recipe.name?.toLowerCase() || "";
        const category = recipe.category?.join(" ").toLowerCase() || "";
        const difficulty = recipe.difficulty?.toLowerCase() || "";

        return (
          name.includes(search) ||
          category.includes(search) ||
          difficulty.includes(search)
        );
      });
    },

    shoppingListText() {
      return this.shoppingList
        .map(
          (item, index) =>
            `${index + 1}. ${item.name} - ${item.quantity} ${item.unit}`,
        )
        .join("\n");
    },
  },

  mounted() {
    this.getUserRecipes();
    this.getFavoriteRecipes();
  },

  methods: {
    toggleRecipe(id) {
      if (this.selectedRecipeIds.includes(id)) {
        this.selectedRecipeIds = this.selectedRecipeIds.filter(
          (item) => item !== id,
        );
      } else {
        this.selectedRecipeIds.push(id);
      }
    },

    async getUserRecipes() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.get(
          `http://localhost:5000/api/recipe/${this.currentUser.displayName}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );

        if (response.status === 200) {
          this.userRecipes = response.data.data;
        }
      } catch (error) {
        console.error(error.message);
      }
    },

    async getFavoriteRecipes() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.get(
          `http://localhost:5000/api/recipe/favorites/${this.currentUser.displayName}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        if (response.status === 200) {
          this.favoriteRecipes = response.data.data;
        }
      } catch (error) {
        console.log(error);
        this.favoriteRecipes = [];
      }
    },

    async generateShoppingList() {
      if (this.selectedRecipeIds.length === 0) return;

      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.post(
          "http://localhost:5000/api/recipe/shopping-list",
          { recipeIds: this.selectedRecipeIds },
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );

        if (response.status === 200) {
          this.shoppingList = response.data.data;
        }
      } catch (error) {
        console.error(error.message);
      }
    },

    async copyShoppingList() {
      await navigator.clipboard.writeText(this.shoppingListText);
    },

    shareOnWhatsApp() {
      const text = encodeURIComponent(this.shoppingListText);
      window.open(`https://wa.me/?text=${text}`, "_blank");
    },
  },
};
</script>

<style scoped>
.shopping-page {
  --color-primary: #c23000;
  --color-secondary: #fcb10a;
  --color-blue: #14235e;
  --color-light: #f7f2ed;
  --color-dark: #0a0b0f;

  min-height: 100vh;
  padding: 48px 20px;
  background: var(--color-light);
  font-family: "Poppins", sans-serif;
}

.shopping-card {
  max-width: 980px;
  margin: 0 auto;
  border-radius: 30px;
  overflow: hidden;
  background: #fffdfb;
}

.shopping-header {
  padding: 36px;
  background: var(--color-blue);
  color: white;
  border-bottom: 6px solid var(--color-secondary);
}

.eyebrow {
  color: var(--color-secondary);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 12px;
  margin-bottom: 6px;
}

.shopping-header h1 {
  font-size: 36px;
  font-weight: 900;
  margin: 0;
}

.shopping-header p {
  margin-top: 8px;
  opacity: 0.78;
}

.shopping-content {
  padding: 32px;
}

.picker-section {
  background: #fffaf5;
  border: 1px solid #eadccd;
  border-radius: 24px;
  padding: 24px;
}

.section-title {
  display: flex;
  justify-content: space-between;
  margin-bottom: 18px;
}

.section-title h2 {
  color: var(--color-blue);
  font-size: 24px;
  font-weight: 900;
  margin: 0;
}

.section-title p {
  color: #766a60;
  margin-top: 4px;
}

.search-input {
  margin-bottom: 18px;
}

.recipe-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 420px;
  overflow-y: auto;
  padding-right: 6px;
}

.recipe-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  border-radius: 18px !important;
  padding: 12px 16px;
  cursor: pointer;
  background: white;
  border: 1px solid #eadccd;
  transition: 0.2s ease;
}

.recipe-row:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(10, 11, 15, 0.08);
}

.recipe-row.selected {
  border-color: var(--color-primary);
  background: #fff3ec;
}

.recipe-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.recipe-thumb {
  border-radius: 12px;
  flex-shrink: 0;
  background: #f7f2ed;
}

.recipe-meta {
  min-width: 0;
}

.recipe-meta h4 {
  color: var(--color-dark);
  font-weight: 900;
  margin: 0;
}

.recipe-meta p {
  color: #766a60;
  font-size: 13px;
  margin: 4px 0 0;
}

.recipe-meta span {
  margin: 0 5px;
}

.source-chip {
  flex-shrink: 0;
  font-weight: 800;
}

.own-chip {
  background: var(--color-blue) !important;
  color: white !important;
}

.favorite-chip {
  background: var(--color-secondary) !important;
  color: var(--color-dark) !important;
}

.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin: 24px 0;
}

.primary-btn {
  background: var(--color-primary) !important;
  color: white !important;
  border-radius: 999px;
  font-weight: 800;
}

.secondary-btn {
  border-color: #d8c7b7 !important;
  color: var(--color-blue) !important;
  border-radius: 999px;
  font-weight: 700;
}

.shopping-list {
  background: #fffaf5;
  border: 1px solid #eadccd;
  border-radius: 24px;
  padding: 24px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18px;
  margin-bottom: 12px;
}

.list-header h2 {
  color: var(--color-blue);
  font-weight: 900;
  margin: 0;
}

.list-header p {
  color: #766a60;
  margin-top: 4px;
}

.list-header span {
  color: var(--color-primary);
  font-weight: 800;
}

.items {
  background: transparent;
}

.shopping-item {
  border-bottom: 1px solid #eadccd;
  padding: 12px 0;
}

.shopping-item:last-child {
  border-bottom: none;
}

.item-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-index {
  width: 30px;
  height: 30px;
  border-radius: 999px;
  background: var(--color-primary);
  color: white;
  display: grid;
  place-items: center;
  font-weight: 900;
  font-size: 13px;
}

.item-name {
  text-transform: capitalize;
  font-weight: 700;
}

.item-quantity {
  color: var(--color-blue);
  font-weight: 900;
}

.empty-state,
.empty-picker {
  border: 1px dashed #d9c8b8;
  border-radius: 22px;
  padding: 36px;
  text-align: center;
  background: #fffaf5;
  color: #766a60;
}

.empty-picker {
  background: white;
}

.empty-state h3,
.empty-picker h3 {
  color: var(--color-blue);
  margin-top: 10px;
  font-weight: 900;
}

@media (max-width: 700px) {
  .shopping-page {
    padding: 24px 10px;
  }

  .shopping-header {
    padding: 26px;
  }

  .shopping-header h1 {
    font-size: 28px;
  }

  .shopping-content {
    padding: 20px;
  }

  .picker-section,
  .shopping-list {
    padding: 18px;
  }

  .recipe-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .recipe-left {
    width: 100%;
  }

  .source-chip {
    align-self: flex-start;
  }

  .list-header {
    flex-direction: column;
  }
}
</style>
