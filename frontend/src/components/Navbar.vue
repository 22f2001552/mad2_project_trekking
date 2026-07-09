<template>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">

<div class="container">

<router-link
class="navbar-brand"
to="/"
>

🏔 Trekking Management

</router-link>

<ul class="navbar-nav ms-auto">

<!-- USER -->

<template v-if="role==='user'">

<li class="nav-item">

<router-link
class="nav-link"
to="/user"
>

Dashboard

</router-link>

</li>

<li class="nav-item">

<router-link
class="nav-link"
to="/my-bookings"
>

My Bookings

</router-link>

</li>

<li class="nav-item">

<router-link
class="nav-link"
to="/profile"
>

Edit Profile

</router-link>

</li>

</template>

<!-- STAFF -->

<template v-if="role==='staff'">

<li class="nav-item">

<router-link
class="nav-link"
to="/staff"
>

Dashboard

</router-link>

</li>

</template>

<!-- ADMIN -->

<template v-if="role==='admin'">

<li class="nav-item">

<router-link
class="nav-link"
to="/admin"
>

Dashboard

</router-link>

</li>

</template>

<li class="nav-item">

<a
class="nav-link text-danger"
href="#"
@click.prevent="logout"
>

Logout

</a>

</li>

</ul>

</div>

</nav>

</template>

<script setup>

import { useRouter } from "vue-router";

const router = useRouter();

const role = localStorage.getItem("role");

function logout(){

    localStorage.clear();

    router.push("/");

}

</script>