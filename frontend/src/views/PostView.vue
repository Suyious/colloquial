<script setup lang="ts">
import { useRoute } from 'vue-router';
import PostPage from './partials/PostPage.vue';

const route = useRoute();

</script>

<template>
    <PostPage :post-id="route.params.id"/>
</template>