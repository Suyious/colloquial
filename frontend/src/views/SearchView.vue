<script setup>
import Avatar from '@/components/avatar/Avatar.vue';
import Carousel from '@/components/carousel/Carousel.vue';
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
                    <div class="flex items-baseline justify-between">
                        <h3 class="font-[Oswald] font-[600] text-[1.3em] mb-4">ACCOUNTS</h3>
                        <span class="font-[Oswald] font-[500] text-[1em] mb-4">{{ accounts.length }} Found</span>
                    </div>
                    <template v-if="accounts.length === 0">
                        <div class="font-[Oswald] w-full text-center">
                            <h1 class="font-[600] uppercase text-[1.5em]">No Accounts Found</h1>
                            <p>No accounts matching your search were found. Try something else.</p>
                        </div>
                    </template>

                    <Carousel v-if="accounts.length > 0" :threshold="9 * 16">
                        <template v-for="account in accounts" :key="account.id">
                            <div class="flex flex-col items-center">
                                <RouterLink :to="{ name: 'profile', params: { id: account.id }}">
                                    <Avatar width="8em"
                                        src="https://images.unsplash.com/photo-1716234240817-6c85af852899?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" />
                                </RouterLink>
                                <RouterLink :to="{ name: 'profile', params: { id: account.id }}">
                                    <h2 class="font-[Oswald] font-[500] text-[1.2em] mb-2">{{ account.name }}</h2>
                                </RouterLink>
                                <button class="bg-black text-white font-[Oswald] font-[500] text-[0.8em] uppercase px-8 py-1 mb-1">Follow</button>
                                <RouterLink :to="{ name: 'profile', params: { id: account.id }}"
                                    class="font-[Oswald] font-[500] uppercase text-[0.8em]">View Profile</RouterLink>
                            </div>
                        </template>
                    </Carousel>
                    
                </section>
    
                <section class="pt-8">
                    <div class="flex items-baseline justify-between">
                        <h3 class="font-[Oswald] font-[600] text-[1.3em] mb-4">POSTS</h3>
                        <span class="font-[Oswald] font-[500] text-[1em] mb-4">{{ posts.length }} Found</span>
                    </div>
                    <template v-if="posts.length === 0">
                        <div class="font-[Oswald] w-full text-center">
                            <h1 class="font-[600] uppercase text-[1.5em]">No Posts Found</h1>
                            <p>No posts matching your search were found. Try something else.</p>
                        </div>
                    </template>
                    <div class="flex flex-col gap-4">
                        <template v-for="post in posts" :key="post.id">
                            <Post
                                :post="post"
                                profile-picture="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                                content="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                                />
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