<template>
    <div class="predefined-pathways">
        <h5>Major Cancer Pathways</h5>
        <multiple-pathway-selector />
        <div id="predefined-pathway-menu">
            <pathway-menu v-bind:predefinedPathways="true" />
        </div>
    </div>
</template>

<script>
    import PathwayMenu from './PathwayMenu.vue'
    import MultiplePathwaySelector from './MultiplePathwaySelector.vue'


    export default {
        name: "predefined-pathways",
        components: {
            PathwayMenu,
            MultiplePathwaySelector

        }
    }
</script>

<style>
    .predefined-pathways {
        border: solid 1px black;
        border-top: none;
    }

    #predefined-pathway-menu {
        /*background-color: #5b80b2;*/
        height: 55vh;
        overflow-y: scroll;
    }
</style>