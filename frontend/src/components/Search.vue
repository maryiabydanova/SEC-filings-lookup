<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">

      <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

      <h1 class="text-h2 font-weight-bold">Edgar Data</h1>

      <div class="py-14" />

      <v-row class="d-flex align-center justify-center">
        <v-col
          cols="12"
        >
          <v-combobox
            v-model="selectedItem"
            item-value="org_cik"
            item-title="org_name"
            :items="items"
            :loading="loading"
            :label="label"
            :hint="hint"
            :rules="rules"
            :menu-props="{ maxHeight: 300 }"
            @input="onInput"
            @change="onChange"
          ></v-combobox>
        </v-col>
        <v-btn
          color="primary"
          size="large"
          @click="handleClick"
        >
          Get Data
        </v-btn>
      </v-row>
      <v-row class="mt-8"  v-show="edgarFiles.length > 0">
        <v-tabs
          v-model="tab"
          bg-color="primary"
        >
          <v-tab v-for="(file, index) in edgarFiles" :key="index" :value="index">
            {{ showFullYear(file.year) }}
          </v-tab>
        </v-tabs>

        <v-card-text>
          <v-window v-model="tab">
            <v-window-item v-for="(file, index) in edgarFiles" :key="index" :value="index">
            {{ file.url }}
            </v-window-item>  
          </v-window>    
        </v-card-text>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script>
  export default {
  data() {
    return {
      selectedItem: null,
      items: [],
      edgarFiles: [],
      loading: false,
      label: 'Select an item',
      hint: 'Start typing to search',
      rules: [v => !!v || 'Item is required'],
      tab: 0,
    }
  },
  methods: {
    fetchItems() {
      this.loading = true
      this.$axios.get(`get_companies/${this.selectedItem}/`)
        .then(response => {
          this.items = response.data
          this.loading = false
        })
        .catch(error => {
          console.error(error)
          this.loading = false
        })
    },
    onInput() {
      console.log('inp', this.selectedItem)
      if(this.selectedItem.length > 3 && !this.loading)  {
        this.fetchItems()
      }
    },
    onChange() {
      console.log('Selected item:', this.selectedItem)
    },
    handleClick() {
      this.$axios.post(`get_company_filings/`, { cik: this.selectedItem.org_cik, docType: 1})
        .then(response => {
          this.edgarFiles = this.buildLinks(response.data)
          this.preloadFirstTab()
        })
        .catch(error => {
          console.error(error)
        })
    },
    buildLinks(links) {
      const regex = /\/(\d+)\/(\d+)-(\d+)-(\d+)\.txt$/;
      return links.map((l) => {
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
    showFullYear(year) {
      const currentYear = new Date().getFullYear() % 100;
      if(year > currentYear) {
        return `19${year}`
      } 
      return `20${year}`
    },
    preloadFirstTab() {
      let firstTab = this.edgarFiles[0];
      let body = { 'url': firstTab.url, 'keyVal': firstTab.key }
      this.$axios.post(`get_filing_data/`, body)
        .then(response => {
          console.log(response)
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>
