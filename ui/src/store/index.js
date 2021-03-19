import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    containers: [],
    notifications: [],
    alerts: [],
    records: [],
    freezerMgrURL: "",
  },
  getters: {
    containers: (state) => state.containers,
    getContainerById: (state) => (id) => {
      return state.containers.find((c) => c.reeferID === id);
    },
    notifications: (state) => state.notifications,
    alerts: (state) => state.alerts,
    records: (state) => state.records,
  },
  mutations: {
    addContainers(state, containers) {
      state.containers = [...state.containers, ...containers];
    },
    setContainers(state, containers) {
      state.containers = [...containers];
    },
    removeNotificationById(state, id) {
      state.notifications = [...state.notifications.filter((n) => n.id !== id)];
    },
    addNotification(state, notification) {
      state.notifications = [...state.notifications, notification];
    },
    addAlert(state, alert) {
      state.alerts = [{ ...alert, id: state.alerts.length }, ...state.alerts];
    },
    addRecord(state, record) {
      state.records = [
        ...state.records,
        { ...record, id: state.records.length },
      ];
    },
    setFreezerMgrURL(state, url) {
      state.freezerMgrURL = url;
    },
  },
  actions: {
    async loadContainers(context) {
      try {
        const reefersData = await fetch(
          `${context.state.freezerMgrURL}/reefers`
        );
        const reefers = await reefersData.json();
        context.commit(
          "setContainers",
          reefers
            .map((r) => ({ ...r, product: "P01" }))
            .sort((r1, r2) => r1.reeferID.localeCompare(r2.reeferID))
        );
      } catch (e) {
        const notification = {
          title: "Network error",
          caption: "Unable to fetch reefers",
          kind: "error",
        };
        context.dispatch("addNotification", { notification, persistent: true });
        console.error("loadContainers", e);
      }
    },
    removeNotificationById(context, id) {
      context.commit("removeNotificationById", id);
    },
    addNotification(context, input) {
      let notification = { ...input },
        options = {};
      if (input.notification) {
        notification = input.notification;
        options = input;
      }
      options.timeout = options.timeout || 3;

      notification.id = new Date().getTime();
      context.commit("addNotification", notification);

      if (!options.persistent) {
        setTimeout(() => {
          context.commit("removeNotificationById", notification.id);
        }, options.timeout * 1000);
      }
    },
    addAlert(context, alert) {
      context.commit("addAlert", { ...alert, receivedOn: new Date() });
    },
    addRecord(context, record) {
      context.commit("addRecord", record);
    },
    setFreezerMgrURL(context, url) {
      context.commit("setFreezerMgrURL", url);
    },
  },
});

export default store;
