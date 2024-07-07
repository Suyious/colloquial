<script setup>
import Avatar from '../avatar/Avatar.vue'

const props = defineProps({
    author: Object,
    profilePicture: String,
    content: String,
    caption: String,
})
</script>

<template>
    <div class="w-[40em] max-w-[95vw] min-h-10em sm:h-[calc(100vh_-_10em)] border-2 border-black rounded-lg relative">
        <div class="relative w-full h-full border-2 border-white rounded-lg overflow-hidden">
            <img class="w-full h-full object-cover" :src="props.content" alt="Content">
            <div class="absolute bottom-0 left-0 w-full h-36 bg-[linear-gradient(0deg,_rgba(0,_0,_0)_0%,_rgba(0,_0,_0,_0)_100%)]"></div>
        </div>
        <caption class="font-[Oswald] font-[300] text-lg absolute bottom-[7em] sm:bottom-[4em] left-4 text-white">{{ caption }}</caption>
        <RouterLink :to="{name: 'profile', params: { id: author.id}}">
            <div class="absolute bottom-[4em] sm:bottom-4 left-4 bg-white p-2 min-w-[10em] max-w-full flex items-center gap-4 rounded-lg">
                <Avatar width="2em" :src="profilePicture"></Avatar>
                <h4 class="font-[Oswald] font-[600] max-w-[15em] text-ellipsis whitespace-nowrap overflow-hidden">{{ props.author.name }}</h4>
            </div>
        </RouterLink>
        <div class="sm:absolute sm:bottom-4 sm:right-4 bg-white p-2 min-w-[10em] flex items-center gap-4 rounded-lg">
            <button class="font-[Oswald] font-[500] bg-black text-white text-sm px-4 py-1 rounded-md">Like</button>
            <input class="font-[Oswald] max-w-full outline-none" placeholder="Leave a Comment..."/>
        </div>
    </div>
</template>