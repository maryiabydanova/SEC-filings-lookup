<template>
  <v-main>
    <Alert v-for="alert in alerts" :key="alert.id" :type="alert.type" :message="alert.message" :dismissable="alert.dismissable" />
    <router-view />
  </v-main>
</template>

<script>
  import Alert from '@/components/Alert.vue';
  import { mapState } from 'vuex';

  export default {
    components: {
      Alert,
    },
    computed: {
      ...mapState(['alerts']),
    },
  };
</script>
