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
                        <!--<a class="delete" v-on:click="removeUserPathway(pathway)"></a>-->
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
                    if (!pathwaysEdgeCounts[pathway]) {
                        return false;
                    }
                }
                return true;
            },
            sortedUserPathways() {
                const userPathways = Object.keys(this.$store.state.userPathways);
                const pathwaysEdgeCounts = this.$store.state.pathwaysEdgeCounts;
                const networkDegree = this.$store.state.networkDegree;

                let sortable = [];

                userPathways.forEach(pathway => {
                    if (pathway === 'query_list') {
                        return;
                    }
                    sortable.push(
                    [
                        pathway,
                        pathwaysEdgeCounts[pathway][networkDegree]
                    ]
                    );
                });


                sortable.sort(function (a, b) {
                    return b[1] - a[1];
                });

                // show query_list as first user pathway
                let ordered_pathways = ['query_list'];
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