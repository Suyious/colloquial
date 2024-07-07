<script setup>
import Avatar from '@/components/avatar/Avatar.vue';
import Post from '@/components/post/Post.vue';
import axios from 'axios';
import { onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Searchbar from './partials/Searchbar.vue';

const route = useRoute();
const router = useRouter();

const keyword = ref(route.query.keyword || "");
function onSearch() {
    if(keyword.value.length !== 0) router.push(`/search?keyword=${keyword.value}`)
    else router.push('/search');
}

const accounts = ref([]);
const posts = ref([]);

// FOR STYLING AND ANIMATING
const wrapperRef = ref(null);
const translatableRef = ref(null);
const translationThreshold = ref("");

onMounted(() => {
    translationThreshold.value = -1 * (wrapperRef.value.offsetWidth - translatableRef.value.offsetWidth);
    console.log(translationThreshold.value)
})

watch(
    route,
    () => {
        getAccounts();
        getPosts();
    },
    { deep: true, immediate: true, }
)

function getAccounts() {
    axios.get(`/api/user/?keyword=${keyword.value}`)
        .then(response => {
            // console.log("user", response.data);
            accounts.value = response.data;
        }).catch(error => {
            accounts.value = [];
        })
}

function getPosts() {
    if(keyword.value) {
        axios.get(`/api/posts/?keyword=${keyword.value}`)
            .then(response => {
                console.log("posts", response.data);
                posts.value = response.data.data;
            }).catch(error => {
                posts.value = [];
            })
    } else {
        posts.value = [];
    }
}

</script>
<template>
    <article>
        <div class="w-[40em] max-w-[90vw] m-auto">
            <Searchbar v-model="keyword" @submit="onSearch" title="COLLOQUIAL" />
            
            <template v-if="Object.keys(route.query).length !== 0">
                <section>
                    <h3 class="font-[Oswald] font-[600] text-[1.3em] mb-4">ACCOUNTS</h3>
                    <div ref="wrapperRef" class="overflow-hidden">
                        <div ref="translatableRef" class="flex gap-4 w-max" :style="{ transform: `translateX(${translationThreshold})`}">
                            <template v-if="accounts.length === 0">
                                <div class="font-[Oswald] w-full text-center">
                                    <h1 class="font-[600] uppercase text-[1.5em]">No Accounts Found</h1>
                                    <p>No accounts matching your search were found. Try something else.</p>
                                </div>
                            </template>
                            <template v-for="account in accounts" :key="account.id">
                                <div class="flex flex-col items-center">
                                    <Avatar width="8em"
                                        src="https://images.unsplash.com/photo-1716234240817-6c85af852899?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" />
                                    <h2 class="font-[Oswald] font-[500] text-[1.2em] mb-2">{{ account.name }}</h2>
                                    <button class="bg-black text-white font-[Oswald] font-[500] text-[0.8em] uppercase px-8 py-1 mb-1">Add Friend</button>
                                    <RouterLink :to="{ name: 'profile', params: { id: account.id }}"
                                        class="font-[Oswald] font-[500] uppercase text-[0.8em]">View Profile</RouterLink>
                                </div>
                            </template>
                        </div>
                    </div>
                    <div class="font-[Oswald] flex justify-end items-center gap-4 mt-4">
                        <button class="bg-black text-white px-4 py-1">Precious</button>
                        <div class="">1 / 10</div>
                        <button class="bg-black text-white px-4 py-1">Next</button>
                    </div>
                </section>
    
                <section class="pt-8">
                    <h3 class="font-[Oswald] font-[600] text-[1.3em] mb-4">POSTS</h3>
                    <div class="flex flex-col gap-4">
                        <template v-if="posts.length === 0">
                            <div class="font-[Oswald] w-full text-center">
                                <h1 class="font-[600] uppercase text-[1.5em]">No Posts Found</h1>
                                <p>No posts matching your search were found. Try something else.</p>
                            </div>
                        </template>
                        <template v-for="post in posts" :key="post.id">
                            <Post :author="post.created_by"
                                profile-picture="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                                content="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                                :caption="post.body" />
                        </template>
                    </div>
                </section>
            </template>

            <template v-else>
                <div class="font-[Oswald] pt-8 w-full text-center">
                    <h1 class="font-[600] uppercase text-[1.5em]">Start Searching</h1>
                    <p>Your results will show up when you search something</p>
                </div>
            </template>
        </div>
    </article>
</template>