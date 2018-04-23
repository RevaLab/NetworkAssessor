<template>
    <div class="user-pathways">
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
        },
        components: {
            PathwayMenu,
            // PathwayColorSelector,
            // Swatches,
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