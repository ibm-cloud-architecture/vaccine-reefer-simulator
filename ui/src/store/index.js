import Vue from 'vue'
import Vuex from 'vuex'
import { serverURL } from "@/tools.js"

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    containers: [],
    notifications: [],
  },
  getters: {
    containers: (state) => state.containers,
    getContainerById: (state) => (id) => {
      return state.containers.find(c => c.reeferID === id)
  },
    notifications: (state) => state.notifications,
  },
  mutations: {
    addContainers(state, containers) {
      state.containers = [...state.containers, ...containers]
    },
    setContainers(state, containers) {
      state.containers = [...containers]
    },
    removeNotificationById(state, id) {
      state.notifications = [...state.notifications.filter(n => n.id !== id)]
    },
    addNotification(state, notification) {
      state.notifications = [...state.notifications, notification]
    }
  },
  actions: {
    async loadContainers(context) {
      const reefersData = await fetch(`${serverURL}/reefers`);
      const reefers = await reefersData.json();
    },
    removeNotificationById(context, id) {
      context.commit("removeNotificationById", id);
    },
    addNotification(context, input) {
      let notification = {...input}, options = {}
      if (input.notification) {
        notification = input.notification
        options = input
      }
      options.timeout = options.timeout || 3

      notification.id = (new Date()).getTime()
      context.commit("addNotification", notification);

      if (!options.persistent) {
        setTimeout(() => {
          context.commit("removeNotificationById", notification.id)
        }, options.timeout * 1000)
      }
    }
  }
})

export default store;