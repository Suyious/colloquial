<script setup>
import Input from '@/components/input/Input.vue';
import { useToastStore } from '@/stores/toast.js';
import axios from 'axios';
import { ref } from 'vue';

const toastStore = useToastStore();

const form = ref({
    email: '',
    name: '',
    password1: '',
    password2: '',
});
const errors = ref({});

function submitForm() {
    errors.value = {};

    if(form.value.email === '') {
        errors.value.email = 'Email is missing';
    }
    if(form.value.name === '') {
        errors.value.name = 'Name is missing';
    }
    if(form.value.password1 === '') {
        errors.value.password1 = 'Password is missing';
    }
    if(form.value.password2 !== form.value.password1) {
        errors.value.password2 = 'Passwords do not match';
    }

    if(Object.keys(errors.value).length === 0) {
        axios.post('/api/signup/', form.value)
            .then(response => {
                if(response.data.status === 'success') {
                    toastStore.showToast(5000, 'User Registered. Please Log In.', 'text-emerald-900')
                } else {
                    toastStore.showToast(5000, 'Something Went Wrong. Please try again.', 'text-red-900')
                }

                form.value.email = '';
                form.value.name = '';
                form.value.password1 = '';
                form.value.password2 = '';
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
            <Input :error="errors.name" v-model="form.name" type="text" label="Name" placeholder="Name"/>
            <Input :error="errors.email" type="email" v-model="form.email" label="Email" placeholder="Name"/>
            <Input :error="errors.password1" type="password" v-model="form.password1" label="Password" placeholder="Password"/>
            <Input :error="errors.password2" type="password" v-model="form.password2" label="Confirm Password" placeholder="Confirm Password"/>
            <button type="submit" class="font-[Oswald] font-[400] bg-black text-white rounded-md px-2 py-2">Sign Up</button>
            <p class="font-[Oswald] font-[300] text-center">Already have an account?
                <RouterLink class="font-[400]"to="/login">Log In</RouterLink>
            </p>
        </form>
    </main>
</template>