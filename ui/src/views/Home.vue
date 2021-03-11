<template>
  <div class="home">
    <ReeferInfo />
    <div class="separator"></div>
    <div class="right-panel">
      <LiveCharts />
      <ReeferControl />
    </div>
  </div>
</template>

<script>
import ReeferInfo from "@/components/ReeferInfo.vue";
import ReeferControl from "@/components/ReeferControl.vue";
import LiveCharts from "@/components/LiveCharts.vue";

export default {
  name: "Home",
  components: {
    ReeferInfo,
    ReeferControl,
    LiveCharts,
  },
};
</script>

<style lang="scss" scoped>
.home {
  padding: 50px;
  display: flex;
  flex-direction: row;

  .separator {
    background-color: #e0e0e0;
    width: 1px;
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
