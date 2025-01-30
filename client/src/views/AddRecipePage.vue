<template>
  <div>
    <RecipeForm :isEditing="false" />
  </div>
</template>

<script>
import RecipeForm from "@/components/RecipeForm.vue";

export default {
  components: {
    RecipeForm,
  },
};
</script>
