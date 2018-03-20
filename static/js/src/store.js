import Vue from 'vue'
import Vuex from 'vuex'
import api from './api.js'

Vue.use(Vuex) // only required if you're using modules.
              // We're using modules, so there you go.

const store = new Vuex.Store({
    state: {
        geneInput: ['test','gello'],
        listName: '',
        networkDegree: 'first_degree',
        networkDatabase: 'hprd',
        selectedPathways: ['query-list'],
        subnetwork: {},
        pathwayColors: {
            'query-list': '#dd7e6b',
            'AKT_ext_path': '#ff9900',
            'Apoptosis_path': '#ffff00',
            'Apoptosis_ext_path': '#00ff00',
            'CALC_PKC_ext_path': '#00ffff',
            'Cellular_Architecture_and_Microenvironment_path': '#4a86e8',
            'Cell_Cycle_Control_path': '#0000ff',
            'Cell_Cycle_ext_path': '#9900ff',
            'Chromatin_Remodeling-DNA_Methylation_path': '#ff00ff',
            'DNA_Damage_path': '#ff00ff',
            'ERK_ext_path': '#f9cb9c',
            'G-Protein_Signaling_path': '#ffe599',
            'Hedgehog_Signaling_path': '#b6d7a8',
            'HIPPO_ext_path': '#a2c4c9',
            'Hormone_Signaling_path': '#b4a7d6',
            'Immune_Checkpoints_path': '#d5a6bd',
            'B-Catenin-WNT_Signaling_path': '#e06666',
            'Jack_Stat_ext_path': '#f6b26b',
            'Janus_Kinase_JAK-or-Signal_Transducers_and_Activators_of_Transcription_STAT_path': '#ffd966',
            'Kinase_Fusions_path': '#93c47d',
            'Metabolic_Signaling_path': '#45818e',
            'NFKB_ext_path': '#3d85c6',
            'Notch_ext_path': '#674ea7',
            'PI3K-AKT1-MTOR_Signaling_path': '#741b47',
            'Protein_Degradation_Ubiquitination_path': '#d9d2e9',
            'RNA_Splicing_path': '#783f04',
            'TGF-B_Signaling_path': '#bf9000',
            'TGFB_ext_path': '#0c343d',
            'WNT_ext_path': '#1155cc',
            'Mitogen_Activated_Protein-MAP_Kinase_Signaling_path': '#4c1130'
        },
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
        'UPDATE_NETWORK_DEGREE' (state, degree) {
            state.networkDegree = degree;
        },
        'UPDATE_NETWORK_DATABASE' (state, database) {
            state.networkDatabase = database;
        },
        'UPDATE_PATHWAY_COLOR' (state, pathway_color_data) {
            let pathway = pathway_color_data['pathway'];
            let color = pathway_color_data['color'];
            state.pathwayColors[pathway] = color;
        },
        'UPDATE_SELECTED_PATHWAYS' (state, selectedPathways) {
            state.selectedPathways = selectedPathways
        },
    },
    actions: {
        addGeneInput(store, geneInput) {
            store.commit('ADD_GENE_INPUT', geneInput);
        },
        getPathwaySubnetwork(store, queryGenesPathwayData) {
            const selectedPathways = queryGenesPathwayData['pathways'];
            store.commit('UPDATE_SELECTED_PATHWAYS', selectedPathways);
            // queryGenesPathwayData['networkDatabase'] = 'hprd';
            api
                .post(
                    'api/subnetwork/submit_genes/',
                    queryGenesPathwayData
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
        updateDatabase(store, database) {
          store.commit('UPDATE_NETWORK_DATABASE', database)
        },
        updateDegree(store, degree) {
            store.commit('UPDATE_NETWORK_DEGREE', degree)
        },
        updateSelectedPathways(store, selectedPathways) {
            store.commit('UPDATE_SELECTED_PATHWAYS', selectedPathways)
        },
        updatePathwayColors(store, pathway_color_data) {
            store.commit('UPDATE_PATHWAY_COLOR', pathway_color_data)
        },
    },
});

export default store;