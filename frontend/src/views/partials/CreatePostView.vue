<script setup>
import axios from 'axios';
import { ref } from 'vue';

const emit = defineEmits('cancelPost')
const body = ref("");

function submitPost() {
  console.log("submit form", body.value);

  axios.post('/api/posts/create/', {
    body: body.value,
  })
  .then(response => {
    console.log('data', response.data);
    emit('cancelPost');
  })
  .catch(error => {
    console.log("error", error);
  })
}

</script>

<template>
    <form @submit.prevent="submitPost" class="max-w-[95vw] bg-white border-2 border-black rounded-lg p-2">
      <div class="w-[40em] max-w-[100%] max-h-[calc(100vh_-_10em)] aspect-video border-2 border-gray-300 bg-gray-100 rounded-lg">
      </div>
      <div class="font-[Oswald] mt-4">
        <textarea v-model="body" class="w-full p-2 outline-none resize-none"placeholder="Enter Caption..."></textarea>
      </div>
      <div class="flex justify-between items-center font-[Oswald] p-2">
        <button type="button">Attach</button>
        <div class="flex gap-8">
          <button type="button" @click="$emit('cancelPost')">Cancel</button>
          <button type="submit" class="bg-black text-white px-8 py-2 rounded-md">Post</button>
        </div>
      </div>
    </form>
</template>