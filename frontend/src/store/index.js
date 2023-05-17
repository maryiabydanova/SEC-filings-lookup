import { createStore } from 'vuex';

export default createStore({
    state: {
        alerts: [],
    },
    mutations: {
        ADD_ALERT(state, alert) {
            state.alerts.push(alert);
            if (!alert.dismissable) {
                setTimeout(() => {
                    state.alerts = state.alerts.filter(a => a.id !== alert.id);
                }, 5000);
            }
        }
    },
    actions: {
        addAlert({ commit }, alert) {
            commit('ADD_ALERT', alert);
        }
    },
});