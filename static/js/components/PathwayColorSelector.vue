<template>
    <div class="network-controls">
            <div class="form__checkbox">
                <input type="checkbox" id="checkbox" v-model="checked">
                <label for="checkbox">{{ pathwayName }}</label>
            </div>
            <div class="color-selector">
                <swatches v-model="color" />
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
                color: '',
                checked: false,
            }
        },
        props: ['pathwayName'],
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
                if (this.checked) {
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