<template>
    <div class="user-pathways">
        <h2>User Pathways</h2>
        <ul id="pathways-ul">
            <li v-for="(pathwayData, pathway) in userPathways" v-bind:key="pathway" v-bind:id="pathway + '-li'">
                <pathway-color-selector v-bind:pathwayName=pathway />
                <a class="delete" v-on:click="removeUserPathway(pathway)"></a>
            </li>
        </ul>
    </div>
</template>

<script>
    import Swatches from 'vue-swatches'
    import PathwayColorSelector from './PathwayColorSelector.vue'

    export default {
        name: "user-pathways",
        computed: {
            userPathways() {
                return this.$store.state.userPathways;
            },
        },
        components: {
            PathwayColorSelector,
            Swatches
        },
        methods: {
            removeUserPathway(pathway) {
                const userPathways = this.$store.state.userPathways;

                // remove user pathway from list
                let currentUserPathways = this.$store.state.userPathways;
                delete currentUserPathways[pathway];
                this.$store.dispatch('updateUserPathways', currentUserPathways);

                const pathwayId = pathway + '-li';
                let allPathways = document.getElementById('pathways-ul');
                const pathwayToRemove = document.getElementById(pathwayId);
                allPathways.removeChild(pathwayToRemove);

                // remove user pathway from selected pathways
                let selectedPathways = this.$store.state.selectedPathways;
                let pw_index = selectedPathways.indexOf(pathway);
                if (pw_index !== -1) {
                    selectedPathways.splice(pw_index, 1);


                    const queryGenes = this.$store.state.geneInput;
                    const networkDatabase = this.$store.state.networkDatabase;

                    const queryGenesPathwayData = {
                        pathways: selectedPathways,
                        queryGenes,
                        networkDatabase,
                        userPathways
                    };

                    this.$store.dispatch('getPathwaySubnetwork', queryGenesPathwayData);
                }

                // update pathways in local storage
                this.$ls.set('userPathways', JSON.stringify(userPathways));
            }
        },
        mounted() {

        },
        updated() {
            // let loader = document.getElementById('loader-bg');
            // loader.style.visibility = 'visible';


        },
    }
</script>

<style>
    .user-pathways {
        height: 35%;
    }

    .user-pathway-li{
        display: flex;
        flex-direction: row;
    }

</style>