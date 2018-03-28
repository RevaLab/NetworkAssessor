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
            <div class="pw-statistics">
                <div class="tooltip">
                    <p>{{ pathwayMemberCount }}</p>
                    <span class="tooltiptext">Pathway Members</span>
                </div>
                <div class="tooltip">
                    <p v-if="pathwayEdgesReady">{{ pathwayEdgeCount }}</p>
                    <span class="tooltiptext">Total graph edges if you add this pw</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Swatches from 'vue-swatches'
    import "vue-swatches/dist/vue-swatches.min.css"

    export default {
        name: "network-controls",
        data() {
            return {
            }
        },
        props: ['pathwayName'],
        computed: {
            pathwayEdgesReady() {
              return this.$store.state.pathwaysEdgeCounts[this.pathwayName]
            },
            pathwayEdgeCount() {
                const networkDegree = this.$store.state.networkDegree;
                return this.$store.state.pathwaysEdgeCounts[this.pathwayName][networkDegree]
            },
            pathwayMemberCount() {
                return this.$store.state.pathwayMemberCounts[this.pathwayName]
            },
            checked: {
                get() {
                    let selectedPathways = this.$store.state.selectedPathways;
                    return selectedPathways.includes(this.pathwayName)
                },
                set() {
                    let selectedPathways = this.$store.state.selectedPathways;
                    const queryGenes = this.$store.state.geneInput;
                    const networkDatabase = this.$store.state.networkDatabase;

                    const isNotSelected = !selectedPathways.includes(this.pathwayName);

                    if (isNotSelected) {
                        selectedPathways = selectedPathways.concat([this.pathwayName]);
                    } else {
                        let pw_index = selectedPathways.indexOf(this.pathwayName);
                        selectedPathways.splice(pw_index, 1);
                    }

                    const queryGenesPathwayData = {
                        pathways: selectedPathways,
                        queryGenes: queryGenes,
                        networkDatabase
                    };

                    // console.log(selectedPathways)
                    // console.log(this.$store.state.selectedPathways)
                    // this.$store.dispatch('updateSelectedPathways', selectedPathways);
                    this.$store.dispatch('getPathwaySubnetwork', queryGenesPathwayData);
                }
            },
            color: {
              get() {
                  return this.$store.state.pathwayColors[this.pathwayName]
              },
              set(hexValue) {
                  let pathway_color_data = {
                      pathway: this.pathwayName,
                      color: hexValue
                  };

                  this.$store.dispatch('updatePathwayColors', pathway_color_data)
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
                return this.pathwayName === 'query-list';
            }
        },
        components: {
            Swatches,
        },
        updated() {
            // let loader = document.getElementById('loader-bg');
            // loader.style.visibility = 'visible';

            const selectedPathways = this.$store.state.selectedPathways;
            const pathwayColors = this.$store.state.pathwayColors;

            if (selectedPathways.includes(this.pathwayName)) {
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

    .tooltip {
    /*position: relative;*/
        display: inline-block;
        border-bottom: 1px dotted black;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;

        /* Position the tooltip */
        position: absolute;
        z-index: 1;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
    }

    .pw-statistics {
        justify-content: right;
    }
</style>