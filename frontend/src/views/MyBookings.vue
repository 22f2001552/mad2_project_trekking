<template>
<Navbar />
<div class="container mt-5">

<h2 class="mb-4">
My Bookings
</h2>

<router-link
to="/user"
class="btn btn-secondary mb-4"
>
Back to Dashboard
</router-link>

<div
v-for="booking in bookings"
:key="booking.booking_id"
class="card mb-3 shadow"
>

<div class="card-body">

<h4>{{ booking.trek_name }}</h4>

<p><strong>Location:</strong> {{ booking.location }}</p>

<p><strong>Status:</strong> {{ booking.status }}</p>

<button
class="btn btn-danger"
@click="cancelBooking(booking.booking_id)"
>
Cancel Booking
</button>

</div>

</div>

<div
v-if="bookings.length===0"
class="alert alert-info"
>

No bookings found.

</div>

</div>

</template>

<script setup>
import UserNavbar from "../components/Navbar.vue";
import { ref,onMounted } from "vue";
import api from "../api/api";

const bookings = ref([]);

async function loadBookings(){

    const response = await api.get(
        "/my-bookings",
        {
            headers:{
                Authorization:"Bearer "+localStorage.getItem("token")
            }
        }
    );

    bookings.value = response.data;

}

async function cancelBooking(id){

    try{

        await api.delete(
            "/bookings/"+id,
            {
                headers:{
                    Authorization:"Bearer "+localStorage.getItem("token")
                }
            }
        );

        alert("Booking Cancelled!");

        await loadBookings();

    }

    catch(error){

        alert(error.response.data.message);

    }

}

onMounted(loadBookings);

</script>