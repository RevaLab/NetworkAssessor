<template>
    <div class="pathway-color-selector">
        <div class="pathway query-list" v-if="queryList">
            <p>Query List</p>
            <swatches
                    v-model="color"
                    colors="text-advanced"
                    popover-to="right"
                    shapes="squares"
                    :trigger-style="triggerStyle"
            />
        </div>
        <div class="pathway" v-else>
            <input type="checkbox" id="checkbox" v-model="checked">
            <div class="form__checkbox">
                <label for="checkbox">{{ pathwayName }}</label>
                <swatches
                        v-model="color"
                        colors="text-advanced"
                        popover-to="right"
                        shapes="circles"
                        :trigger-style="triggerStyle"
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
            triggerStyle() {
                let styleOptions = {
                    width: '20px',
                    height: '20px',
                    margin: '5px',
                };

                if (this.queryList) {
                  styleOptions['border-radius'] = '0px'
                }

                return styleOptions;
            },
            queryList () {
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
    .pathway-color-selector {
        border: solid 1px green;
        display: flex;
        flex-direction: column;
        width: 100%;
        margin-left: 0;
        /*float: left;*/
        /*margin-left: 0;*/
    }
/*.pathway-color-selector {*/
    /*display: flex;*/
    /*!*flex-direction: row;*!*/
    /*!*word-wrap: break-word;*!*/
    /*background-color: #5b80b2;*/
/*}*/

/*.pathway {*/
    /*background-color: #6DDCBD;*/
    /*display: flex;*/
    /*flex-direction: row;*/
    /*align-items: center;*/
    /*justify-content: left;*/
    /*width: 100%;*/
/*}*/

/*.query-list {*/
    /*!*border-bottom: solid 1px black;*!*/
    /*justify-content: center;*/
    /*!*width: 100%;*!*/
/*}*/

/*input {*/
    /*margin: auto 5px;*/
    /*!*margin-bottom: auto;*!*/
    /*!*margin-right: 5px;*!*/
    /*!*margin-left: 5px;*!*/
/*}*/

/*.form__checkbox {*/
    /*word-wrap: break-word;*/
    /*display: flex;*/
    /*flex-direction: row;*/
    /*align-items: center;*/
    /*!*justify-content: left;*!*/
    /*!*width: 100%;*!*/
    /*background-color: pink;*/
    /*!*padding-top: auto;*!*/
    /*!*vertical-align: middle;*!*/
    /*!*line-height: 200px;*!*/
    /*!*margin-top: auto;*!*/
    /*!*margin-bottom: auto;*!*/
/*}*/
</style>