import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import ContainerDetail from '../views/ContainerDetail.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/containers/:id', name: 'ContainerDetail', component: ContainerDetail },
]

const router = new VueRouter({
  routes
})

export default router
