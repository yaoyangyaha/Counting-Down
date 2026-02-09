import { createRouter, createWebHistory } from 'vue-router'

// @ts-ignore
import Home from '../views/Home.vue'
// @ts-ignore
import Login from '../views/Login.vue'
// @ts-ignore
import Register from '../views/Register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Home },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
  ],
})

export default router
