<template>
    <div class="toggle-legend">
        <span>
            Legend
            <a class="button is-small" v-on:click="toggleLegend">{{ buttonLabel }}</a>
        </span>
    </div>
</template>

<script>
    export default {
        name: "toggle-legend",
        data() {
            return {
               shown: true
            }
        },
        computed: {
            buttonLabel() {
                return this.shown ? 'Hide' : 'Show'
            }
        },
        methods: {
            toggleLegend() {
                this.shown = !this.shown;

                const legend = document.getElementById("network-legend");

                if (this.shown) {
                    legend.style.display = 'block';
                } else {
                    legend.style.display = 'none';
                    console.log('hide legend')
                }
            }
        }
    }
</script>

<style>

</style>