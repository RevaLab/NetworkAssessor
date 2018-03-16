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

<style>
    .network-container {
        display: flex;
        flex-direction: row;
    }

    /*network {*/
        /*width: 80%;*/
    /*}*/

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
/*.network-container {*/
    /*!*display: table;*!*/
    /*display: flex;*/
    /*flex-direction: row;*/
    /*width: 22%;*/
    /*min-width: 150px;*/
    /*border: solid black 1px;*/
    /*margin: 5px;*/
    /*background-color: #5E5694;*/
/*}*/

</style>