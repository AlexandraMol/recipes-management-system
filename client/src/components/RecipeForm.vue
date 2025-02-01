<template>
  <div class="container-add-recipe">
    <Toaster ref="toaster" />
    <h1 class="recipe-header">
      {{ isEditing ? "Edit Recipe" : "Create Recipe" }}
    </h1>

    <v-form class="recipe-form" v-model="valid" @submit.prevent="submitForm">
      <v-container>
        <h3>General Information:</h3>
        <div class="row">
          <v-text-field
            v-model="recipe.name"
            label="Name"
            :rules="[(v) => !!v || 'Name is required']"
          ></v-text-field>

          <v-select
            v-model="recipe.visibility"
            :items="['Public', 'Private']"
            label="Visibility"
            :rules="[(v) => !!v || 'Visibility is required']"
          ></v-select>
        </div>

        <div class="row">
          <v-select
            v-model="recipe.difficulty"
            :items="['Easy', 'Medium', 'Hard']"
            label="Difficulty"
            :rules="[(v) => !!v || 'Difficulty is required']"
          ></v-select>

          <v-text-field
            v-model="recipe.preparationTime"
            label="Preparation Time (minutes)"
            type="number"
            :rules="[(v) => !!v || 'Preparation time is required']"
          ></v-text-field>
        </div>

        <v-select
          v-model="recipe.category"
          label="Category"
          :items="['Breakfast', 'Lunch', 'Dinner', 'Snack', 'Dessert']"
          multiple
          :rules="[(v) => !!v || 'Category is required']"
        ></v-select>

        <h3>Ingredients:</h3>
        <v-btn @click="addIngredient" color="green" class="mb-5 mt-1"
          >Add Ingredient</v-btn
        >
        <v-list>
          <div v-for="(ingredient, index) in recipe.ingredients" :key="index">
            <div class="row">
              <v-text-field
                v-model="ingredient.name"
                label="Ingredient Name"
                :rules="[(v) => !!v || 'Ingredient name is required']"
              ></v-text-field>

              <v-text-field
                v-model="ingredient.quantity"
                label="Quantity"
                type="number"
                :rules="[(v) => !!v || 'Quantity is required']"
              ></v-text-field>
            </div>

            <v-btn @click="removeIngredient(index)" color="red" class="mb-5"
              >Remove Ingredient</v-btn
            >
          </div>
        </v-list>

        <h3>Steps:</h3>
        <v-btn @click="addStep" color="green" class="mt-1">Add Step</v-btn>

        <v-list>
          <div v-for="(step, index) in recipe.steps" :key="index">
            <v-textarea
              v-model="step.description"
              :rules="[(v) => !!v || 'Step description is required']"
              label="Description"
              rows="4"
            ></v-textarea>
            <v-btn @click="removeStep(index)" color="red" class="mb-5"
              >Remove Step</v-btn
            >
          </div>
        </v-list>
      </v-container>

      <v-btn color="black" type="submit">{{
        isEditing ? "Update Recipe" : "Create Recipe"
      }}</v-btn>
    </v-form>
  </div>
</template>

<script>
import {
  VContainer,
  VForm,
  VTextField,
  VSelect,
  VBtn,
  VTextarea,
  VList,
} from "vuetify/components";
import axios from "axios";
import { mapGetters } from "vuex";
import Toaster from "@/components/Toaster.vue";

export default {
  props: {
    existingRecipe: Object,
    isEditing: Boolean,
  },
  components: {
    VContainer,
    VForm,
    VTextField,
    VSelect,
    VBtn,
    VTextarea,
    VList,
    Toaster,
  },
  computed: {
    ...mapGetters(["currentUser"]),
  },
  data() {
    return {
      valid: false,
      recipe: this.existingRecipe
        ? { ...this.existingRecipe }
        : {
            name: "",
            difficulty: "",
            preparationTime: "",
            ingredients: [],
            steps: [],
            visibility: "Private",
            category: [],
            username: "",
          },
    };
  },
  methods: {
    addIngredient() {
      this.recipe.ingredients.push({ name: "", quantity: "" });
    },
    removeIngredient(index) {
      this.recipe.ingredients.splice(index, 1);
    },
    addStep() {
      this.recipe.steps.push({ description: "" });
    },
    removeStep(index) {
      this.recipe.steps.splice(index, 1);
    },
    async submitForm() {
      if (this.valid) {
        this.recipe.username = this.currentUser.displayName;
        const token = await this.currentUser.getIdToken();
        try {
          if (this.isEditing) {
            await axios.put(
              `http://localhost:3000/api/recipe/edit/${this.$route.params.id}`,
              this.recipe,
              {
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`,
                },
              }
            );
          } else {
            await axios.post(
              "http://localhost:3000/api/recipe/add",
              this.recipe,
              {
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`,
                },
              }
            );
          }
          this.$router.push("/home");
        } catch (error) {
          this.$refs.toaster.showToast(
            error?.response?.data?.error || error.message
          );
        }
      }
    },
  },
};
</script>

<style scoped>
.recipe-header {
  margin-top: 1em;
}
.recipe-form {
  width: 50%;
  align-items: center;
  display: flex;
  flex-direction: column;
  margin: 1em;
}
.container-add-recipe {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1em;
}
.text-center {
  text-align: center;
}
.row {
  display: flex;
  gap: 10px;
}

@media (max-width: 900px) {
  .recipe-form {
    width: 100%;
  }
}
</style>
