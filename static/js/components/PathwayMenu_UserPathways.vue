<template>
    <div class="user-pathways">
        <h2>User Pathways</h2>
        <ul id="pathways-ul">
            <li v-for="(pathwayData, pathway) in userPathways">
                <pathway-color-selector v-bind:pathwayName=pathway />
            </li>
        </ul>
    </div>
</template>

<script>
    import Swatches from 'vue-swatches'
    import PathwayColorSelector from './PathwayColorSelector.vue'

    export default {
        name: "user-pathways",
        computed: {
            userPathways() {
                return this.$store.state.userPathways;
            },
        },
        components: {
            PathwayColorSelector,
            Swatches
        },
        mounted() {

        }
    }
</script>

<style>
    .user-pathways {
        height: 35%;
    }

</style>