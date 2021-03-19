<template>
  <div class="container-detail">
    <ReeferInfo :container="container" />
    <div class="separator"></div>
    <div class="right-panel">
      <LiveCharts :container="container" />
      <KafkaRecords :container="container" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import ReeferInfo from "@/components/ReeferInfo.vue";
import LiveCharts from "@/components/LiveCharts.vue";
import KafkaRecords from "@/components/KafkaRecords.vue";

export default {
  name: "ContainerDetail",
  components: {
    ReeferInfo,
    LiveCharts,
    KafkaRecords
  },
  mounted() {
    this.loadContainerByIdInRoute();
  },
  watch: {
    containers: function () {
        this.loadContainerByIdInRoute();
      },
    "$route.params.id": function () {
      this.loadContainerByIdInRoute();
    },
  },
  methods: {
    loadContainerByIdInRoute() {
      this.container = this.getContainerById(this.$route.params.id);
      if (this.containers.length > 0 && !this.container) {
        this.$router.push("/");
      }
    },
  },
  computed: {
    ...mapGetters(["getContainerById", "containers"]),
  },
  data() {
    return {
      container: null,
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
