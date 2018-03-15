<template>
    <div class="network-controls">
            <div v-if="queryList">
                <span>Query List</span>
                <swatches
                        v-model="color"
                        colors="text-advanced"
                        popover-to="right"
                        shapes="squares"
                />
            </div>
        <div v-else>
            <div class="form__checkbox">
                <input type="checkbox" id="checkbox" v-model="checked">
                <label for="checkbox">{{ pathwayName }}</label>
            </div>
            <div class="color-selector">
                <swatches
                        v-model="color"
                        colors="text-advanced"
                        popover-to="right"
                        shapes="circles"
                />
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
                checked: false,
            }
        },
        props: ['pathwayName'],
        computed: {
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
            queryList () {
                // let isQueryList = ;

                // if (isQueryList) {
                //     const nodes = document.querySelectorAll(`.${this.pathwayName}`);
                //         nodes.forEach(node => {
                //             node.style.fill = this.color;
                //         });
                // }

                return this.pathwayName === 'query-list';
            }
        },
        watch: {
            checked: 'visualizePathway',
            color: 'updateColor'
        },
        components: {
            Swatches,
        },
        mounted () {
            // let queryListColor = this.$store.state.pathwayColors['query-list'];
            // const nodes = document.querySelectorAll('.query-list');
            // nodes.forEach(node => {
            //     node.style.fill = queryListColor;
            // });
        },
        methods: {
            visualizePathway() {
                let selectedPathways = this.$store.state.selectedPathways;
                const queryGenes = this.$store.state.geneInput;

                if (this.checked) {
                    selectedPathways = selectedPathways.concat([this.pathwayName]);
                } else {
                    let pw_index = selectedPathways.indexOf(this.pathwayName);
                    selectedPathways = selectedPathways.splice(1, pw_index);
                }

                const queryGenesPathwayData = {
                    pathways: selectedPathways,
                    queryGenes: queryGenes
                };

                this.$store.dispatch('updateSelectedPathways', selectedPathways);
                this.$store.dispatch('getPathwaySubnetwork', queryGenesPathwayData);
            },
            updateColor() {
                if (this.checked || this.queryList) {
                    const nodes = document.querySelectorAll(`.${this.pathwayName}`);
                    nodes.forEach(node => {
                        node.style.fill = this.color;
                    });
                }
            }
        }
    }
</script>

<style>
.network-controls {
    display: flex;
}

.color-selector {
    margin-left: 5px;
}

</style>