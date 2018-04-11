import Vue from 'vue'
import Vuex from 'vuex'
import api from './api.js'

Vue.use(Vuex) // only required if you're using modules.
              // We're using modules, so there you go.

const store = new Vuex.Store({
    state: {
        geneInput: [],
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
            'Receptor_Tyrosine_KinaseORGrowth_Factor_Signaling_path': '#000000',
            'TGF-B_Signaling_path': '#bf9000',
            'TGFB_ext_path': '#0c343d',
            'WNT_ext_path': '#1155cc',
            'Mitogen_Activated_Protein-MAP_Kinase_Signaling_path': '#4c1130'
        },
        pathwaysEdgeCounts: {},
        pathwayMemberCounts: {
            'AKT_ext_path': 20,
            'Apoptosis_path': 10,
            'Apoptosis_ext_path': 31,
            'CALC_PKC_ext_path': 18,
            'Cellular_Architecture_and_Microenvironment_path': 2,
            'Cell_Cycle_Control_path': 30,
            'Cell_Cycle_ext_path': 87,
            'Chromatin_Remodeling-DNA_Methylation_path': 19,
            'DNA_Damage_path': 24,
            'ERK_ext_path': 40,
            'G-Protein_Signaling_path': 6,
            'Hedgehog_Signaling_path': 3,
            'HIPPO_ext_path': 31,
            'Hormone_Signaling_path': 5,
            'Immune_Checkpoints_path': 12,
            'B-Catenin-WNT_Signaling_path': 14,
            'Jack_Stat_ext_path': 21,
            'Janus_Kinase_JAK-or-Signal_Transducers_and_Activators_of_Transcription_STAT_path': 12,
            'Kinase_Fusions_path': 12,
            'Metabolic_Signaling_path': 17,
            'NFKB_ext_path': 12,
            'Notch_ext_path': 19,
            'PI3K-AKT1-MTOR_Signaling_path': 16,
            'Protein_Degradation_Ubiquitination_path': 8,
            'Receptor_Tyrosine_KinaseORGrowth_Factor_Signaling_path': 38,
            'RNA_Splicing_path': 4,
            'TGF-B_Signaling_path': 7,
            'TGFB_ext_path': 19,
            'WNT_ext_path': 92,
            'Mitogen_Activated_Protein-MAP_Kinase_Signaling_path': 14
        },
        predefinedPathways: ['query-list', 'AKT_ext_path', 'Apoptosis_path', 'Apoptosis_ext_path', 'CALC_PKC_ext_path', 'Cellular_Architecture_and_Microenvironment_path', 'Cell_Cycle_Control_path', 'Cell_Cycle_ext_path', 'Chromatin_Remodeling-DNA_Methylation_path', 'DNA_Damage_path', 'ERK_ext_path', 'G-Protein_Signaling_path', 'Hedgehog_Signaling_path', 'HIPPO_ext_path', 'Hormone_Signaling_path', 'Immune_Checkpoints_path', 'B-Catenin-WNT_Signaling_path', 'Jack_Stat_ext_path', 'Janus_Kinase_JAK-or-Signal_Transducers_and_Activators_of_Transcription_STAT_path', 'Kinase_Fusions_path', 'Metabolic_Signaling_path', 'NFKB_ext_path', 'Notch_ext_path', 'PI3K-AKT1-MTOR_Signaling_path', 'Protein_Degradation_Ubiquitination_path', 'Receptor_Tyrosine_KinaseORGrowth_Factor_Signaling_path', 'RNA_Splicing_path', 'TGF-B_Signaling_path', 'TGFB_ext_path', 'WNT_ext_path', 'Mitogen_Activated_Protein-MAP_Kinase_Signaling_path'],
        userPathways: {},
        pathwayDisplayNames: {
            'AKT_ext_path': 'AKT Extension',
            'Apoptosis_path': 'Apoptosis',
            'Apoptosis_ext_path': 'Apoptosis Extension',
            'CALC_PKC_ext_path': 'CALC-PKC Extension',
            'Cellular_Architecture_and_Microenvironment_path': 'Cellular Architecture and Microenvironment',
            'Cell_Cycle_Control_path': 'Cell Cycle Control',
            'Cell_Cycle_ext_path': 'Cell Cycle Extension',
            'Chromatin_Remodeling-DNA_Methylation_path': 'Chromatin Remodeling-DNA Methylation',
            'DNA_Damage_path': 'DNA Damage',
            'ERK_ext_path': 'ERK Extension',
            'G-Protein_Signaling_path': 'G-Protein Signaling',
            'Hedgehog_Signaling_path': 'Hedgehog Signaling',
            'HIPPO_ext_path': 'HIPPO Extension',
            'Hormone_Signaling_path': 'Hormone Signaling',
            'Immune_Checkpoints_path': 'Immune Checkpoints',
            'B-Catenin-WNT_Signaling_path': 'B-Catenin-WNT Signaling',
            'Jack_Stat_ext_path': 'JAK-STAT Extension',
            'Janus_Kinase_JAK-or-Signal_Transducers_and_Activators_of_Transcription_STAT_path': 'JAK-STAT',
            'Kinase_Fusions_path': 'Kinase Fusions',
            'Metabolic_Signaling_path': 'Metabolic Signaling',
            'NFKB_ext_path': 'NFKB Extension',
            'Notch_ext_path': 'Notch Extension',
            'PI3K-AKT1-MTOR_Signaling_path': 'PI3K-AKT1-MTOR Signaling',
            'Protein_Degradation_Ubiquitination_path': 'Protein Degradation-Ubiquitination',
            'Receptor_Tyrosine_KinaseORGrowth_Factor_Signaling_path': 'RTK/Growth Factor Signaling',
            'RNA_Splicing_path': 'RNA Splicing',
            'TGF-B_Signaling_path': 'TGF-B Signaling',
            'TGFB_ext_path': 'TGFB Extension',
            'WNT_ext_path': 'WNT Extension',
            'Mitogen_Activated_Protein-MAP_Kinase_Signaling_path': 'MAP Kinase Signaling'
        },
    },
    mutations: {
        'ADD_GENE_INPUT' (state, geneInput) {
            state.geneInput = geneInput
        },
        'ADD_PATHWAYS_EDGE_COUNTS' (state, pathwaysEdgeCounts) {
            state.pathwaysEdgeCounts = pathwaysEdgeCounts
        },
        'ADD_SUBNETWORK' (state, subnetwork) {
            state.subnetwork = subnetwork;
        },
        'UPDATE_USER_PATHWAY_COLORS' (state, userPathwayColors) {
            let raw = state.pathwayColors;
            let allowed = state.predefinedPathways;

            const filtered = Object.keys(raw)
              .filter(key => allowed.includes(key))
              .reduce((obj, key) => {
                obj[key] = raw[key];
                return obj;
              }, {});

            state.pathwayColors = {...filtered, ...userPathwayColors}
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
            const { pathway, color } = pathway_color_data;
            state.pathwayColors[pathway] = color;
        },
        'UPDATE_PATHWAY_DISPLAY_NAMES' (state, displayData) {
            const { pathways, add } = displayData;
            if(add) {
                state.pathwayDisplayNames = {...state.pathwayDisplayNames, ...pathways}
            } else {
                for (let pathway in pathways) {
                    delete state.pathwayDisplayNames[pathway]
                }
            }
        },
        'UPDATE_SELECTED_PATHWAYS' (state, selectedPathways) {
            state.selectedPathways = selectedPathways
        },
        'UPDATE_USER_PATHWAYS' (state, userPathways) {
            state.userPathways = userPathways
        }
    },
    actions: {
        addGeneInput(store, geneInput) {
            store.commit('ADD_GENE_INPUT', geneInput);
        },
        getPathwaySubnetwork(store, queryGenesPathwayData) {
            const selectedPathways = queryGenesPathwayData['pathways'];
            store.commit('UPDATE_SELECTED_PATHWAYS', selectedPathways);
            api
                .post(
                    'api/subnetwork/submit_genes/',
                    queryGenesPathwayData
                )
                .then(
                    response => {
                        // console.log(response.body)
                        store.commit('ADD_SUBNETWORK', response.body['interaction_networks']);
                        store.commit('ADD_PATHWAYS_EDGE_COUNTS', JSON.parse(response.body['pathways_edge_counts']));
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
        updateUserPathways(store, userPathways) {
            store.commit('UPDATE_USER_PATHWAYS', userPathways);
            let pathwayColors = {};
            for (let pathway in userPathways) {
                pathwayColors[pathway] = userPathways[pathway]['color'];
            }
            store.commit('UPDATE_USER_PATHWAY_COLORS', pathwayColors)
        },
        updatePathwayDisplayNames(store, displayData) {
            store.commit('UPDATE_PATHWAY_DISPLAY_NAMES', displayData)
        }
    },
});

export default store;