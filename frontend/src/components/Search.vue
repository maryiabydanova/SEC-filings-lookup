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
          Get Docs
        </v-btn>
      </v-row>
      <v-row v-show="edgarFiles.length > 0">
        <p v-for="fileUrl in edgarFiles"> {{ fileUrl }}</p>
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
      rules: [v => !!v || 'Item is required']
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
          this.edgarFiles = response.data.file_urls
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>
