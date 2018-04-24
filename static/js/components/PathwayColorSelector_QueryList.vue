<template>
        <div class="pathway-query-list" id="query-list">
            <p>Query List</p>
            <swatches
                    v-model="color"
                    colors="text-advanced"
                    popover-to="right"
                    shapes="squares"
                    row-length="5"
                    :trigger-style="triggerStyle"
                    :exceptions="exceptions"
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
              exceptions: ['#00ff00'],
              // triggerStyle: {
              //       width: '20px',
              //       height: '20px',
              //       margin: '5px',
              //       'border-radius': '0px'
              //   }
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

    #query-list {
        display: flex;
        flex-direction: row;
        /*justify-content: space-around;*/
        margin: auto;
        /*height: 3vh;*/
    }
</style>