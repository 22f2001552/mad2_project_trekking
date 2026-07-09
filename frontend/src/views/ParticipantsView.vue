<template>

<div class="container mt-5">

<h2 class="mb-4">

Participants

</h2>

<div
v-for="participant in participants"
:key="participant.user_id"
class="card mb-3 shadow"
>

<div class="card-body">

<h4>{{ participant.name }}</h4>

<p><strong>Email:</strong> {{ participant.email }}</p>

</div>

</div>

<div
v-if="participants.length===0"
class="alert alert-info"
>

No participants yet.

</div>

</div>

</template>

<script setup>

import { ref,onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "../api/api";

const route = useRoute();

const participants = ref([]);

async function loadParticipants(){

    const response = await api.get(

        "/staff/participants/" + route.params.trekId,

        {
            headers:{
                Authorization:
                "Bearer " +
                localStorage.getItem("token")
            }
        }

    );

    participants.value = response.data;

}

onMounted(loadParticipants);

</script>