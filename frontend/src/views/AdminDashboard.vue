<template>

  <Navbar />

    <div class="container mt-4">

        <h2 class="mb-1">🛠 Admin Dashboard</h2>

        <p class="text-muted">
        Welcome {{ name }}
        </p>

        <div class="row mb-5">

            <div class="col-md-3">
                <div class="card shadow border-primary">
                <div class="card-body text-center">
                    <h6 class="text-primary">Users</h6>
                    <h2>{{ summary.users }}</h2>
                </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card shadow border-success">
                <div class="card-body text-center">
                    <h6 class="text-success">Staff</h6>
                    <h2>{{ summary.staff }}</h2>
                </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card shadow border-warning">
                <div class="card-body text-center">
                    <h6 class="text-warning">Treks</h6>
                    <h2>{{ summary.treks }}</h2>
                </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card shadow border-danger">
                <div class="card-body text-center">
                    <h6 class="text-danger">Bookings</h6>
                    <h2>{{ summary.bookings }}</h2>
                </div>
                </div>
            </div>
        </div>
    

        <hr>
            <h3 class="mb-3">Trek Management</h3>
            <button
            class="btn btn-success mb-4"
            @click="showCreateTrek = !showCreateTrek">
            {{ showCreateTrek ? "Close Form" : "+ Create Trek" }}
            </button>



        <hr>

        <div v-if="showCreateTrek" class="card shadow p-4 mb-5">
            <div class="row">

                <div class="col-md-6 mb-3">

                    <label class="form-label">
                        Trek Name
                    </label>

                    <input
                        class="form-control"
                        v-model="trekForm.name">

                </div>

                <div class="col-md-6 mb-3">

                <label class="form-label">
                    Location
                </label>

                <input
                    class="form-control"
                    v-model="trekForm.location">

            </div>

            <div class="col-md-6 mb-3">
                <label class="form-label">
                    Difficulty
                </label>
                <select
                    class="form-select"
                    v-model="trekForm.difficulty">
                    <option value="">Select Difficulty</option>
                    <option value="Easy">Easy</option>
                    <option value="Moderate">Moderate</option>
                    <option value="Hard">Hard</option>
                </select>
            </div>
            <div class="col-md-6 mb-3">
                <label class="form-label">
                    Duration (Days)
                </label>

                <input
                    type="number"
                    class="form-control"
                    v-model="trekForm.duration_days">
            </div>

            <div class="col-md-6 mb-3">

                <label class="form-label">
                    Available Slots
                </label>

                <input
                    type="number"
                    class="form-control"
                    v-model="trekForm.available_slots">
            </div>

            <div class="col-md-6 mb-3">

                <label class="form-label">
                    Assign Staff
                </label>

                <select
                class="form-select"
                v-model="trekForm.staff_id">

                <option value="">
                Select Staff
                </option>

                <option
                v-for="staff in staffList"
                :key="staff.id"
                :value="staff.id">
                {{ staff.name }}
                </option>

            </select>

        </div>

        <div class="col-md-6 mb-3">

            <label class="form-label">
                Start Date
            </label>

            <input
                type="date"
                class="form-control"
                v-model="trekForm.start_date"
            >

        </div>

        <div class="col-md-6 mb-3">

            <label class="form-label">
                End Date
            </label>

            <input
                type="date"
                class="form-control"
                v-model="trekForm.end_date"
            >

        </div>

    </div>

    <button
        class="btn btn-primary"
        @click="isEditing ? updateTrek() : createTrek()">
        {{ isEditing ? "Update Trek" : "Create Trek" }}

    </button>

</div>

<hr>
        <h3>Staff Management</h3>

        <button
        class="btn btn-success mb-3"
        @click="showCreateStaff = !showCreateStaff"
        >
        {{ showCreateStaff ? "Close Form" : "+ Create Staff" }}
        </button>
        
    <div
        v-if="showCreateStaff"
        class="card shadow p-4 mb-4"
        >

        <div class="row">
            <div class="col-md-6 mb-3">
                <label>Name</label>
                <input
                class="form-control"
                v-model="staffForm.name"
                />

            </div>

            <div class="col-md-6 mb-3">

                <label>Email</label>

                <input
                type="email"
                class="form-control"
                v-model="staffForm.email"
                autocomplete="off"
                />

            </div>

            <div class="col-md-6 mb-3">

                <label>Password</label>

                <input
                type="password"
                class="form-control"
                v-model="staffForm.password"
                autocomplete="new-password"
                />

            </div>

        </div>

        <button
        class="btn btn-primary"
        @click="createStaff"
        >

            Create Staff

        </button>

    </div>

