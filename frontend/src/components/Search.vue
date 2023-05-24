<template>
  <v-responsive class="fill-height d-flex align-center text-center">

    <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

    <h1 class="text-h2 font-weight-bold mb-4">Edgar Data</h1>

    <v-row class="d-flex align-center justify-center">
      <v-col
        cols="12"
      >
        <v-combobox
          v-model="selectedItem"
          item-value="org_cik"
          item-title="org_name"
          :items="companies"
          :loading="loading"
          :label="label"
          :hint="hint"
          :rules="rules"
          :menu-props="{ maxHeight: 300 }"
          @input="onInput"
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
  </v-responsive>
</template>

<script>
  export default {
    data() {
      return {
        selectedItem: null,
        loading: false,
        label: 'Select an item',
        hint: 'Start typing to search',
        rules: [v => !!v || 'Item is required'],
      }
    },
    computed: {
      companies() {
        return this.$store.state.companies
      },
      isCompanySelected() {
        return this.$store.state.companyFilings.length > 0
      }
    },
    methods: {
      async fetchItems() {
        this.loading = true
        this.$store.dispatch('getCompanies', this.selectedItem)
        this.loading = false
      },
    onInput() {
      if(this.selectedItem.length > 3 && !this.loading)  {
        this.fetchItems()
      }
    },
    handleClick() {
      this.$store.dispatch('getCompanyFilings', this.selectedItem.org_cik)
    }
  }
}
</script>
