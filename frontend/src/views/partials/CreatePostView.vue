<script setup>
import axios from 'axios';
import { ref } from 'vue';

const emit = defineEmits('cancelPost')
const body = ref("");
const fileInput = ref(null);
const imageSrc = ref(null);

const uploading = ref(false);

function submitPost() {
  uploading.value = true;
  const formData = new FormData();

  formData.append('body', body.value);
  if (fileInput.value) {
    formData.append('image', fileInput.value.files[0]);
  }

  axios.post('/api/posts/', formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
    .then(response => {
      console.log('data', response.data);
      uploading.value = false;
      emit('cancelPost');
    })
    .catch(error => {
      uploading.value = false;
      console.log("error", error);
    })
}

function onFileInput() {
  fileInput.value.click();
}

function clearInput() {
  imageSrc.value = null;
  if (fileInput.value) {
    fileInput.value.value = ""; // Reset the file input
  }
}

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imageSrc.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

</script>

<template>
    <form @submit.prevent="submitPost" class="max-w-[95vw] bg-white border-2 border-black rounded-lg p-2">
      <div class="w-[40em] max-w-[100%] max-h-[calc(100vh_-_10em)] aspect-video border-2 border-gray-300 bg-gray-100 rounded-lg overflow-hidden cursor-pointer">
        <div class="w-full h-full group flex justify-center items-center relative">
          <template v-if="imageSrc">
              <img class="w-full h-full object-cover" :src="imageSrc" alt="New Image">
              <div class="group-hover:flex absolute w-full h-full font-[Oswald] hidden justify-center items-center gap-8 bg-black/20 text-white/60">
                <button type="button" @click="onFileInput">Replace Image</button>
                <button type="button" @click="clearInput">Clear Image</button>
              </div>
          </template>
          <template v-else>
            <button type="button" @click="onFileInput" class="font-[Oswald] text-black/50">Click to upload file</button>
          </template>
        </div>
        <input @change="handleFileChange" ref="fileInput" class="hidden" type="file" accept="image/*">
      </div>
      <div class="font-[Oswald] mt-4">
        <textarea v-model="body" class="w-full p-2 outline-none resize-none"placeholder="Enter Caption..."></textarea>
      </div>
      <div class="flex justify-between items-center font-[Oswald] p-2">
        <button @click="onFileInput" type="button">Attach</button>
        <div class="flex gap-8">
          <button type="button" @click="$emit('cancelPost')">Cancel</button>
          <button :disabled="uploading" type="submit" class="bg-black text-white px-8 py-2 rounded-md">{{ uploading ? "Pending" : "Post" }}</button>
        </div>
      </div>
    </form>
</template>