<script setup>
    const { title } = defineProps(["title", "onSubmit"]);
    defineEmits("submit")

    const model = defineModel();
</script>

<template>
    <form @submit.prevent="$emit('submit')" class="w-[40em] max-w-[90vw] flex gap-4 h-12 items-center">
        <div class="font-[Oswald] font-[600] text-lg uppercase">{{ title }}</div>
        <input v-model="model" class="font-[Oswald] font-[500] placeholder:uppercase text-lg flex-1 outline-none" :placeholder="`Search ${title}`">
        <button type="submit" class="font-[Oswald] font-[500] uppercase text-lg">Search</button>
    </form>
</template>