<template>
  <div class="degree-selector">
    <div>Degrees of separation from the query genes:</div>
    <div class="radio-group-container">
      <div class="radio-group">
        <input type="radio" id="one" value="first_degree" v-model="picked">
        <label for="one">One</label>
      </div>
      <div class="radio-group">
        <input type="radio" id="two" value="second_degree" v-model="picked">
        <label for="two">Two</label>
      </div>
      <div class="radio-group">
        <input type="radio" id="three" value="third_degree" v-model="picked">
        <label for="three">Three</label>
      </div>
      <div class="radio-group">
        <input type="radio" id="whole" value="whole" v-model="picked">
        <label for="whole">Whole</label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "radio-button",
  data() {
    return {
    }
  },
  computed: {
    picked: {
      get() {
        return this.$store.state.networkDegree
      },
      set(degree) {
        this.$store.dispatch('updateDegree', degree)
      }
    }
  },
  updated() {
  }
}
</script>

<style>
.degree-selector {
  display: flex;
  flex-direction: column;
}

.radio-group-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 10px 0;
}

</style>
