<script setup>
import { ref } from 'vue'

const { threshold } = defineProps(["threshold"])

const wrapperRef = ref(null);
const translatableRef = ref(null);
const translationThreshold = ref(0);

const FORWARD = -1;
const BACKWARD = +1;

function translate(direction, threshold) {
    const totalArea = wrapperRef.value.offsetWidth;
    const visibleArea = translatableRef.value.offsetWidth;
    const maxThreshold = totalArea - visibleArea;

    if (translationThreshold.value >= 0 && direction === BACKWARD) return;
    if (translationThreshold <= maxThreshold && direction === FORWARD) return;

    let newTranslationThreshold = translationThreshold.value + direction * threshold;
    console.log(newTranslationThreshold, maxThreshold);
    if (newTranslationThreshold < maxThreshold) newTranslationThreshold = maxThreshold;
    if (newTranslationThreshold > 0) newTranslationThreshold = 0;

    translationThreshold.value = newTranslationThreshold;

}

</script>

<template>
    <div ref="wrapperRef" class="overflow-hidden">
        <div ref="translatableRef" class="flex gap-4 w-max transition-transform duration-100 ease-in-out"
            :style="{ transform: `translateX(${translationThreshold}px)` }">
            <slot></slot>
        </div>
    </div>
    <div class="font-[Oswald] flex justify-end items-center gap-4 mt-4">
        <button @click="() => translate(BACKWARD, threshold)" class="bg-black text-white px-4 py-1">Previous</button>
        <button @click="() => translate(FORWARD, threshold)" class="bg-black text-white px-4 py-1">Next</button>
    </div>
</template>