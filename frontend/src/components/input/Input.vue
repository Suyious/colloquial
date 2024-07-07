<script setup>

const { label, placeholder, type, error } = defineProps({
    label: String,
    placeholder: String,
    type: String,
    error: {
        type: String,
        default: '',
    }
})

const model = defineModel();

</script>

<template>
    <label class="flex flex-col gap-2">
        <div class="flex justify-between">
            <div class="font-[Oswald] font-[400] text-sm">{{ label }}</div>
            <div v-if="error.length !== 0" class="font-[Oswald] font-[400] text-sm text-red-500">{{ error }}</div>
        </div>
        <input v-model="model" class="font-[Oswald] font-[400] bg-transparent outline-none px-4 py-2 border-2 border-black rounded-md" :type="type" :placeholder="placeholder"/>
    </label>
</template>