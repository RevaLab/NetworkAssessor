<template>
    <div class="degree-selector">
        <p>Degrees of separation from the query genes:</p>
        <div class="radio-group">
            <input type="radio" id="one" value="first_degree" v-model="picked">
            <label for="one">One</label>
        </div>
        <div class="radio-group">
            <input type="radio" id="two" value="second_degree" v-model="picked">
            <label for="two">Two</label>
        </div>
        <div class="radio-group">
            <input type="radio" id="three" value="third_degree" v-model="picked">
            <label for="three">Three</label>
        </div>
    </div>
</template>

<script>
    export default {
        name: "radio-button",
        data() {
            return {
                picked: 'first_degree'
            }
        },
        watch: {
            picked() {
                this.$store.dispatch('updateDegree', this.picked)
            }
        }
    }
</script>

<style>
    .degree-selector {
        padding: 10px;
        border: solid 1px yellow;
        display: flex;
        flex-direction: row;
        justify-content: space-around;
    }
</style>