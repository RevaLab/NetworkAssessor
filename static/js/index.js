import Vue from 'vue';
import store from './src/store.js';

import GeneInput from "./components/GeneInput.vue";

const app = new Vue({
    el: '#app',
    components: {
        GeneInput
    },
    store: store
});