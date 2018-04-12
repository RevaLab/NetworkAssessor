<template>
    <div class="user-pathways">
        <div id="user-pathways-header-and-add">
            <h2>User Pathways</h2>
            <a class="button is-primary" v-on:click="showAddUserPathwayModal">+</a>
            <modal name="add-user-pathway">
                <user-pathway-add-form />
            </modal>
        </div>
        <div class="user-pathway-menu" v-if="userPathwayEdges">
            <ul id="pathways-ul">
                    <li v-for="pathway in sortedUserPathways" v-bind:key="pathway" >
                            <pathway-color-selector v-bind:pathway="pathway" />
                            <a class="delete" v-on:click="removeUserPathway(pathway)"></a>
                    </li>
            </ul>
        </div>
    </div>
</template>

<script>
    import Swatches from 'vue-swatches'
    import PathwayColorSelector from './PathwayColorSelector.vue'
    import userPathwayAddForm from './UserPathway_AddForm.vue'


    export default {
        name: "user-pathways",
        computed: {
            userPathwayEdges() {
                const userPathways = this.$store.state.userPathways;
                const pathwaysEdgeCounts = this.$store.state.pathwaysEdgeCounts;

                for (let pathway in userPathways) {
                    // alert(pathway)
                    if (!pathwaysEdgeCounts[pathway]) {
                // alert('returning false')
                        return false;
                    }
                }
                // alert('returning true')
                return true;
            },
            sortedUserPathways() {
                const userPathways = Object.keys(this.$store.state.userPathways);
                const pathwaysEdgeCounts = this.$store.state.pathwaysEdgeCounts;
                const networkDegree = this.$store.state.networkDegree;

                let sortable = [];

                // pathwayMemberCounts selects only the curated cancer pathways, since
                // for now it seems the edges are not being calculated correctly for user pws

                // SHRINK THIS FOR DOWN TO THE GROUP
                userPathways.forEach(pathway => {
                    alert(pathway)
                    // console.log(userPathways)
                    // console.log(pathwaysEdgeCounts)
                    // console.log(pathwaysEdgeCounts[pathway])
                    // if (pathwaysEdgeCounts[pathway]) {
                        sortable.push(
                            [
                                pathway,
                                pathwaysEdgeCounts[pathway][networkDegree]
                            ]
                        );
                    // }
                  });


                sortable.sort(function (a, b) {
                    return b[1] - a[1];
                });

                let ordered_pathways = [];
                sortable.forEach(pathway => {
                    ordered_pathways.push(pathway[0])
                });
                return ordered_pathways;
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
                let userPathways = Object.assign({}, this.$store.state.userPathways);

                // remove user pathway from list in store
                delete userPathways[pathway];
                this.$store.dispatch('updateUserPathways', userPathways);

                // remove user pathway display data
                const displayData = {
                  pathways: {},
                  add: false
                };
                displayData['pathways'][pathway] = pathway;

                this.$store.dispatch(
                    'updateUserPathwayDisplay',
                    displayData
                );

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