<!--------------------------------------------------------------------------------------------------------------------->
<hr>

<div v-if="showTreks" class="mt-4">
    <div class="d-flex gap-2 flex-wrap">
        <button
        class="btn btn-outline-primary"
        @click="showTreks=!showTreks">
        {{ showTreks ? "Hide Treks" : "View Treks" }}

    </button>
    </div>

    <h3 class="mb-3"> All Treks </h3>

    <table class="table table-bordered table-hover">

        <thead class="table-dark">

            <tr>

                <th>Name</th>

                <th>Location</th>

                <th>Difficulty</th>

                <th>Duration</th>

                <th>Staff</th>

                <th>Status</th>

                <th>Slots</th>

                <th>Actions</th>

            </tr>

        </thead>

        <tbody>

            <tr
            v-for="trek in treks":key="trek.id">

                <td>{{ trek.name }}</td>
                <td>{{ trek.location }}</td>
                <td>{{ trek.difficulty }}</td>
                <td>{{ trek.duration_days }} Days</td>
                <td>{{ trek.staff_name }}</td>
                <td>

                    <span class="badge bg-success" v-if="trek.status==='Open'">  Open </span>
                    <span class="badge bg-danger" v-else>  Closed  </span>

                </td>

                <td>{{ trek.slots }}</td>

                <td>
                    <button class="btn btn-warning btn-sm me-2" @click="editTrek(trek)">Edit</button>
                    <button class="btn btn-danger btn-sm me-2" @click="deleteTrek(trek.id)">Delete</button>
                    <button
                        class="btn btn-secondary btn-sm"
                        v-if="trek.staff_id"
                        @click="unassignStaff(trek.id)">
                            Unassign

                    </button>

                

                    <div v-else class="d-flex">

                        <select
                                class="form-select form-select-sm me-2"
                                style="width:170px"
                                v-model="selectedStaff[trek.id]">

                            <option value="">
                                Select Staff
                            </option>

                            <option
                                v-for="staff in staffList"
                                :key="staff.id"
                                :value="staff.id">
                                {{ staff.name }}
                            </option>

                        </select>

                        <button
                            class="btn btn-success btn-sm"
                            @click="assignStaff(trek.id)">
                            Assign
                        </button>

                    </div>

                </td>

            </tr>

        </tbody>

    </table>
</div>
<!--------viewstaff---------------------->
<div v-if="showStaff" class="mt-4">
    <div class="d-flex gap-2 flex-wrap">
        <button class="btn btn-outline-success" @click="showStaff = !showStaff; loadStaff()">
        {{ showStaff ? "Hide Staff" : "View Staff" }}
    </button>
    </div>

    <h3 class="mb-3"> All Staff </h3>

    <table class="table table-bordered table-hover">

        <thead class="table-dark">

            <tr>

                <th>Name</th>

                <th>Email</th>

                <th>Assigned Trek</th>

                <th>Status</th>

                <th>Action</th> 

            </tr>

        </thead>

        <tbody>

            <tr v-for="staff in staffTable":key="staff.id">
                <td>{{ staff.name }}</td>

                <td>{{ staff.email }}</td>

                <td>{{ staff.assigned_trek }}</td>

                <td>

                    <span class="badge bg-success" v-if="staff.active">
                        Active
                    </span>

                    <span class="badge bg-danger" v-else >
                        Inactive
                    </span>

                </td>

                <td>

                    <button class="btn btn-danger btn-sm" @click="deactivateStaff(staff.id)" :disabled="!staff.active">
                        Deactivate
                    </button>

                </td>

            </tr>

        </tbody>

    </table>

</div>
<hr>

