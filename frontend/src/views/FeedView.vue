<script setup>
import Post from '@/components/post/Post.vue';
import SearchBar from '@/views/partials/Searchbar.vue'
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const posts = ref([]);

onMounted(() => {
    getFeed();
})

function getFeed() {
    axios.get('/api/posts/')
        .then(response => {
            // console.log(response.data);
            posts.value = response.data.data;
        }).catch(error => {
            console.log(error);
        })
}

const keyword = ref("");

function onSearch() {
    if(keyword.value.length !== 0) router.push(`/search?keyword=${keyword.value}`)
    else router.push('/search');
}

</script>

<template>
    <article class="px-2 flex flex-col gap-4 items-center">
        <SearchBar v-model="keyword" @submit="onSearch" title="COLLOQUIAL"/>
        <template v-for="post in posts" :key="post.id">
            <Post
            :author="post.created_by" 
            profile-picture="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            content="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            :caption="post.body"/>
        </template>
    </article>
</template>