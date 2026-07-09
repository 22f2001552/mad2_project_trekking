import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import StaffDashboard from '../views/StaffDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'
import MyBookings from '../views/MyBookings.vue'
import ProfileView from "../views/ProfileView.vue"
import ParticipantsView from "../views/ParticipantsView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard,
    },
    {
      path: '/staff',
      name: 'staff',
      component: StaffDashboard,
    },
    {
      path: '/user',
      name: 'user',
      component: UserDashboard,
    },
    {
      path: "/my-bookings",
      name: "my-bookings",
      component: MyBookings,
    },
    {
    path: "/profile",
    name: 'profile',
    component: ProfileView,
    },
    {
    path: "/participants/:trekId",
    name: "participants",
    component: ParticipantsView,
    },
  ],
})

export default router
