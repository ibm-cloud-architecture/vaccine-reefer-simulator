<template>
  <div class="charts">
    <Chart :chartData="tempData" />
    <Chart :chartData="co2Data" />
  </div>
</template>

<script>
import Chart from "@/components/Chart.vue";

const SECS = 20;

export default {
  name: "LiveCharts",
  components: {
    Chart,
  },
  mounted() {
    for (let index = 0; index < SECS; index++) {
      this.temperatures.push(22.5);
      this.temperatures_timestamps.push(new Date());
      this.co2values.push(122.5);
      this.co2values_timestamps.push(new Date());
    }
    setInterval(() => {
      this.addTemperaturePoint(Math.random() * 5 + 20, new Date());
      this.addCO2Point(Math.random() * 5 + 120, new Date());
    }, 500);
  },
  data: function() {
    return {
      temperatures: [],
      temperatures_timestamps: [],
      co2values: [],
      co2values_timestamps: [],
    };
  },
  computed: {
    tempData: function() {
      return {
        labels: this.temperatures_timestamps,
        datasets: [
          {
            label: "Temperature (C)",
            backgroundColor: "#d05659",
            borderColor: "#d05659",
            data: this.temperatures,
            fill: false,
          },
        ],
      };
    },
    co2Data: function() {
      return {
        labels: this.co2values_timestamps,
        datasets: [
          {
            label: "CO₂ (g/m³)",
            backgroundColor: "#00b97c",
            borderColor: "#00b97c",
            data: this.co2values,
            fill: false,
          },
        ],
      };
    },
  },
  methods: {
    addTemperaturePoint: function(value, time) {
      this.temperatures.push(value);
      this.temperatures_timestamps.push(time);

      if (this.temperatures.length > SECS) {
        this.temperatures.shift();
        this.temperatures_timestamps.shift();
      }
    },
    addCO2Point: function(value, time) {
      this.co2values.push(value);
      this.co2values_timestamps.push(time);

      if (this.co2values.length > SECS) {
        this.co2values.shift();
        this.co2values_timestamps.shift();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.charts {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  max-height: 200px;
}
</style>
