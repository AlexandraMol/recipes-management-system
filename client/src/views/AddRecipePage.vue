<!-- TODO: refactor code, make responsive for phone, treat errors, move rules to data, get Token universal -->
<template>
  <div class="container-add-recipe">
    <h1 class="recipe-header">Recipe formular</h1>

    <v-form v-model="valid" @submit.prevent="submitForm">
      <v-container>
        <h3>General information:</h3>
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
            label="Dificulty"
            :rules="[(v) => !!v || 'Dificulty is required']"
          ></v-select>

          <v-text-field
            v-model="recipe.preparationTime"
            label="Preparation time (minutes)"
            type="number"
            :rules="[(v) => !!v || 'Preparation time is required']"
          ></v-text-field>
        </div>
        <v-select
          v-model="recipe.category"
          label="Category"
          :items="['Cina', 'Pranz', 'Mic dejun', 'Gustare', 'Desert']"
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
                label="Nume ingredient"
                :rules="[(v) => !!v || 'Numele ingredientului este necesar']"
              ></v-text-field>

              <v-text-field
                v-model="ingredient.quantity"
                label="Cantitate"
                type="number"
                :rules="[(v) => !!v || 'Cantitatea este necesara']"
              ></v-text-field>
            </div>

            <v-btn @click="removeIngredient(index)" color="red" class="mb-5"
              >Remove Ingredient</v-btn
            >
          </div>
        </v-list>

        <h3>Steps:</h3>
        <div>
          <v-btn @click="addStep" color="green" class="mt-1">Add Step</v-btn>
        </div>

        <v-list>
          <div v-for="(step, index) in recipe.steps" :key="index">
            <v-textarea
              v-model="step.description"
              :rules="[(v) => !!v || 'Step description is required']"
              label="Description"
              rows="2"
            ></v-textarea>
            <v-btn @click="removeStep(index)" color="red" class="mb-5">
              Remove Step
            </v-btn>
          </div>
        </v-list>
      </v-container>
      <v-btn color="black" type="submit">Create Recipe</v-btn>
    </v-form>
  </div>
</template>

<script>
import axios from "axios";
import {
  VContainer,
  VForm,
  VTextField,
  VSelect,
  VBtn,
  VTextarea,
  VList,
} from "vuetify/components";
import { mapGetters } from "vuex";

export default {
  components: {
    VContainer,
    VForm,
    VTextField,
    VSelect,
    VBtn,
    VTextarea,
    VList,
  },
  computed: {
    ...mapGetters(["currentUser"]),
  },
  data() {
    return {
      valid: false,
      recipe: {
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
          const response = await axios.post(
            "http://localhost:3000/api/recipe/add",
            this.recipe,
            {
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            }
          );
          if (response.status === 201) {
            this.$router.push("/home");
          }
        } catch (error) {
          console.log(error);
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

.v-form {
  width: 50%;
  align-items: center;
  display: flex;
  flex-direction: column;
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
</style>
