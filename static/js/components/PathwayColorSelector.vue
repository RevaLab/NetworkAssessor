<template>
    <div class="pathway-color-selector">
        <div class="pathway" id="query-list" v-if="queryList">
            <p>Query List</p>
            <swatches
                    v-model="color"
                    colors="text-advanced"
                    popover-to="right"
                    shapes="squares"
                    row-length="5"
                    :trigger-style="triggerStyle"
            />
        </div>
        <div class="pathway" v-else>
            <input type="checkbox" id="pw-checkbox" v-model="checked">
            <div class="label-and-swatch">
                <label for="pw-checkbox">{{ pathwayName }}</label>
                <swatches
                        v-model="color"
                        colors="text-advanced"
                        popover-to="right"
                        shapes="circles"
                        row-length="5"
                        :trigger-style="triggerStyle"
                />
            </div>
            <pathway-statistics v-bind:pathway="pathway"/>
        </div>
    </div>
</template>

<script>
    import Swatches from 'vue-swatches'
    import "vue-swatches/dist/vue-swatches.min.css"
    import pathwayStatistics from './PathwayStatistics.vue'

    export default {
        name: "network-controls",
        data() {
            return {
            }
        },
        props: ['pathway'],
        computed: {
            pathwayName() {
                const displayNames = this.$store.state.pathwayDisplayNames;
                return displayNames[this.pathway]
            },
            checked: {
                get() {
                    let selectedPathways = this.$store.state.selectedPathways;
                    return selectedPathways.includes(this.pathway)
                },
                set() {
                    let selectedPathways = this.$store.state.selectedPathways;

                    const isNotSelected = !selectedPathways.includes(this.pathway);

                    if (isNotSelected) {
                        selectedPathways = selectedPathways.concat([this.pathway]);
                    } else {
                        let pw_index = selectedPathways.indexOf(this.pathway);
                        selectedPathways.splice(pw_index, 1);
                    }

                    this.$store.dispatch('updateSelectedPathways', selectedPathways);
                }
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
            triggerStyle() {
                let styleOptions = {
                    width: '20px',
                    height: '20px',
                    margin: '5px',
                };

                if (this.queryList) {
                    // renders query list selector as a square
                  styleOptions['border-radius'] = '0px'
                }

                return styleOptions;
            },
            queryList () {
                return this.pathway === 'query_list';
            }
        },
        components: {
            Swatches,
            pathwayStatistics
        },
        updated() {
            // let loader = document.getElementById('loader-bg');
            // loader.style.visibility = 'visible';

            const selectedPathways = this.$store.state.selectedPathways;
            const pathwayColors = this.$store.state.pathwayColors;

            if (selectedPathways.includes(this.pathway)) {
                for (let i = 0; i < selectedPathways.length; i ++) {
                    let pathwayToColor = selectedPathways[i];
                    const nodes = document.querySelectorAll(`.${pathwayToColor}`);
                    nodes.forEach(node => {
                        node.style.fill = pathwayColors[pathwayToColor];
                    });
                }
            }
        },
    }
</script>

<style>
    .pathway-color-selector {
        border: solid 1px green;
        display: flex;
        flex-direction: row;
    }

    .pathway {
        display: flex;
        flex-direction: row;
        /*align-items: center;*/
        justify-content: space-between;
    }

    #query-list {
        margin: auto;
    }

    .label-and-swatch {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: left;
    }

    #pw-checkbox {
        margin: auto 5px;
    }
</style>