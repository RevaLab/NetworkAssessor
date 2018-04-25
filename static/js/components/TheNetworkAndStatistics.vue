<template>
    <div class="network-and-statistics">
        <network />
        <network-legend />
    </div>
</template>

<script>
    import Network from './Network.vue'
    import NetworkLegend from "./NetworkLegend.vue";

    export default {
        name: "network-and-statistics",
        components: {
            NetworkLegend,
            Network
        },
    }
</script>

<style>
    .network-and-statistics {
        width: 78%;
        height: 100%;
    }
</style>