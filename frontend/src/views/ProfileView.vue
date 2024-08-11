<script setup>
import Avatar from '@/components/avatar/Avatar.vue';
import Post from '@/components/post/Post.vue';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Searchbar from './partials/Searchbar.vue';
import format from '@/utils/format';

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const keyword = ref(route.query.keyword || "");
function onSearch() {
    if(keyword.value.length !== 0) router.push(`/user/${route.params.id}?keyword=${keyword.value}`)
    else router.push(`/user/${route.params.id}`);
}

const posts = ref([]);
const user = ref({});

const cards = computed(() => [
    { title: "posts", figure: posts.value.length ? posts.value.length : 0},
    { title: "following", figure: user.value.following ? user.value.following : 0 },
    { title: "followers", figure: user.value.followers ? user.value.followers : 0 },
]);

onMounted(() => {
    getFeed();
    getUser();
})

watch(
    route,
    () => {
        console.log("rerun");
        getFeed();
        getUser();
    }, {
    deep: true,
    immediate: true
})

function getFeed() {
    let url;
    if(keyword.value.length !== 0) url = `/api/posts/?user=${route.params.id}&keyword=${keyword.value}`
    else url = (`/api/posts/?user=${route.params.id}`);

    axios.get(url)
        .then(response => {
            // console.log(response.data);
            posts.value = response.data.data;
        }).catch(error => {
            posts.value = [];
        })
}

function getUser() {
    axios.get(`/api/user/${route.params.id}`)
        .then(response => {
            // console.log("User", response.data);
            user.value = response.data;
        }).catch(error => {
            console.log(error);
        })
}

function cancelRequest() {
    axios.delete(`/api/user/${user.value.id}/cancel/`)
        .then(response => {
            console.log("[FOLLOW] ", response);
            user.value = {
                ...user.value,
                sent_request: false,
            }
        })
        .catch(error => {
            console.log("[FOLLOW] error: ", error.response);
        })
}
function acceptRequest() {
    axios.post(`/api/user/${user.value.id}/accept/`)
        .then(response => {
            console.log("[FOLLOW] ", response);
            user.value = {
                ...user.value,
                following: user.value.following + 1,
                is_follower: true,
                received_request: false,
            }
        })
        .catch(error => {
            console.log("[FOLLOW] error: ", error.response);
        })
}
function unfollow() {
    axios.delete(`/api/user/${user.value.id}/unfollow/`)
        .then(response => {
            console.log("[FOLLOW] ", response);
            user.value = {
                ...user.value,
                is_following: false,
            }
        })
        .catch(error => {
            console.log("[FOLLOW] error: ", error.response);
        })
}
function follow() {
    axios.post(`/api/user/${user.value.id}/follow/`)
        .then(response => {
            console.log("[FOLLOW] ", response);
            user.value = {
                ...user.value,
                sent_request: true,
            }
        })
        .catch(error => {
            console.log("[FOLLOW] error: ", error.response);
        })
}

</script>

<template>
    <article class="px-2 flex flex-col gap-4 items-center">
        <Searchbar v-model="keyword" @submit="onSearch" :title="user.name"/>

        <div class="w-[40em] max-w-[90vw] flex flex-col md:flex-row items-center gap-4 md:gap-16">
            <Avatar width="10em" src="https://images.unsplash.com/photo-1716234240817-6c85af852899?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"/>
            <div class="flex-1 w-full">
                <div class="flex justify-between items-center">
                    <template v-for="card in cards" :key="card.title">
                        <div class="flex flex-col items-center">
                            <div class="font-[Oswald] font-[400] text-[1.2em] md:text-[1.5em]">{{ card.title }}</div>
                            <div class="font-[Oswald] font-[600] text-[2em] md:text-[3.5em]">{{ format(card.figure) }}</div>
                        </div>
                    </template>
                </div>
                <div class="flex gap-4 font-[Oswald] mt-4">
                    <button v-if="userStore.user.id === user.id" class="bg-black text-white py-1 w-8/12 uppercase">Edit Profile</button>
                    <button @click="cancelRequest" v-else-if="user.sent_request" class="bg-black text-white py-1 w-8/12 uppercase">Requested</button>
                    <button @click="acceptRequest" v-else-if="user.received_request" class="bg-black text-white py-1 w-8/12 uppercase">Accept Request</button>
                    <button @click="unfollow" v-else-if="user.is_following" class="bg-black text-white py-1 w-8/12 uppercase">Following</button>
                    <button @click="follow" v-else-if="user.is_follower" class="bg-black text-white py-1 w-8/12 uppercase">Follow Back</button>
                    <button @click="follow" v-else class="bg-black text-white py-1 w-8/12 uppercase">Follow</button>
                    <RouterLink to="/chat"class="text-center border-black border-2 py-1 w-4/12">Message</RouterLink>
                </div>
            </div>
        </div>
        <div class="w-[40em] max-w-[90vw] font-[Oswald]">
            <h1 class="font-[500] lowercase">{{ user?.name }}</h1>
            <p v-if="user.bio">{{ user?.bio }}</p>
            <p class="text-black/50" v-else>Bio is Empty</p>
        </div>

        <section class="w-[40em] max-w-[95vw] pt-16">
            <h1 class="font-[Oswald] font-[600] text-[1.2em] uppercase">Posts Feed</h1>
            <div class="pt-4 flex flex-col gap-4">
                <template v-if="posts.length === 0">
                    <div class="font-[Oswald] w-full text-center">
                        <h1 class="font-[600] uppercase text-[1.5em]">No Posts Found</h1>
                        <p>No posts matching your search were found. Try something else.</p>
                    </div>
                </template>
                <template v-for="post in posts" :key="post.id">
                    <Post
                    :post="post"
                    profile-picture="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                    content="https://images.unsplash.com/photo-1716545617942-1845033e0bc8?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                    />
                </template>
            </div>
        </section>
    </article>
</template>