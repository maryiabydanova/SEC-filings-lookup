import { createStore } from 'vuex';
import axios from '@/plugins/axios';

export default createStore({
    state: {
        alerts: [],
        companyFilings: [],
        companies: [],
        companyMetadata: null,
        companyFilingTypes: []
    },
    mutations: {
        ADD_ALERT(state, alert) {
            state.alerts.push(alert);
            if (!alert.dismissable) {
                setTimeout(() => {
                    state.alerts = state.alerts.filter(a => a.id !== alert.id);
                }, 5000);
            }
        },
        SET_COMPANY_FILINGS(state, filings) {
          const regex = /\/(\d+)\/(\d+)-(\d+)-(\d+)\.txt$/;
          state.companyFilings = filings.map((l) => {
            console.log('filing', l)
            const match = l.match(regex);
            let linkText = '';
            let cik = ''
            let reportYear;
            if (match) {
              cik = match[2];
              reportYear = match[3];
              linkText = `${cik} - year: ${reportYear}`;

            }
            return {
              text: linkText,
              url: l,
              year: reportYear,
              key: `${cik}-${reportYear}`
            }
      
          }).sort((l1, l2) => l2.year - l1.year )
        },
        SET_COMPANIES(state, searchResult) {
          state.companies = searchResult;
        },
        SET_COMPANY_METADATA(state, selectedCompany) {
          state.companyMetadata = selectedCompany
        }
    },
    actions: {
        addAlert({ commit, dispatch }, alert) {
          commit('ADD_ALERT', alert);
        },
        async getCompanyFilings({ commit, dispatch }, companyCIK) {
            try {
              let response = await axios.post(`get_company_filings/`, { cik: companyCIK});
              if(response.message) {
                dispatch('addAlert', {message: response.message, id: Math.random()})
              } else {
                commit('SET_COMPANY_FILINGS', response.data);
                dispatch('preloadCompanyFilingsYear')
              }
            } catch (err) {
              console.error(err)
            }
        },
        async preloadCompanyFilingsYear({ commit }) {
          let lastYearFilings = this.state.companyFilings[0];
          try {
            let response = await axios.post(`get_filing_data/`, {
              'url': lastYearFilings.url, 'keyVal': lastYearFilings.key
            });
            commit('SET_COMPANY_METADATA', response.data?.FILER)
          } catch (err) {
            console.error(err)
          }
        },
        async getCompanies({ commit }, searchValue) {
          try {
            let response = await axios.get(`get_companies/${searchValue}/`);
            commit('SET_COMPANIES', response.data);
          } catch (err) {
            console.log(err)
          }
        }

    },
});