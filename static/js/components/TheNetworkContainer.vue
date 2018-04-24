<template>
    <div class="network-container" id="network-container">
        <div class="controls">
            <network-controls />
            <predefined-pathways />
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
    import PredefinedPathways from './PathwayMenu_PredefinedPathways.vue'

    export default {
        name: "network-container",
        components: {
            Network,
            NetworkControls,
            PathwayMenu,
            UserPathways,
            PredefinedPathways,
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
        width: 300px;
        height: 95vh;
        /*overflow-y: scroll;*/
        margin: 5px;
        /*border: solid 1px black;*/
        border-bottom: none;
        font-size: small;
    }
</style>