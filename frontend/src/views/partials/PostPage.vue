<script setup>
// import Post from '@/components/post/Post.vue';
import Avatar from '@/components/avatar/Avatar.vue';
import axios from 'axios';
import { onMounted, ref } from 'vue';
const { postId } = defineProps(["postId"]);

const post = ref(null);
const comments = ref(null);
const comments_page_number = ref(null);

onMounted(() => {
    getPost();
    getComments();
})

function getPost(){
    axios.get(`/api/posts/${postId}`)
        .then(response => {
            post.value = response.data;
        }).catch(error => {
            console.log(error);
        })
}

function getComments() {
    axios.get(`/api/posts/${postId}/comments`)
        .then(response => {
            comments.value = response.data.data;
            comments_page_number.value = response.data.page
        }).catch(error => {
            console.log(error);
        })
}

</script>

<template>
    <main v-if="post" class="h-full p-4 overflow-y-scroll">
        <div class="min-w-[10em] max-w-full flex items-center gap-4">
            <Avatar width="2.5em" src="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"></Avatar>
            <h4 class="font-[Oswald] font-[600] max-w-[15em] text-ellipsis whitespace-nowrap overflow-hidden">{{ post.created_by.name }}</h4>
        </div>
        <h1>{{ post.body }}</h1>
        <p>{{ post.created_ago }} ago</p>
        <div class="w-[40em] max-w-[95vw]">
            <img class="w-full h-full object-cover cursor-pointer" alt="Content"
                 src="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D">
        </div>
        <p>{{ post.likes_count }} likes</p>
        <p>{{ post.comments_count }} comments</p>
        <template v-if="comments && comments.length !== 0" v-for="comment in comments" :key="comment.id">
            <div class="flex gap-3">
                <h3 class="font-[500]">{{ comment.user.name }}</h3>
                <p>{{ comment.body }}</p>
            </div>
        </template>
        <template v-else>
            <p>No Comments</p>
        </template>
    </main>

    <!-- <Post v-if="post" :post="post"
        profile-picture="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        content="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" /> -->
</template>