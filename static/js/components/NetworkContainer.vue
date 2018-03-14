<template>
    <div class="network-container">
        <pathway-color-selector />
        <network />
    </div>
</template>

<script>
    import Network from './Network.vue'
    import PathwayColorSelector from './PathwayColorSelector.vue'

    export default {
        name: "network-container",
        components: {
            Network,
            PathwayColorSelector
        }
    }
</script>

<style scoped>
.network-container {
    display: flex
}
</style>