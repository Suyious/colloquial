<script setup>
import Modal from '@/components/modal/Modal.vue';
import Post from '@/components/post/Post.vue';
import SearchBar from '@/views/partials/Searchbar.vue'
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import PostPage from './partials/PostPage.vue';
import { content } from '@/assets/content.js'

const router = useRouter();

const posts = ref([]);

onMounted(() => {
    getFeed();
})

function getFeed() {
    axios.get('/api/posts/')
        .then(response => {
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

const currentPost = ref(null);
const showModal = ref(false);

function openModal(id) {
    currentPost.value = id;
    history.pushState({}, "", `/post/${id}`)
    showModal.value = true;
    window.addEventListener("popstate", closeModal)
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    currentPost.value = null;
    history.pushState({}, "", "/");
    showModal.value = false;
    window.removeEventListener("popstate", closeModal)
    document.body.style.overflow = 'unset';
}

</script>

<template>
    <article class="px-2 flex flex-col gap-4 items-center">
        <SearchBar v-model="keyword" @submit="onSearch" title="COLLOQUIAL" />
        <template v-for="(post, index) in posts" :key="post.id">
            <Post @click-post="() => openModal(post.id)" :post="post"
                profile-picture="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                :content="content[index]" />
        </template>
        <Modal bottom="50%" left="50%" :show="showModal" :toggle-show="closeModal" z="99" bg="rgb(0 0 0 / 66%)">
            <div class="absolute -top-8 right-2 z-99 text-white uppercase font-[Oswald] font=[600] cursor-pointer"
                    @click="closeModal">Close</div>
            <div class="bg-white w-[90vw] h-[90vh] border-t-2 border-x-2 border-black rounded-lg relative overflow-hidden">
                <PostPage :post-id="currentPost" />
            </div>
        </Modal>
    </article>
</template>