<template>
    <div class="network-controls">
        <div class="form__field">
            <div class="form__checkbox">
                <input type="checkbox" id="checkbox" v-model="checked">
                <label for="checkbox">{{ pathwayName }}</label>
            </div>
            <div class="form__input">
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
                const selectedPathways = this.$store.state.selectedPathways.concat([this.pathwayName]);
                const queryGenes = this.$store.state.geneInput;

                if (this.checked) {
                    const queryGenesPathwayData = {
                        pathways: selectedPathways,
                        queryGenes
                    };
                    this.$store.dispatch('getPathwaySubnetwork', queryGenesPathwayData);
                    this.$store.dispatch('addPathway', this.pathwayName);
                } else {
                    console.log('unchecked')

                    // this.$store.dispatch('removePathway', this.pathwayName)
                }
            },
            updateColor() {
                if (this.checked) {
                    const nodes = document.querySelectorAll('.query-list');
                    // querySelectorAll(.pathwayName)
                    nodes.forEach(node => {
                        node.style.fill = this.color;
                    });
                }
            }
        }
    }
</script>

<style scoped>

</style>