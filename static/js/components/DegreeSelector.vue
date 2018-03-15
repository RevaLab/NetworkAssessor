<template>
    <div class="degree-selector">
        <input type="radio" id="one" value="first_degree" v-model="picked">
        <label for="one">One</label>
        <br>
        <input type="radio" id="two" value="second_degree" v-model="picked">
        <label for="two">Two</label>
        <br>
        <input type="radio" id="three" value="third_degree" v-model="picked">
        <label for="three">Three</label>
        <br>
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

</style>