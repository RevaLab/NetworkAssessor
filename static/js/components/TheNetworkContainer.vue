<template>
    <div class="network-container" id="network-container">
        <div class="controls">
            <network-controls />
            <predefined-pathways />
            <user-pathways />
        </div>
        <network-and-statistics />
    </div>
</template>

<script>
    import NetworkAndStatistics from './TheNetworkAndStatistics.vue';
    import NetworkControls from './NetworkControls.vue';
    import UserPathways from './PathwayMenu_UserPathways.vue';
    import PredefinedPathways from './PathwayMenu_PredefinedPathways.vue';

    export default {
        name: "network-container",
        components: {
            NetworkAndStatistics,
            NetworkControls,
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
        margin: 5px;
        border-bottom: none;
        font-size: small;
        background-color: lightgrey;
        padding: 10px;
        box-sizing: border-box;
    }
</style>
