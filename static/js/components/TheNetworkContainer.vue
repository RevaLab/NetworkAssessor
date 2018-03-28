<template>
    <div class="network-container">
        <div class="controls">
            <network-controls />
            <pathway-menu />
            <user-pathways />
        </div>
        <network />
    </div>
</template>

<script>
    import Network from './Network.vue'
    import NetworkControls from './NetworkControls.vue'
    import PathwayMenu from './PathwayMenu.vue'
    import UserPathways from './PathwayMenu_UserPathways.vue'

    export default {
        name: "network-container",
        components: {
            Network,
            NetworkControls,
            PathwayMenu,
            UserPathways,
        }
    }
</script>

<style>
    .network-container {
        display: flex;
        flex-direction: row;
    }

    .controls {
        display: flex;
        flex-direction: column;
        width: 22%;
        height: 95vh;
        overflow-y: scroll;
        margin: 5px;
        border: solid 1px black;
        font-size: small;
    }
</style>