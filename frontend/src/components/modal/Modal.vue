<script setup>

const { show, toggleShow, bottom, left, right, top, z, bg }
    = defineProps(["show", "toggleShow", "bottom", "left", "right", "top", "z", "bg"]);

function translationX(bottom, top) {
    if(top === "50%") return -50
    if(bottom === "50%") return 50
    return 0
}

function translationY(left, right) {
    if(right === "50%") return 50
    if(left === "50%") return -50
    return 0
}

</script>


<template>
    <Transition name="modal">
        <div v-if="show" class="fixed top-0 left-0 w-full h-full z-[98]" :style="{ zIndex: z || 98}">
            <div @click="toggleShow" class="absolute top-0 left-0 w-full h-full" :style="{ background: bg }"></div>
            <div class="absolute"
                 :style="{
                    bottom: bottom, top: top, left: left, right: right,
                    transform: `translate(${translationY(left,right)}%,${translationX(bottom,top)}%)`
                }">
                <slot></slot>
            </div>
        </div>    
    </Transition>
</template>

<style>
.modal-enter-from,
.modal-leave-to {
    opacity: 0;
    transform: translateY(70%);
    scale: 0;
    transform-origin: bottom;
}
.modal-enter-to,
.modal-leave-from {
    opacity: 1;
    transform: translateX(0);
    scale: 1;
}
.modal-enter-active,
.modal-leave-active {
    transition: all 300ms cubic-bezier(0.45, -0.45, 0.45, 1.45);
}
</style>