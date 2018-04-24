<template>
    <div class="user-pathways">
        <div id="user-pathways-header-and-add">
            <h5>User Pathways</h5>
            <a class="button is-primary" v-on:click="showAddUserPathwayModal">+</a>
            <modal name="add-user-pathway">
                <user-pathway-add-form />
            </modal>
        </div>
        <!--<div id="user-pathway-menu">-->
            <pathway-menu v-bind:predefinedPathways="false"/>
        <!--</div>-->
    </div>
</template>

<script>
    import userPathwayAddForm from './UserPathway_AddForm.vue'
    import PathwayMenu from './PathwayMenu.vue'

    export default {
        name: "user-pathways",
        computed: {
        },
        components: {
            PathwayMenu,
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
        /*height: 35%;*/
        /*overflow-y: scroll;*/
    }

    #user-pathways-header-and-add {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

    #user-pathway-menu {
        height: 20vh;
        overflow-y: scroll;
    }
</style>