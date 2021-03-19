<template>
  <div class="charts">
    <Chart
      class="chart"
      :chartData="tempData"
      :min="tempMinMax.min"
      :max="tempMinMax.max"
    />
    <Chart
      class="chart"
      :chartData="co2Data"
      :min="co2MinMax.min"
      :max="co2MinMax.max"
    />
  </div>
</template>

<script>
import Chart from "@/components/Chart.vue";

const TEMP_PADDING = 20;
const CO2_PADDING = 10;
const round = (input) => Math.round(input / 5) * 5;

export default {
  name: "LiveCharts",
  props: ["container"],
  components: {
    Chart,
  },
  computed: {
    records: function () {
      if (!this.container) {
        return [];
      }
      return this.$store.getters.records.filter(
        (r) => r.container_id === this.container.reeferID
      );
    },
    temperatures: function () {
      return this.records.map((r) => r.temperature);
    },
    measurement_times: function() {
      return this.records.map((r) => r.measurement_time);
    },
    co2values:  function() {
      return this.records.map((r) => r.carbon_dioxide_level);
    },
    tempMinMax: function () {
      let min = round(Math.min(...this.temperatures) - TEMP_PADDING);
      let max = round(Math.max(...this.temperatures) + TEMP_PADDING);
      return { min, max };
    },
    co2MinMax: function () {
      let min = round(Math.min(...this.co2values) - CO2_PADDING);
      let max = round(Math.max(...this.co2values) + CO2_PADDING);
      return { min, max };
    },
    tempData: function () {
      return {
        labels: this.measurement_times,
        datasets: [
          {
            label: "Temperature (C)",
            backgroundColor: "#b51818",
            borderColor: "#b51818",
            data: this.temperatures,
            fill: false,
          },
        ],
      };
    },
    co2Data: function () {
      return {
        labels: this.measurement_times,
        datasets: [
          {
            label: "CO₂ (%)",
            backgroundColor: "#00b97c",
            borderColor: "#00b97c",
            data: this.co2values,
            fill: false,
          },
        ],
      };
    },
  },
};
</script>

<style lang="scss" scoped>
.charts {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  .chart {
    max-height: 200px;
    margin-right: 20px;
  }
}
</style>
