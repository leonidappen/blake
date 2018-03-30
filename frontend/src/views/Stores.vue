<template>
    <v-container fluid>
        <v-layout column align-center>
            <h1>Stores</h1>
            <Store v-if="store" :store="store"></Store>
        </v-layout>
    </v-container>
</template>

<script lang="ts">
import Store from '@/components/Store.vue';

import Vue from 'vue';

export default Vue.extend({
  name: 'Stores',
  components: {
      Store,
  },
    props: [ 'store' ],
});
</script>
