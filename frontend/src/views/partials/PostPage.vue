<script setup>
import Post from '@/components/post/Post.vue';
import axios from 'axios';
import { onMounted, ref } from 'vue';
const { postId } = defineProps(["postId"]);

const post = ref(null);

onMounted(() => {
    getPost();
})

function getPost(){
    axios.get(`/api/posts/${postId}`)
        .then(response => {
            post.value = response.data;
        }).catch(error => {
            console.log(error);
        })
}

</script>

<template>
    <Post v-if="post" :post="post"
        profile-picture="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        content="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" />
</template>