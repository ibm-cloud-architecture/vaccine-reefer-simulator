<template>
  <div class="home">
    <div class="tiles">
      <cv-tile
        class="tile"
        v-for="container in containers"
        :key="container.id"
        kind="clickable"
        :to="`/containers/${container.id}`"
      >
        <h1>{{ container.id }}</h1>
        <p>Details and simulation</p>
      </cv-tile>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "Home",
  computed: {
    ...mapGetters(["containers"]),
  },
};
</script>

<style lang="scss" scoped>
.home {
  background-color: white;
  padding: 50px;
  min-height: calc(100vh - 48px);

  .tiles {
    display: flex;
    flex-wrap: wrap;
    $separation: 25px;

    .tile {
      margin: 0 $separation $separation 0;
    }
  }
}
</style>