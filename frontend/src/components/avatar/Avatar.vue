<script setup>
    const props = defineProps({
        src: String,
        width: {
            type: String,
            default: "3em"
        }
    })
</script>
<template>
    <div class="overflow-hidden rounded-md border-2 border-black" :style="{ width: props.width, height: props.width }">
        <img class="w-full h-full object-cover border-2 border-white rounded-md" :src="props.src" alt="profile">
    </div>
</template>