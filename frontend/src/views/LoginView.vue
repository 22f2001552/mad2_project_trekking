<template>
  <div class="container mt-5">
    <div class="row justify-content-center">

      <div class="col-md-5">

        <div class="card shadow">

          <div class="card-header text-center">
            <h3>Trekking Management</h3>
            <h5>please do login with your correct credentials</h5>
          </div>

          <div class="card-body">

            <div class="mb-3">
              <label>Email</label>

              <input
                type="email"
                class="form-control"
                v-model="email"
                autocomplete="off"
              >
            </div>

            <div class="mb-3">
              <label>Password</label>

              <input
                type="password"
                class="form-control"
                v-model="password"
                autocomplete="new-password"
              >
            </div>

            <button
              class="btn btn-primary w-100"
              @click="login"
            >
              Login
            </button>

            <p class="mt-3 text-center">
              Don't have an account?

              <router-link to="/register">
                Register
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
const email = ref("");
const password = ref("");

async function login(){

    try{

        const response = await api.post("/login",{

            email: email.value,
            password: password.value  

        });

        localStorage.setItem("token", response.data.token);
        localStorage.setItem("role", response.data.role);
        localStorage.setItem("name", response.data.name);

        if(response.data.role==="admin"){
            router.push("/admin");
        }
        else if(response.data.role==="staff"){
            router.push("/staff");
        }
        else{
            router.push("/user");
        }
    }
    catch(error){
      if(error.response && error.response.data.message){
        alert(error.response.data.message);
      }
      else{
        alert("Login Failed");
      }
    }

}

</script>