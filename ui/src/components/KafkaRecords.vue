<template>
  <div class="kafka-records" v-if="container">
    <h2>Alerts</h2>
    <cv-structured-list :condensed="true">
      <template slot="headings">
        <cv-structured-list-heading>Type</cv-structured-list-heading>
        <cv-structured-list-heading>Date</cv-structured-list-heading>
      </template>
      <template slot="items">
        <cv-structured-list-item
          class="alert"
          v-for="alert in alerts"
          :key="alert.id"
        >
          <cv-structured-list-data>{{ alert.type }}</cv-structured-list-data>
          <cv-structured-list-data>{{
            alert.receivedOn
          }}</cv-structured-list-data>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script>
export default {
  name: "KakfaRecords",
  props: ["container"],
  computed: {
    alerts: function () {
      return this.$store.getters.alerts.filter(
        (a) => a.containerID === this.container.reeferID
      );
    },
  },
};
</script>

<style lang="scss" scoped>
.kafka-records {
  background: white;
  padding: 50px 10px;

  h2 {
    text-align: left;
  }

  .alert {
    animation: blinker 1s linear;

    @keyframes blinker {
      50% {
        opacity: 0;
      }
    }
  }
}
</style>
