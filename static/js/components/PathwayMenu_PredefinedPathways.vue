<template>
  <div class="predefined-pathways">
    <div class="predefined-pathways-header">
      <div class="header-and-selector">
        Major Cancer Pathways
        <multiple-pathway-selector />
      </div>
      <div class="hover-caption">{{ labelHover }}</div>
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
  },
    computed: {
      labelHover() {
        return this.$store.state.labelHover;
      }
    }
}
</script>

<style>
  .header-and-selector {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }

  .hover-caption {
    text-align: right;
    font-size: small;
    font-style: italic;
    padding-top: 5px;
  }
  /*.predefined-pathways-header {*/


    /*padding: 10px 0;*/
  /*}*/

  .predefined-pathways-header {
    font-size: 1.2em;
  }
</style>
