<template>
    <div class="Demo">
        <input v-model="message" placeholder="edit me">
        <p>Message is: {{ message }}</p>

        <button @click='clickHandle'>click me</button>
    </div>
</template>

<script>
    import api from '../src/api.js'

    export default {
        data() {
            return {
                message: ""
            }
        },
        methods: {
            clickHandle() {
                alert('clicked!');
                api.get("/go_annotation/")
                    .then(response => { console.log(response) });
            }
        }
    };
</script>

<style>
</style>