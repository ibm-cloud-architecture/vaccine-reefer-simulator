import Vue from 'vue'
import Vuex from 'vuex'
import { serverURL } from "@/tools.js"

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    containers: []
  },
  getters: {
    containers: (state) => state.containers,
    getContainerById: (state) => (id) => {
      return state.containers.find(c => c.reeferID === id)
    }
  },
  mutations: {
    addContainers(state, containers) {
      state.containers = [...state.containers, ...containers]
    }
  },
  actions: {
    async loadContainers(context) {
      const reefersData = await fetch(`${serverURL}/reefers`);
      const reefers = await reefersData.json();
      context.commit("addContainers", reefers.map(r => ({...r, product: { id: "P01", amount: 10 } })))
    }
  }
})

export default store;