<template>
    <div class="network-container">
        <div class="controls">
            <network-controls />
            <pathway-menu />
        </div>
        <network />
    </div>
</template>

<script>
    import Network from './Network.vue'
    import NetworkControls from './NetworkControls.vue'
    import PathwayMenu from './PathwayMenu.vue'

    export default {
        name: "network-container",
        components: {
            Network,
            NetworkControls,
            PathwayMenu
        }
    }
</script>

<style scoped>
.network-container {
    display: flex
}
</style>