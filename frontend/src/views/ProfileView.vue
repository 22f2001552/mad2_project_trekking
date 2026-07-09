<template>

<Navbar />

<div class="container mt-5">

<div class="card shadow">

<div class="card-header">

<h3>Edit Profile</h3>

</div>

<div class="card-body">

<div class="mb-3">

<label>Name</label>

<input
class="form-control"
v-model="newName"
/>

</div>

<button
class="btn btn-primary"
@click="updateProfile"
>

Update Profile

</button>

</div>

</div>

</div>

</template>

<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import api from "../api/api";

const router = useRouter();

const name = ref(localStorage.getItem("name"));

const newName = ref(name.value);

async function updateProfile(){

    try{

        await api.put(
            "/profile",

            {
                name: newName.value
            },

            {
                headers:{
                    Authorization:"Bearer "+localStorage.getItem("token")
                }
            }

        );

        localStorage.setItem("name", newName.value);

        alert("Profile Updated Successfully!");

        router.push("/user");

    }

    catch(error){

        console.log(error.response.status);
        console.log(error.response.data);
        alert("Unable to update profile");

}

}

</script>