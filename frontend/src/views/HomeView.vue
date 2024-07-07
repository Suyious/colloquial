<script setup>
import Avatar from '@/components/avatar/Avatar.vue';
import SecondaryNavigation from '@/components/navigation/SecondaryNavigation.vue';
import Modal from '@/components/modal/Modal.vue';
import { ref } from 'vue';
import CreatePostView from './partials/CreatePostView.vue';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();

const showModal = ref(false);
function toggleShowModal() {
  showModal.value = !showModal.value;
}
</script>

<template>
  <SecondaryNavigation>

    <!-- FOR DESKTOP/LARGER SCREENS -->
    <RouterLink to="/" class="font-[Oswald] font-[600] hidden md:block text-lg">COLLOQUIAL</RouterLink>
    <!-- FOR MOBILE/SMALL SCREENS -->
    <RouterLink to="/" class="font-[Oswald] font-[600] md:hidden text-sm flex flex-col">
      <span>COLO</span>
      <span class="mt-[-8px]">QUIAL</span>
    </RouterLink>

    <RouterLink to="/chat" class="font-[Oswald] font-[600] uppercase text-sm">Chat</RouterLink>

    <button @click="toggleShowModal" class="font-[Oswald] font-[600] uppercase text-sm bg-black text-white py-2 px-6 rounded-md">New Post</button>

    <!-- FOR DESKTOP/LARGER SCREENS -->
    <RouterLink to="/notifications" class="font-[Oswald] font-[600] hidden md:block uppercase text-sm">Notifications</RouterLink>
    <!-- FOR MOBILE/SMALL SCREENS -->
    <RouterLink to="/notifications" class="font-[Oswald] font-[600] md:hidden uppercase text-sm">Notif</RouterLink>

    <template v-if="userStore.user.isAuthenticated">
      <RouterLink :to="{name: 'profile', params: { id: userStore.user.id }}">
        <Avatar src="https://images.unsplash.com/photo-1711993429168-286628fbc02f?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"/>
      </RouterLink>
    </template>

  </SecondaryNavigation>

  <main class="my-20">
    <RouterView/>
  </main>

  <Modal bottom="5em" left="50%" :show="showModal" :toggle-show="toggleShowModal">
    <CreatePostView @cancel-post="toggleShowModal"/>
  </Modal>

</template>
