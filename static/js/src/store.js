import Vue from 'vue'
import Vuex from 'vuex'
import api from './api.js'

Vue.use(Vuex) // only required if you're using modules.
              // We're using modules, so there you go.

const store = new Vuex.Store({
    state: {
        geneInput: [],
        listName: '',
        selectedPathways: [],
        subnetwork: {
            nodes: [],
            links: []
        }
    },
    mutations: {
        'ADD_GENE_INPUT' (state, geneInput) {
            state.geneInput = geneInput
        },
        'ADD_SUBNETWORK' (state, subnetwork) {
            state.subnetwork = subnetwork;
        },
        'API_FAIL' (state, error) {
            console.error(error)
        },
        'UPDATE_SELECTED_PATHWAYS' (state, selectedPathways) {
            state.selectedPathways = selectedPathways
        },
    },
    actions: {
        getSubnetwork(store, geneInput) {
            const geneInputArr = geneInput.split('\n');
            geneInput = geneInputArr.join('_n_');
            store.commit('ADD_GENE_INPUT', geneInputArr);
            api
                .get(
                    `/api/subnetwork/submit_genes/${geneInput}`
                )
                .then(
                    response => {
                        store.commit('ADD_SUBNETWORK', response.body)
                    }
                )
                .catch(
                    error => {
                        store.commit('API_FAIL', error)
                    }
                )
        },
        getPathwaySubnetwork(store, queryGenesPathwayData) {
            console.log(queryGenesPathwayData);
            api
                .post(
                    'api/subnetwork/select_pathways/',
                    queryGenesPathwayData
                )
                .then(
                    response => {
                        console.log(response.body)
                        store.commit('ADD_SUBNETWORK', response.body)
                    }
                )
                .catch(
                    error => {
                        store.commit('API_FAIL', error)
                    }
                )
        },
        updateSelectedPathways(store, selectedPathways) {
            store.commit('UPDATE_SELECTED_PATHWAYS', selectedPathways)
        }
    },
});

export default store;