<template>
    <div class="user-pathways">
        <div id="user-pathways-header-and-add">
            <h2>User Pathways</h2>
            <a class="button is-primary" v-on:click="showAddUserPathwayModal">+</a>
            <modal name="add-user-pathway">
                <user-pathway-add-form />
            </modal>
        </div>
        <ul id="pathways-ul">
            <li v-for="(pathwayData, pathway) in userPathways" v-bind:key="pathway" v-bind:id="pathway + '-li'">
                <pathway-color-selector v-bind:pathway="pathway" />
                <a class="delete" v-on:click="removeUserPathway(pathway)"></a>
            </li>
        </ul>
    </div>
</template>

<script>
    import Swatches from 'vue-swatches'
    import PathwayColorSelector from './PathwayColorSelector.vue'
    import userPathwayAddForm from './UserPathway_AddForm.vue'

    export default {
        name: "user-pathways",
        computed: {
            userPathways() {
                return this.$store.state.userPathways;
            },
        },
        components: {
            PathwayColorSelector,
            Swatches,
            userPathwayAddForm
        },
        methods: {
            showAddUserPathwayModal() {
                this.$modal.show('add-user-pathway')
            },
            removeUserPathway(pathway) {
                let userPathways = this.$store.state.userPathways;

                // remove user pathway from list in store
                delete userPathways[pathway];
                this.$store.dispatch('updateUserPathways', userPathways);

                const displayData = {
                  pathways: {},
                  add: false
                };
                displayData['pathways'][pathway] = pathway;

                this.$store.dispatch(
                    'updatePathwayDisplayNames',
                    displayData
                );

                // remove user pathway from DOM
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
    }
</script>

<style>
    .user-pathways {
        height: 35%;
    }

    #user-pathways-header-and-add {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

</style>