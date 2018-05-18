<template>
  <div class="network-container" id="network-container">
    <div class="controls">
      <network-controls />
      <predefined-pathways />
      <user-pathways />
    </div>
    <network-and-statistics />
  </div>
</template>

<script>
import NetworkAndStatistics from './TheNetworkAndStatistics.vue';
import NetworkControls from './NetworkControls.vue';
import UserPathways from './PathwayMenu_UserPathways.vue';
import PredefinedPathways from './PathwayMenu_PredefinedPathways.vue';

export default {
  name: "network-container",
  components: {
    NetworkAndStatistics,
    NetworkControls,
    UserPathways,
    PredefinedPathways,
  }
}
</script>

<style>
.network-container {
  display: flex;
  flex-direction: row;
  overflow: hidden;
}

.controls {
  display: flex;
  flex-direction: column;
  min-width: 300px;
  max-height: calc(100vh - 100px);
  margin: 5px;
  /*border-bottom: none;*/
  font-size: small;
  background-color: lightgrey;
  padding: 10px;
  box-sizing: border-box;
  overflow: auto;
}
</style>
