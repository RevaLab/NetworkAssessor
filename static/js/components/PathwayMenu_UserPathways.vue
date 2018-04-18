<template>
    <div class="user-pathways" v-if="userPathwayEdges">
        <div id="user-pathways-header-and-add">
            <h5>User Pathways</h5>
            <a class="button is-primary" v-on:click="showAddUserPathwayModal">+</a>
            <modal name="add-user-pathway">
                <user-pathway-add-form />
            </modal>
        </div>
        <pathway-menu v-bind:predefinedPathways="false"/>
    </div>
</template>

<script>
    import Swatches from 'vue-swatches'
    import PathwayColorSelector from './PathwayColorSelector.vue'
    import userPathwayAddForm from './UserPathway_AddForm.vue'
    import PathwayMenu from './PathwayMenu.vue'

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
        },
        components: {
            PathwayMenu,
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