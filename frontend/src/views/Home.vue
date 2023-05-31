<template>
  <v-container class="fill-height">
    <Search />
    <v-row v-show="companyMetadata">
      <v-col cols="6">
        <v-list>
          <v-list-item
            prepend-icon="mdi-phone"
            :title="companyMetadata?.BUSINESS_ADDRESS?.BUSINESS_PHONE"
          ></v-list-item>
          <v-divider inset></v-divider>
          <v-list-item
            prepend-icon="mdi-map-marker"
            :title="`${this.companyMetadata?.BUSINESS_ADDRESS?.STREET_1 }, ${ this.companyMetadata?.BUSINESS_ADDRESS?.CITY }, ${ this.companyMetadata?.BUSINESS_ADDRESS?.STATE }, ${this.companyMetadata?.BUSINESS_ADDRESS?.ZIP }`"
          ></v-list-item>
        </v-list>
      </v-col>
      <v-col cols="6">
        <p> Name: {{ companyMetadata?.COMPANY_DATA.COMPANY_CONFORMED_NAME }}</p>
        <p> Central Index Key: {{ companyMetadata?.COMPANY_DATA.CENTRAL_INDEX_KEY }}</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import Search from '@/components/Search.vue'
  export default {
    components: {
      Search
    },
    computed: {
      companyMetadata() {
        return this.$store.state.companyMetadata
      },
      isCompanySelected() {
        return this.$store.state.companyFilings.length > 0
      }
    }
  }
</script>
