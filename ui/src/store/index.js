import Vue from 'vue'
import Vuex from 'vuex'
import { freezerMgrUrl } from "@/tools.js"

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    containers: [],
    notifications: [],
    alerts: [],
  },
  getters: {
    containers: (state) => state.containers,
    getContainerById: (state) => (id) => {
      return state.containers.find(c => c.reeferID === id)
    },
    notifications: (state) => state.notifications,
    alerts: (state) => state.alerts,
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
    },
    addAlert(state, alert) {
      state.alerts = [{...alert, id: state.alerts.length}, ...state.alerts]
    },
  },
  actions: {
    async loadContainers(context) {
      try {
        const reefersData = await fetch(`${freezerMgrUrl}/reefers`);
        const reefers = await reefersData.json();
        context.commit("setContainers", reefers.map(r => ({ ...r, product: { id: "P01", amount: 10 } })))
      } catch (e) {
        const notification = {
          title: "Network error", caption: "Unable to fetch reefers", kind: "error"
        }
        context.dispatch("addNotification", { notification, persistent: true })
        console.error("loadContainers", e);
      }
    },
    removeNotificationById(context, id) {
      context.commit("removeNotificationById", id);
    },
    addNotification(context, input) {
      let notification = { ...input }, options = {}
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
    },
    addAlert(context, alert) {
      context.commit("addAlert", { ...alert, receivedOn: new Date() });
    },
  }
})

export default store;