import Vue from 'vue'
import Vuex from 'vuex'
import api from './api.js'

Vue.use(Vuex) // only required if you're using modules.
              // We're using modules, so there you go.

const store = new Vuex.Store({
    state: {
        geneInput: [],
        listName: '',
    },
    mutations: {

    },
    actions: {
        getSubnetwork(store, geneInput) {
            console.log('fetching subnetwork');
            console.log(geneInput);
            geneInput = geneInput.split('\n').join('_n_');
            api.get(
                `/api/subnetwork/${geneInput}`
            ).then(
                response => {
                    console.log(response);
                }
            )
        }
    },
});

export default store;