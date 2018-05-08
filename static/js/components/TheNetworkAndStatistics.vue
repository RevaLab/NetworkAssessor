<template>
  <div class="network-and-statistics">
    <network />
    <network-legend />
  </div>
</template>

<script>
import Network from './Network.vue'
import NetworkLegend from "./NetworkLegend.vue";

export default {
  name: "network-and-statistics",
  components: {
    NetworkLegend,
    Network
  },
}
</script>

<style>
.network-and-statistics {
  height: calc(100vh - 110px);
  width: calc(100vw - 300px);
  border: 1px solid black;
  margin: 10px;
}

</style>
