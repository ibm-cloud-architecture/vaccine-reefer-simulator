<template>
  <div class="home">
    <ReeferInfo :container="container" />
    <div class="separator"></div>
    <div class="right-panel">
      <LiveCharts />
    </div>
  </div>
</template>

<script>
import ReeferInfo from "@/components/ReeferInfo.vue";
import LiveCharts from "@/components/LiveCharts.vue";

export default {
  name: "Home",
  components: {
    ReeferInfo,
    LiveCharts,
  },
  data() {
    return {
      container: {
        id: "C01",
        product: { id: "P01", amount: 50000 },
      },
    };
  },
};
</script>

<style lang="scss" scoped>
.home {
  padding: 50px 0;
  display: flex;
  flex-direction: row;

  .separator {
    background-color: #e0e0e0;
    width: 1px;
    min-width: 1px;
    height: calc(100vh - 150px);
  }

  .right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 50px;
  }
}
</style>
