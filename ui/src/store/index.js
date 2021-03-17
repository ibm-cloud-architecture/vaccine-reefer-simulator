import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    containers: []
  },
  getters: {
    containers: (state) => state.containers,
    getContainerById: (state) => (id) => {
      return state.containers.find(c => c.id === id)
    }
  },
  mutations: {
    addContainers(state, containers) {
      state.containers = [...state.containers, ...containers]
    }
  },
  actions: {
    loadContainers(context) {
      const containers = [
        { id: "C01", product: { id: "P01", amount: 10000 } },
        { id: "C02", product: { id: "P01", amount: 20000 } },
        { id: "C03", product: { id: "P01", amount: 30000 } },
        { id: "C04", product: { id: "P01", amount: 40000 } },
        { id: "C05", product: { id: "P01", amount: 50000 } },
      ];
      context.commit("addContainers", containers)
    }
  }
})

export default store;