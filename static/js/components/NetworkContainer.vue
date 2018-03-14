<template>
    <div class="network-container">
        <pathway-menu />
        <network />
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