<script setup>
import { content } from '@/assets/content';
import Avatar from '@/components/avatar/Avatar.vue';
import axios from 'axios';
import { onMounted, ref } from 'vue';
const { postId } = defineProps(["postId"]);

const post = ref(null);
const post_loading = ref(false);
const comments = ref(null);
const comments_loading = ref(false);
const comments_page_number = ref(null);

const cover = ref(false);

function toggleCover() {
    cover.value = !cover.value
}

const comment = ref("")

onMounted(() => {
    getPost();
    getComments();
})

function getPost() {
    post_loading.value = true;
    axios.get(`/api/posts/${postId}`)
        .then(response => {
            post.value = response.data;
            post_loading.value = false;
        }).catch(error => {
            console.log(error);
            // post_loading.value = false;
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

function submitComment() {
    if(comment.length === 0) return;
    axios.post(`api/posts/${postId}/comments/`, 
        { body: comment.value }
    )
        .then(response => {
            comments.value.unshift(response.data.data);
            comment.value = "";
        })
        .catch(error => {
            console.log(error);
        })
}

</script>

<template>
    <main class="h-full" v-if="post_loading">
        <div class="font-[Oswald] h-full w-full flex justify-center items-center">
            <div class="text-center">
                <h1 class="text-lg font-[500]">Loading Your post...</h1>
                <p class="text-sm">Please wait while the post is loading</p>
            </div>
        </div>
    </main>
    <main v-else-if="post" class="h-full flex">
        <!-- LEFT (Post) -->
        <div class="lg:w-1/2 h-full min-h-[100] p-5">
            <div class="h-full w-full flex flex-col gap-3">
                <div class="w-full flex-1 rounded-lg bg-gray-300 relative overflow-hidden">
                    <img class="w-full h-full" alt="Content" :style="{ objectFit: cover ? 'cover' : 'contain' }"
                        :src="content[0]">
                    <button @click="toggleCover"
                        class="py-1 px-2 absolute bg-white bottom-4 right-4 font-[Oswald] text-[0.8em] uppercase rounded-md">
                        {{ cover ? "Contain" : "Cover" }}
                    </button>
                </div>
                <div class="h-[8em] w-full gap-1 flex flex-col">
                    <div class="flex-1 overflow-hidden">
                        <h1 class="font-[Oswald] text-[1.2em]">{{ post.body }}</h1>
                    </div>
                    <div class="flex">
                        <div class="flex flex-1 gap-2 items-center">
                            <RouterLink :to="{ name: 'profile', params: { id: post.created_by.id } }">
                                <Avatar width="3em"
                                    src="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D">
                                </Avatar>
                            </RouterLink>
                            <div class="leading-5">
                                <RouterLink :to="{ name: 'profile', params: { id: post.created_by.id } }">
                                    <h4
                                        class="font-[Oswald] text-[1.2em] font-[600] max-w-[15em] text-ellipsis whitespace-nowrap overflow-hidden">
                                        {{ post.created_by.name }}</h4>

                                </RouterLink>
                                <p class="font-[Oswald] font-[400] text-[0.8em]">{{ post.created_ago ===
                                    '0\u00A0minutes' ? "Right Now" : post.created_ago + " ago" }}</p>
                            </div>
                        </div>
                        <div class="flex gap-2 items-end">
                            <button
                                class="font-[Oswald] uppercase text-[0.8em] rounded-md bg-black text-white px-6 py-1">
                                {{ post.created_by.is_following ? "following": "follow" }}
                            </button>
                            <button
                                class="font-[Oswald] uppercase text-[0.8em] rounded-md bg-black text-white px-6 py-1">{{
                                post.likes_count }} {{ post.is_liked ? "unlike": "like" }}</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- RIGHT (Comments) -->
        <div class="hidden lg:block w-1/2 h-full p-5 relative">
            <div class="h-[15em] w-1 bg-gray-500 absolute top-1/2 -translate-y-1/2 left-0"> </div>
            <div class="h-full w-full flex flex-col gap-4">
                <div class="w-full flex-1 overflow-auto">
                    <template v-if="comments_loading">
                        <div class="font-[Oswald] h-full w-full flex justify-center items-center">
                            <div class="text-center">
                                <h1 class="text-lg font-[500]">The Comments are loading...</h1>
                                <p class="text-sm">Please wait while the comments are fetched</p>
                            </div>
                        </div>
                    </template>
                    <template v-else-if="comments && comments.length !== 0" v-for="comment in comments" :key="comment.id">
                        <div class="font-[Oswald] flex gap-3 mb-4">
                            <RouterLink :to="{ name: 'profile', params: { id: post.created_by.id } }">
                                <Avatar width="2.5em"
                                    src="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D">
                                </Avatar>
                            </RouterLink>
                            <div class="leading-5">
                                <div class="flex gap-1 align-baseline">
                                    <RouterLink :to="{ name: 'profile', params: { id: post.created_by.id } }">
                                        <h3 class="font-[600] text-[0.9em]">{{ comment.user.name }}</h3>
                                    </RouterLink>
                                    <p class="text-[0.6em]">{{ comment.created_ago === '0\u00A0minutes' ? "Right Now" :
                                        comment.created_ago + " ago" }}</p>
                                </div>
                                <p>{{ comment.body }}</p>
                            </div>
                        </div>
                    </template>
                    <template v-else>
                        <div class="font-[Oswald] h-full w-full flex justify-center items-center">
                            <div class="text-center">
                                <h1 class="text-lg font-[500]">No Comments Yet</h1>
                                <p class="text-sm">Be the first to leave a comment</p>
                            </div>
                        </div>
                    </template>
                </div>
                <form @submit.prevent="() => submitComment(comment)"
                    class="h-[6em] w-full bg-gray-300 rounded-lg p-3 flex gap-4">
                    <Avatar width="3em"
                        src="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D">
                    </Avatar>
                    <div class="flex-1 flex flex-col items-end">
                        <textarea placeholder="Leave a comment..." v-model="comment"
                            class="font-[Oswald] w-full h-full bg-transparent resize-none outline-none placeholder:text-slate-500"></textarea>
                        <button
                            class="font-[Oswald] uppercase text-[0.8em] rounded-md bg-black text-white px-6 py-1">Comment</button>
                    </div>
                </form>
            </div>
        </div>

    </main>

</template>