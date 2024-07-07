<script setup>
import { useToastStore } from '@/stores/toast.js'

const store = useToastStore();

</script>
<template>
    <div
        v-if="store.isVisible"
        class="border-2 border-black rounded-lg w-80 h-24 p-2 bg-white fixed bottom-2 right-2 z-[100] overflow-hidden"
    >
    <div class="flex justify-between">
        <h4 class="text-xs font-[Oswald] font-[600]">COLLOQUIAL</h4>
        <div @click="store.closeToast" class="font-[Oswald] text-xs uppercase px-1 cursor-pointer">close</div>
    </div>
    <div class="mt-1 font-[Oswald] font-[400]">
        {{ store.message.length > 100 ? store.message.substring(0, 100) + '...' : store.message }}
    </div>
    </div>
</template>