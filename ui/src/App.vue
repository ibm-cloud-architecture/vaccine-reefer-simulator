<template>
  <div id="app">
    <Header />
    <router-view />
    <NotificationCenter />
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import NotificationCenter from "@/components/NotificationCenter.vue";
import { freezerMgrUrl, backendUrl } from "@/tools.js";

export default {
  name: "App",
  components: { Header, NotificationCenter },
  async mounted() {
    this.$store.dispatch("loadContainers");

    const reeferAlerts = new EventSource(`${freezerMgrUrl}/reefers/alerts`);
    reeferAlerts.onmessage = (message) => console.log(message);

    reeferAlerts.onmessage = (message) => {
      const alert = JSON.parse(message.data);
      this.$store.dispatch("addAlert", alert);
    };

    const data = await fetch(`${backendUrl}/health`);
    console.log(await data.json());
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #f3f3f3;
  padding-top: 48px; // Top NavBar (cv-header) size
  min-height: 100vh;
}
</style>
