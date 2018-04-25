<template>
    <div class="toggle-legend">
        <div id="toggle-legend-content">
            Legend
            <a class="button is-small legend-button" v-on:click="toggleLegend">{{ buttonLabel }}</a>
        </div>
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
    .toggle-legend {
        border: solid 1px yellow;
        display: flex;
        justify-content: space-between;
    }

    #toggle-legend-content {
        display: flex;
        flex-direction: row;
        margin: auto;
    }

    .legend-button {
        margin-left: 10px;
    }
</style>