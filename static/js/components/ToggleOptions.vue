<template>
    <div class="toggle-options">
        <toggle-legend />
        <toggle-isolates />
    </div>
</template>

<script>
    import ToggleIsolates from "./ToggleIsolates.vue"
    import ToggleLegend from "./ToggleLegend.vue"

    export default {
        name: "toggle-options",
        components: {
            ToggleIsolates,
            ToggleLegend
        }
    }
</script>

<style scoped>
.toggle-options {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    margin: 10px;
}
</style>