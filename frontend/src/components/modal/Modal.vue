<script setup>

const { show, toggleShow, bottom, left, right, top } = defineProps(["show", "toggleShow", "bottom", "left", "right", "top"]);

</script>

<template>
    <Transition name="modal">
        <div v-if="show" class="fixed top-0 left-0 w-full h-full z-[98]">
            <div @click="toggleShow" class="absolute top-0 left-0 w-full h-full"></div>
            <div class="absolute translate-x-[-50%]"
                 :style="{bottom: bottom+'', top: top, left: left, right: right}">
                <slot></slot>
            </div>
        </div>    
    </Transition>
</template>

<style>
.modal-enter-from,
.modal-leave-to {
    opacity: 0;
    transform: translateY(100%);
    scale: 0;
}
.modal-enter-to,
.modal-leave-from {
    opacity: 1;
    transform: translateX(0);
    scale: 1;
}
.modal-enter-active,
.modal-leave-active {
    transition: all 200ms ease-in;
}
</style>