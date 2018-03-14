import Vue from 'vue';
import VueRouter from 'vue-router';

import store from './src/store.js';

import App from './App.vue'
import GeneInput from "./components/GeneInput.vue";
import NetworkContainer from "./components/NetworkContainer.vue";


Vue.use(VueRouter);

const routes = [
    { path: '/', component: GeneInput },
    { path: '/network', component: NetworkContainer }
];

const router = new VueRouter({ routes });

const app = new Vue({
    el: '#app',
    router: router,
    store: store,
    render: h => h(App)
});