<template>
  <div class="container-detail" v-if="container">
    <ReeferInfo :container="container" :containers="containers" />
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
  name: "ContainerDetail",
  components: {
    ReeferInfo,
    LiveCharts,
    KafkaRecords,
  },
  mounted() {
    this.loadContainerByIdInRoute();
    if (!this.container) {
      this.$router.push("/home");
    }
  },
  watch: {
    "$route.params.id": {
      handler: function () {
        this.loadContainerByIdInRoute();
      },
      immediate: true,
    },
  },
  methods: {
    loadContainerByIdInRoute() {
      this.container = this.containers.find(
        (c) => c.id === this.$route.params.id
      );
    },
  },
  data() {
    return {
      container: null,
      containers: [
        { id: "C01", product: { id: "P01", amount: 10000 } },
        { id: "C02", product: { id: "P01", amount: 20000 } },
        { id: "C03", product: { id: "P01", amount: 30000 } },
        { id: "C04", product: { id: "P01", amount: 40000 } },
        { id: "C05", product: { id: "P01", amount: 50000 } },
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
.container-detail {
  padding: 0;
  display: flex;
  flex-direction: row;

  .right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: white;
    padding: 50px;
    min-height: calc(100vh - 48px);
  }
}
</style>
