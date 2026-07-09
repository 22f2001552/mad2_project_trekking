<template>
<Navbar />
<div class="container mt-5">
    <h2 class="mb-4">
        Welcome {{ name }}
    </h2>
    <div class="mb-4">
        <router-link
        to="/my-bookings"
        class="btn btn-primary"
        >
        My Bookings
    </router-link>
</div>

<div class="d-flex justify-content-between align-items-center mb-4">
    <button class="btn btn-danger" @click="logout">
        logout
    </button>
</div>

<div class="card shadow-sm p-3 mb-4">
    <h5>Search Treks</h5>
    <div class="row">
        <div class="col-md-4">
            <input class="form-control" placeholder="Location" v-model="searchLocation">
        </div>

        <div class="col-md-3">
            <select class="form-select"  v-model="searchDifficulty">
                <option value="">All Difficulties</option>
                <option value="Easy">Easy</option>
                <option value="Moderate">Moderate</option>
                <option value="Hard">Hard</option>
            </select>
        </div>

        <div class="col-md-2">
            <input
                type="number"
                class="form-control"
                placeholder="Days"
                v-model="searchDuration">
        </div>
        <div class="col-md-3">
            <button
                class="btn btn-primary me-2"
                @click="searchTreks">
                Search
            </button>

            <button
                class="btn btn-secondary"
                @click="resetSearch">
                Reset
            </button>
        </div>
    </div>
</div>

<h3 class="mb-4">
Available Treks
</h3>

<div class="row">
    <div class="col-md-4 mb-4" v-for="trek in treks" :key="trek.id">
        <div class="card shadow h-100">
            <div class="card-body">
                <h4>{{ trek.name }}</h4>
                <p><strong>Location:</strong> {{ trek.location }}</p>
                <p><strong>Difficulty:</strong> {{ trek.difficulty }}</p>
                <p><strong>Available Slots:</strong> {{ trek.slots }}</p>
                <p><strong>Start date</strong>{{ trek.start_date }}</p>
                <p><strong>End date</strong>{{ trek.end_date }}</p>
                <p><strong>Status:</strong> {{ trek.status }}</p>
                <button class="btn btn-success w-100" @click="bookTrek(trek.id)">
                    Book Trek
                </button>
            </div>
        </div>
    </div>
</div>
</div>
</template>

<script setup>
import Navbar from "../components/Navbar.vue";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api/api";
const name = localStorage.getItem("name");
const treks = ref([]);
const router = useRouter();
const searchLocation = ref("");
const searchDifficulty = ref("");
const searchDuration = ref("");
async function loadTreks(){
    const response = await api.get("/treks");
    console.log(response.data);
    treks.value = response.data;
}
async function bookTrek(id){
    try{
        await api.post(
            "/bookings",
            {
                trek_id: id
            },
            {
                headers:{
                    Authorization: "Bearer " + localStorage.getItem("token")
                }
            }
        );
        alert("Booking Successful!");
        await loadTreks();
    }
    catch(error){

        alert(error.response.data.message);

    }
}
function logout(){

    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("name");

    router.push("/");

}

async function searchTreks(){
    try{
        const response = await api.get(
            "/search",
            {
                params:{
                    location: searchLocation.value,
                    difficulty: searchDifficulty.value,
                    duration: searchDuration.value
                }
            }
        );
        treks.value = response.data;
    }
    catch(error){
        alert(error.response?.data?.message || "Search failed");

    }

}
function resetSearch(){
    searchLocation.value = "";
    searchDifficulty.value = "";
    searchDuration.value = "";
    loadTreks();

}

onMounted(loadTreks);

</script>