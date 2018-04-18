<template>
    <div class="predefined-pathways">
        <h5>Major Cancer Pathways</h5>
        <pathway-menu v-bind:predefinedPathways="true"/>
    </div>
</template>

<script>
    import PathwayMenu from './PathwayMenu.vue'

    export default {
        name: "predefined-pathways",
        components: {
            PathwayMenu
        }
    }
</script>

<style scoped>

</style>