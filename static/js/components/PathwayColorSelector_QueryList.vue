<template>
  <div class="pathway-query-list" id="query-list">
    <div>Query List</div>
    <swatches
      class="query-list-swatch"
      v-model="color"
      colors="text-advanced"
      popover-to="right"
      shapes="squares"
      row-length="5"
      :trigger-style="triggerStyle"
    />
    <pathway-statistics v-bind:pathway="pathway"/>
  </div>
</template>

<script>
    import Swatches from 'vue-swatches'
    import "vue-swatches/dist/vue-swatches.min.css"
    import pathwayStatistics from './PathwayStatistics.vue'

    export default {
        name: "pathway-color-selector-query-list",
        data() {
          return {
              pathway: 'query_list',
          }
        },
        components: {
            Swatches,
            pathwayStatistics
        },
        computed: {
            triggerStyle() {
                let style = {
                    width: '20px',
                    height: '20px',
                    margin: '5px',
                };

                style['border-radius'] = '0px';

                return style
            },
            color: {
              get() {
                  return this.$store.state.pathwayColors[this.pathway]
              },
              set(hexValue) {
                  let pathwayColorData = {};
                  pathwayColorData[this.pathway] = hexValue;

                  this.$store.dispatch('updatePathwayColors', pathwayColorData)
              }
            },
        }
    }
</script>

<style>
  .pathway-query-list {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
  }

  .query-list-swatch {
    margin: 0 10px;
  }
</style>
