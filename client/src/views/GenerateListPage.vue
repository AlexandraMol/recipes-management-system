<template>
  <v-container class="container-generate-list">
    <h2>Select recipes you want to prepare:</h2>
    <v-select
      v-model="selectedRecipeIds"
      :items="userRecipes"
      item-title="name"
      item-value="id"
      label="Recipes"
      multiple
    ></v-select>

    <v-btn color="black" @click="generateShoppingList">
      Get Shopping List
    </v-btn>

    <div class="shopping-list" v-if="shoppingList.length > 0">
      <h2>Shopping List</h2>
      <v-list class="items">
        <v-list-item v-for="(item, index) in shoppingList" :key="index">
          <span> {{ index + 1 }}. {{ item.name }} : {{ item.quantity }} </span>
        </v-list-item>
      </v-list>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import {
  VContainer,
  VSelect,
  VBtn,
  VList,
  VListItem,
} from "vuetify/lib/components/index.mjs";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      userRecipes: [],
      selectedRecipeIds: [],
      shoppingList: [],
    };
  },
  components: {
    VContainer,
    VSelect,
    VBtn,
    VList,
    VListItem,
  },
  computed: {
    ...mapGetters(["currentUser"]),
  },
  mounted() {
    this.getUserRecipes();
  },
  methods: {
    async getUserRecipes() {
      try {
        const token = await this.currentUser.getIdToken();
        const response = await axios.get(
          `http://localhost:3000/api/recipe/${this.currentUser.displayName}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        if (response.status === 200) {
          this.userRecipes = response.data.data;
        }
      } catch (error) {
        console.error(error.message);
      }
    },

    async generateShoppingList() {
      if (this.selectedRecipeIds.length === 0) return;

      try {
        const token = await this.currentUser.getIdToken();
        const response = await axios.post(
          `http://localhost:3000/api/recipe/shopping-list`,
          { recipeIds: this.selectedRecipeIds },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        if (response.status === 200) {
          this.shoppingList = response.data.data;
        }
      } catch (error) {
        console.error(error.message);
      }
    },
  },
};
</script>
<style scoped>
.container-generate-list {
  display: flex;
  flex-direction: column;
  gap: 1em;
  width: 50%;
}

.shopping-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid black;
  border-radius: 10px;
}

.items {
  align-self: baseline;
  margin: 5px;
}

@media (max-width: 500px) {
  .container-generate-list {
    width: 100%;
  }
}
</style>
