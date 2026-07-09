<template>

<Navbar />

<div class="container mt-4">

    <h2 class="fw-bold">
        🧑‍💼 Staff Dashboard
    </h2>
    <p class="text-muted">
        Welcome, <strong>{{ name }}</strong>. Manage your assigned treks below.
    </p>


    <div class="row mb-4">

        <div class="col-md-4">

            <div class="card shadow text-center">

                <div class="card-body">

                    <h5>Total Treks</h5>

                    <h2>{{ treks.length }}</h2>

                </div>

            </div>

        </div>

        <div class="col-md-4">

            <div class="card shadow text-center">

                <div class="card-body">

                    <h5>Open Treks</h5>

                    <h2>{{ openTreks }}</h2>

                </div>

            </div>

        </div>

        <div class="col-md-4">

            <div class="card shadow text-center">

                <div class="card-body">

                    <h5>Closed Treks</h5>

                    <h2>{{ closedTreks }}</h2>

                </div>

            </div>

        </div>

    </div>

    <hr>

    <h3 class="text-center mb-4">

        Assigned Treks

    </h3>

    <hr>

    <div
        v-for="trek in treks"
        :key="trek.id"
        class="card shadow mb-4"
    >

        <div class="card-body">

            <h4>{{ trek.name }}</h4>

            <p>
                <strong>Location :</strong>
                {{ trek.location }}
            </p>

            <p>
                <strong>Difficulty :</strong>
                {{ trek.difficulty }}
            </p>

            <p>

                <strong>Status :</strong>

                <span
                    class="badge rounded-pill bg-success"
                    v-if="trek.status==='Open'">
                        Open
                </span>

                <span
                    class="badge rounded-pill bg-danger"
                    v-else>
                        Closed

                </span>

            </p>

            <p>
                <strong>Available Slots :</strong>
                {{ trek.slots }}
            </p>

            <p>
                <strong>Starting Date :</strong>
                {{ trek.start_date }}
            </p>

            <p>
                <strong>Ending Date :</strong>
                {{ trek.end_date }}
            </p>

            <div class="mt-3">

                <button
                    class="btn btn-warning me-2"
                    @click="updateStatus(trek)"
                >
                    Update Status
                </button>

                <button
                    class="btn btn-info"
                    @click="viewParticipants(trek.id)"
                >
                    View Participants
                </button>

            </div>

        </div>

    </div>

    <div
        v-if="treks.length===0"
        class="alert alert-info text-center"
    >

        No treks assigned.

    </div>

</div>

</template>

<script setup>

import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";

import api from "../api/api";
import Navbar from "../components/Navbar.vue";

const router = useRouter();

const name = localStorage.getItem("name");

const treks = ref([]);

const openTreks = computed(() =>
    treks.value.filter(t => t.status === "Open").length
);

const closedTreks = computed(() =>
    treks.value.filter(t => t.status === "Closed").length
);

async function loadTreks(){

    const response = await api.get(

        "/staff/treks",

        {
            headers:{
                Authorization:
                    "Bearer " + localStorage.getItem("token")
            }
        }

    );

    treks.value = response.data;

}

async function updateStatus(trek){

    try{

        const newStatus =
            trek.status === "Open"
            ? "Closed"
            : "Open";

        await api.put(

            "/staff/trek/" + trek.id,

            {
                status: newStatus
            },

            {
                headers:{
                    Authorization:
                        "Bearer " + localStorage.getItem("token")
                }
            }

        );

        alert("Status Updated Successfully!");

        await loadTreks();

    }

    catch(error){

        alert(error.response.data.message);

    }

}

function viewParticipants(id){

    router.push("/participants/" + id);

}

onMounted(loadTreks);

</script>