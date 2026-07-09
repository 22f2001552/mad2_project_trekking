<template>
  <div class="container mt-5">
    <div class="row justify-content-center">

      <div class="col-md-5">

        <div class="card shadow">

          <div class="card-header text-center">
            <h3>Create Account</h3>
          </div>

          <div class="card-body">

            <div class="mb-3">
              <label>Name</label>
              <input
                type="text"
                class="form-control"
                v-model="name"
              >
            </div>

            <div class="mb-3">
              <label>Email</label>
              <input
                type="email"
                class="form-control"
                v-model="email"
              >
            </div>

            <div class="mb-3">
              <label>Password</label>
              <input
                type="password"
                class="form-control"
                v-model="password"
              >
            </div>

            <button
              class="btn btn-success w-100"
              @click="register"
            >
              Register
            </button>

            <p class="text-center mt-3">
              Already have an account?

              <router-link to="/">
                Login
              </router-link>

            </p>

          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api/api";

const router = useRouter();

const name = ref("");
const email = ref("");
const password = ref("");

async function register(){

    try{

        await api.post("/register",{

            name: name.value,
            email: email.value,
            password: password.value

        });

        alert("Registration Successful");

        router.push("/");

    }

    catch(error){

        alert("Registration Failed");

    }

}

</script>