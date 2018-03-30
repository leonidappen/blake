<template>
    <v-container fluid>
        <v-layout column align-center>
            <h1>Scripts</h1>
            <Script v-if="script" :script="script"></Script>
        </v-layout>
    </v-container>
</template>

<script lang="ts">
import Script from '@/components/Script.vue';

import Vue from 'vue';

export default Vue.extend({
  name: 'Scripts',
  components: {
      Script,
  },
    props: [ 'script' ],
});
</script>
