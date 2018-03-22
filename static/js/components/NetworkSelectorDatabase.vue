<template>
    <div class="db-selector">
        <p>PPI Database:</p>
        <div class="radio-group">
            <input type="radio" id="hprd" value="hprd" v-model="picked">
            <label for="hprd">HPRD</label>
        </div>
        <div class="radio-group">
            <input type="radio" id="biogrid" value="biogrid" v-model="picked">
            <label for="biogrid">BioGRID</label>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                // picked: 'hprd'
            }
        },
        computed: {
            picked: {
                get() {
                    return this.$store.state.networkDatabase
                },
                set(database) {
                    const pathways = this.$store.state.selectedPathways;
                    const queryGenes = this.$store.state.geneInput;

                    const queryGenesPathwayData = {
                        pathways,
                        queryGenes,
                        networkDatabase: database
                    };

                    this.$store.dispatch('updateDatabase', database);
                    this.$store.dispatch('getPathwaySubnetwork', queryGenesPathwayData);
                }
            }
        },
        // watch: {
        //     picked() {
        //     }
        // }
    }
</script>

<style>
    .db-selector {
        padding: 10px;
        border: solid 1px yellow;
        display: flex;
        flex-direction: row;
        justify-content: space-around;
    }
</style>