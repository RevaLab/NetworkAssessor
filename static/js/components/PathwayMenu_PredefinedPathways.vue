<template>
  <div class="predefined-pathways">
    <div class="predefined-pathways-header">
      <div>Major Cancer Pathways</div>
      <multiple-pathway-selector />
    </div>
    <div id="predefined-pathway-menu">
      <pathway-menu v-bind:predefinedPathways="true" />
    </div>
  </div>
</template>

<script>
import PathwayMenu from './PathwayMenu.vue'
import MultiplePathwaySelector from './MultiplePathwaySelector.vue'


export default {
  name: "predefined-pathways",
  components: {
    PathwayMenu,
    MultiplePathwaySelector
  }
}
</script>

<style>
.predefined-pathways-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
}

.predefined-pathways-header {
  font-size: 1.2em;
}
</style>
