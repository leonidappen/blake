<template>
  <h1>Store: {{ store }}</h1>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
    name: 'Store',
    props: [ 'store' ],
});
</script>
