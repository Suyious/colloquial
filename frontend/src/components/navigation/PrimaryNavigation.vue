<script setup>
</script>

<template>
    <nav class="w-full h-20 p-2 fixed top-0 left-0 z-[99]">
        <div class="h-full bg-white flex justify-between items-center rounded-lg border-[3px] border-black">
            <!-- LEFT -->
            <div class="">
                <slot name="left"></slot>
            </div>
            <!-- CENTER -->
            <div class="">
                <slot name="center"></slot>
            </div>
            <!-- RIGHT -->
            <div class="">
                <slot name="right"></slot>
            </div>
        </div>
    </nav>
</template>