<script setup lang="ts">

import axios from 'axios';
import PrimaryNavigation from './components/navigation/PrimaryNavigation.vue';
import Toast from './components/toast/Toast.vue';
import { useUserStore } from './stores/user';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();

userStore.initStore();

const token = userStore.user.access;
if (token) {
  axios.defaults.headers.common["Authorization"] = "Bearer " + token;
} else {
  axios.defaults.headers.common["Authorization"] = "";
  router.push("/login");
}

</script>

<template>
  <PrimaryNavigation>
    <template #center>
      <h1 class="font-[Oswald] font-[600] text-xl">COLLOQUIAL</h1>
    </template>
  </PrimaryNavigation>
  <RouterView />
  <Toast/>
</template>