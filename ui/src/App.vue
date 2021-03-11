<template>
  <div id="app">
    <Header />
    <router-view />
    </div>
</template>

<script>
import Header from "@/components/Header.vue";

export default {
  name: "App",
  components: { Header },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #f3f3f3;
  padding-top: 47px; // Top NavBar (cv-header) size
  min-height: 100vh;
}
</style>
