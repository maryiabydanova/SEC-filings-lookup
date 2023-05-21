<template>
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
  </template>
  
  <script>
  export default {
    data() {
      return {
        tab: 0
      }
    },
    computed: {
      edgarFiles() {
        return this.$store.state.companyFilings;
      }
    },
    methods: {
      showFullYear(year) {
        const currentYear = new Date().getFullYear() % 100;
        if(year > currentYear) {
          return `19${year}`
        } 
        return `20${year}`
      },
    }
  };
  </script>