<template>
    <div class="network-container">
        <pathway-menu />
        <div id="network-visualization">
            <network />
        </div>
    </div>
</template>

<script>
    import Network from './Network.vue'
    import PathwayMenu from './PathwayMenu.vue'

    export default {
        name: "network-container",
        components: {
            Network,
            PathwayMenu
        }
    }
</script>

<style scoped>
.network-container {
    display: flex
}
</style>