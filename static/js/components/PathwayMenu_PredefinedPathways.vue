<template>
    <div class="predefined-pathways">
        <h5>Major Cancer Pathways</h5>
        <div id="predefined-pathway-menu">
            <pathway-menu v-bind:predefinedPathways="true" />
        </div>
    </div>
</template>

<script>
    import PathwayMenu from './PathwayMenu.vue'


    export default {
        name: "predefined-pathways",
        components: {
            PathwayMenu,
        }
    }
</script>

<style>
#predefined-pathway-menu {
    /*background-color: #5b80b2;*/
    height: 55vh;
    overflow-y: scroll;
}
</style>