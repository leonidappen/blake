<template>
  <h1>Script: {{ script }}</h1>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
    name: 'Script',
    props: [ 'script' ],
});
</script>
