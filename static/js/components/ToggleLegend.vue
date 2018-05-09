<template>
  <div class="toggle-legend" id="toggle-legend-content">
    <a class="button is-small legend-button" v-on:click="toggleLegend">{{ buttonLabel }} Legend</a>
  </div>
</template>

<script>
export default {
  name: "toggle-legend",
  data() {
    return {
      shown: true
    }
  },
  computed: {
    buttonLabel() {
      return this.shown ? 'Hide' : 'Show'
    }
  },
  methods: {
    toggleLegend() {
      this.shown = !this.shown;

      const legend = document.getElementById("network-legend");

      if (this.shown) {
        legend.style.display = 'block';
      } else {
        legend.style.display = 'none';
      }
    }
  }
}
</script>

<style>
.toggle-legend {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin: 10px 0;
}

</style>