<!----------------ADMIN VIEW USERS--------------------------------------------------------------------->
<div v-if="showUsers" class="mt-4">
    <div class="d-flex gap-2 flex-wrap">
        <button class="btn btn-outline-warning" @click="showUsers = !showUsers; loadUsers()">
        {{ showUsers ? "Hide Users" : "View Users" }}
    </button>
    </div>
    <h3 class="mb-3">
        All Users
    </h3>

    <table class="table table-bordered table-hover">

        <thead class="table-dark">
            <tr>

                <th>Name</th>

                <th>Email</th>

                <th>Status</th>

                <th>Action</th>

            </tr>

        </thead>

        <tbody>
            <tr v-for="user in usersTable" :key="user.id">
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>
                    <span class="badge bg-success" v-if="user.active">
                        Active
                    </span>

                    <span class="badge bg-danger" v-else>
                        Inactive
                    </span>

                </td>

                <td>

                    <button class="btn btn-danger btn-sm" @click="deactivateUser(user.id)" :disabled="!user.active">
                        Deactivate
                    </button>
                </td>
            </tr>
        </tbody>
    </table>

</div>


<!----------------------ADMINB VIEWING BOoKINGS------------------------------->
<div v-if="showBookings" class="mt-4" >
    <div v-if="showUsers" class="mt-4">
        <button class="btn btn-outline-info"  @click="showBookings = !showBookings; loadBookings()">
            {{ showBookings ? "Hide Bookings" : "View Bookings" }}
        </button>

    </div>
    <h3 class="mb-3">
        All Bookings
    </h3>

    <table class="table table-bordered table-hover">

        <thead class="table-dark">

            <tr>

                <th>Booking ID</th>

                <th>User</th>

                <th>Trek</th>

                <th>Booking Date</th>

                <th>Status</th>

            </tr>

        </thead>

        <tbody>

            <tr v-for="booking in bookingsTable" :key="booking.booking_id" >

                <td>{{ booking.booking_id }}</td>

                <td>{{ booking.user }}</td>

                <td>{{ booking.trek }}</td>

                <td>{{ booking.booking_date }}</td>

                <td>

                    <span class="badge bg-success">
                        {{ booking.status }}
                    </span>
                </td>
            </tr>
        </tbody>
    </table>
</div>

<!--------------edit form------>

<div v-if="showEditForm" class="popup-overlay">
    <div class="popup-box">
        <div class="card-body">
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label>Trek Name</label>
                    <input class="form-control" v-model="trekForm.name"/>
                </div>

                <div class="col-md-6 mb-3">

                    <label>Location</label>
                    <input class="form-control" v-model="trekForm.location"/>

                </div>

                <div class="col-md-6 mb-3">
                    <label>Difficulty</label>
                    <select class="form-select" v-model="trekForm.difficulty">
                    <option>Easy</option>
                    <option>Moderate</option>
                    <option>Hard</option>
                    </select>

                </div>

                <div class="col-md-6 mb-3">

                    <label>Duration (Days)</label>

                    <input type="number" class="form-control" v-model="trekForm.duration_days"/>

                </div>

                <div class="col-md-6 mb-3">

                    <label>Available Slots</label>

                    <input
                    type="number"
                    class="form-control"
                    v-model="trekForm.available_slots"
                    />

                </div>

                <div class="col-md-6 mb-3">

                    <label>Assign Staff</label>

                    <select class="form-select" v-model="trekForm.staff_id">
                    <option value="">Select Staff</option>
                    <option v-for="staff in staffList" :key="staff.id" :value="staff.id">
                        {{ staff.name }}
                    </option>
                    </select>

                </div>

                <div class="col-md-6 mb-3">

                    <label>Start Date</label>

                    <input
                    type="date"
                    class="form-control"
                    v-model="trekForm.start_date"
                    />

                </div>

                <div class="col-md-6 mb-3">
                    <label>End Date</label>
                    <input
                    type="date"
                    class="form-control"
                    v-model="trekForm.end_date"
                    />

                </div>

            </div>

                <button class="btn btn-success me-2" @click="updateTrek">
                Update Trek
                </button>
                <button class="btn btn-secondary" @click="showEditForm=false">
                Cancel
                </button>
        </div>

    </div>
</div>
    

