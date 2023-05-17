<template>
  <v-alert :type="type">
    {{ message }}
  </v-alert>
</template>

<script>
export default {
    props: {
        type: {
            type: String,
            default: 'info',
        },
        message: {
            type: String,
            required: true,
        }
    }
};
</script>