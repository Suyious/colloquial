<script setup lang="ts">
import { useRoute } from 'vue-router';
import PostPage from './partials/PostPage.vue';

const route = useRoute();

</script>

<template>
    <main class="w-9/12 m-auto h-[78vh]">
        <PostPage :post-id="route.params.id"/>
    </main>
</template>