<div class="d-flex gap-2 flex-wrap">
    <button
        class="btn btn-outline-primary"
        @click="showTreks=!showTreks">
        {{ showTreks ? "Hide Treks" : "View Treks" }}

    </button>



    <button class="btn btn-outline-success" @click="showStaff = !showStaff; loadStaff()">
        {{ showStaff ? "Hide Staff" : "View Staff" }}
    </button>


    <button class="btn btn-outline-warning" @click="showUsers = !showUsers; loadUsers()">
        {{ showUsers ? "Hide Users" : "View Users" }}
    </button>

    <button class="btn btn-outline-info"  @click="showBookings = !showBookings; loadBookings()">
        {{ showBookings ? "Hide Bookings" : "View Bookings" }}
    </button>



    <button class="btn btn-outline-dark" @click="exportCSV" > 
        Export CSV 
    </button>

</div>

</div>

    



</template>

<script setup>

import { ref, reactive, onMounted } from "vue";
import Navbar from "../components/Navbar.vue";
import api from "../api/api";
const name = localStorage.getItem("name");
const showCreateTrek = ref(false);
const selectedStaff = ref({});
const showEditForm = ref(false);    
const summary = ref({
  users: 0,
  staff: 0,
  treks: 0,
  bookings: 0
});
const showBookings = ref(false);
const bookingsTable = ref([]);
const staffList = ref([]);
const showTreks = ref(false);
const treks = ref([]);
const isEditing = ref(false);
const editingTrekId = ref(null);
const showCreateStaff = ref(false);
const showStaff = ref(false);
const staffTable = ref([]);
const showUsers = ref(false);
const usersTable = ref([]);
const staffForm = reactive({

    name: "",

    email: "",

    password: "",

});
console.log(staffForm);


const trekForm = reactive({
  name: "",
  location: "",
  difficulty: "",
  duration_days: "",
  available_slots: "",
  start_date: "",
  end_date: "",
  staff_id: ""
});

async function loadSummary() {

  const response = await api.get(
    "/admin/summary",
    {
      headers: {
        Authorization:
          "Bearer " + localStorage.getItem("token")
      }
    }
  );

  summary.value = response.data;

}

async function loadStaff(){
    try{
        const response = await api.get(
            "/admin/active-staff",
            {
                headers:{
                    Authorization:
                    "Bearer " +
                    localStorage.getItem("token")
                }
            }
        );
        staffList.value = response.data;
        staffTable.value = response.data;
    }
    catch(error){
        alert(error.response.data.message);
    }
}

async function loadUsers(){

    try{

        const response = await api.get(

            "/admin/users",

            {
                headers:{
                    Authorization:
                    "Bearer " +
                    localStorage.getItem("token")
                }
            }

        );

        usersTable.value = response.data;

    }

    catch(error){

        alert(error.response.data.message);

    }

}








async function createTrek() {

  try {

    await api.post(
      "/admin/treks",
      trekForm,
      {
        headers: {
          Authorization:
            "Bearer " + localStorage.getItem("token")
        }
      }
    );
    alert("Trek Created Successfully!");
    showCreateTrek.value = false;
    Object.assign(trekForm, {
      name: "",
      location: "",
      difficulty: "",
      duration_days: "",
      available_slots: "",
      start_date: "",
      end_date: "",
      staff_id: ""
    });
    loadTreks();
    loadSummary();
  }
  catch (error) {
    alert(error.response.data.message);
  }

}


function editTrek(trek){
    showEditForm.value = true;
    editingTrekId.value = trek.id;
    trekForm.name = trek.name;
    trekForm.location = trek.location;
    trekForm.difficulty = trek.difficulty;
    trekForm.duration_days = trek.duration_days;
    trekForm.available_slots = trek.slots;
    trekForm.start_date = trek.start_date;
    trekForm.end_date = trek.end_date;
    trekForm.staff_id = trek.staff_id;

}


async function loadTreks(){

    const response = await api.get(

        "/admin/treks",

        {
            headers:{
                Authorization:
                "Bearer " +
                localStorage.getItem("token")
            }
        }

    );

    treks.value = response.data;

}
async function deleteTrek(id){

    const confirmDelete = confirm(
        "Are you sure you want to delete this trek?"
    );

    if(!confirmDelete){
        return;
    }
    try{

        await api.delete(

            "/admin/trek/" + id,

            {
                headers:{
                    Authorization:
                    "Bearer " +
                    localStorage.getItem("token")
                }
            }
        );
        alert("Trek Deleted Successfully!");
        loadTreks();
        loadSummary();
    }
    catch(error){

        alert(error.response.data.message);

    }

}

