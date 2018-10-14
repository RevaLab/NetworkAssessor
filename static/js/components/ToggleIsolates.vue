<template>
    <div class="toggle-isolates">
        <a class="button is-small" v-on:click="toggleIsolates">{{ buttonLabel }} Query List Isolates</a>
    </div>
</template>

<script>
    export default {
        name: "toggle-isolates",
        data() {
            return {
              shown: false
            }
        },
        computed: {
            buttonLabel() {
             return this.shown ? 'Hide' : 'Show'
            }
        },
        methods: {
            toggleIsolates() {
                this.shown = !this.shown;

                this.$store.dispatch('updateShowIsolates', this.shown)
            }
        }
    }
</script>

<style scoped>

</style>