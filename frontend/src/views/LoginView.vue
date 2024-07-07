<script setup>
import Input from '@/components/input/Input.vue';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const userStore = useUserStore();

const form = ref({
    email: '',
    password: '',
});
const errors = ref({});

async function submitForm() {
    errors.value = {};

    if(form.value.email === '') {
        errors.value.email = 'Email is missing';
    }
    if(form.value.password === '') {
        errors.value.password = 'Password is missing';
    }

    if(Object.keys(errors.value).length === 0) {
        await axios.post('/api/login/', form.value)
            .then(response => {
                userStore.setToken(response.data);

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access;
            })
            .catch(error => {
                console.log(error);
            })
        await axios.get('/api/me/')
            .then(response => {
                userStore.setUserInfo(response.data);
                router.push('/');
            })
            .catch(error => {
                console.log(error);
            })
    } else {
        console.log(form.value)
        console.log(errors.value);
    }

}

</script>

<template>
    <main class="pt-24 px-2">
        <form @submit.prevent="submitForm" class="flex flex-col gap-4 w-[30em] max-w-[100%] m-auto">
            <Input :error="errors.email" v-model="form.email" type="email" label="Email" placeholder="Name"/>
            <Input :error="errors.password" v-model="form.password" type="password" label="Password" placeholder="Password"/>
            <button type="submit" class="font-[Oswald] font-[400] bg-black text-white rounded-md px-2 py-2">Log In</button>
            <p class="font-[Oswald] font-[300] text-center">Don't have an account?
                <RouterLink class="font-[400]" to="/signup">Sign Up</RouterLink>
            </p>
        </form>
    </main>
</template>