async function assignStaff(trekId){

    const staffId = selectedStaff.value[trekId];

    if(!staffId){

        alert("Please select a staff member.");

        return;

    }

    try{

        await api.put(

            "/admin/trek/" + trekId + "/assign-staff",

            {
                staff_id: staffId
            },

            {
                headers:{
                    Authorization:
                        "Bearer " + localStorage.getItem("token")
                }
            }

        );

        alert("Staff Assigned Successfully!");

        loadTreks();

    }

    catch(error){

        alert(error.response.data.message);

    }

}

async function unassignStaff(id){
    if(!confirm("Are u sure Unassign staff from this trek?")){
        return;
    }
    try{
        await api.put(
            "/admin/trek/" + id + "/unassign",
            {},
            {
                headers:{
                    Authorization:
                    "Bearer " +
                    localStorage.getItem("token")
                }
            }
        );
        alert("Staff Unassigned!");
        loadTreks();
    }
    catch(error){
        alert(error.response.data.message);
    }
}

async function updateTrek(){

    try{

        await api.put(

            "/admin/treks/" + editingTrekId.value,

            trekForm,

            {
                headers:{
                    Authorization:
                    "Bearer " +
                    localStorage.getItem("token")
                }
            }

        );

        alert("Trek Updated Successfully!");

        isEditing.value = false;

        editingTrekId.value = null;
        showEditForm.value = false;

        Object.assign(trekForm,{
            name:"",
            location:"",
            difficulty:"",
            duration_days:"",
            available_slots:"",
            start_date:"",
            end_date:"",
            staff_id:""
        });

        loadTreks();
        loadSummary();

    }

    catch(error){

        alert(error.response.data.message);

    }

}


async function createStaff(){

    try{

        await api.post(

            "/admin/staff",

            staffForm,

            {

                headers:{

                    Authorization:
                    "Bearer " +
                    localStorage.getItem("token")

                }

            }

        );

        alert("Staff Created Successfully!");

        showCreateStaff.value = false;

        Object.assign(staffForm,{

            name:"",
            email:"",
            password:""

        });

        loadSummary();

    }

    catch(error){

        alert(error.response.data.message);

    }

}

async function deactivateStaff(id){

    if(!confirm("Are you sure you want to deactivate this staff member?")){
        return;
    }

    try{

        await api.put(

            "/admin/staff/" + id + "/deactivate",

            {},

            {
                headers:{
                    Authorization:
                    "Bearer " +
                    localStorage.getItem("token")
                }
            }

        );

        alert("Staff deactivated successfully!");

        loadStaff();

        loadSummary();

    }

    catch(error){

        alert(error.response.data.message);

    }

}

async function deactivateUser(id){

    if(!confirm("Are you sure you want to deactivate this user?")){
        return;
    }

    try{

        await api.put(

            "/admin/user/" + id + "/deactivate",

            {},

            {
                headers:{
                    Authorization:
                    "Bearer " +
                    localStorage.getItem("token")
                }
            }

        );

        alert("User deactivated successfully!");

        loadUsers();

        loadSummary();

    }

    catch(error){

        alert(error.response.data.message);

    }

}


async function loadBookings(){

    try{

        const response = await api.get(

            "/admin/bookings",

            {
                headers:{
                    Authorization:
                    "Bearer " +
                    localStorage.getItem("token")
                }
            }

        );

        bookingsTable.value = response.data;

    }

    catch(error){

        alert(error.response.data.message);

    }

}

async function exportCSV(){

    try{

        const response = await api.get(

            "/export/bookings",

            {
                headers:{
                    Authorization:
                    "Bearer " +
                    localStorage.getItem("token")
                }
            }

        );

        alert(response.data.message);

    }

    catch(error){

        alert(error.response.data.message);

    }

}

onMounted(() => {
  loadSummary();
  loadStaff();
  loadTreks();
});

</script>

<style scoped>

.popup-overlay{

    position:fixed;

    top:0;

    left:0;

    width:100%;

    height:100%;

    background:rgba(0,0,0,0.5);

    display:flex;

    justify-content:center;

    align-items:center;

    z-index:1000;

}

.popup-box{

    background:white;

    width:800px;

    max-height:90vh;

    overflow-y:auto;

    padding:25px;

    border-radius:10px;

    box-shadow:0 0 20px rgba(0,0,0,.3);

}

</style>