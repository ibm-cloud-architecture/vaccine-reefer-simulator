<template>
  <div class="charts">
    <Chart class="chart" :chartData="tempData" :options="tempOptions" />
    <Chart class="chart" :chartData="co2Data" :options="co2Options" />
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
      this.temperatures.push(-72.5);
      this.temperatures_timestamps.push(new Date());
      this.co2values.push(408.5);
      this.co2values_timestamps.push(new Date());
    }
    setInterval(() => {
      this.addTemperaturePoint(Math.random() * 5 - 70, new Date());
      this.addCO2Point(Math.random() * 5 + 408, new Date());
    }, 500);
  },
  data: function () {
    return {
      temperatures: [],
      temperatures_timestamps: [],
      co2values: [],
      co2values_timestamps: [],
      tempOptions: {
        scales: {
          yAxes: [
            {
              ticks: {
                min: -80,
                
              }
            }
          ]
        }
      },
      co2Options: {
        scales: {
          yAxes: [
            {
              ticks: {
                min: 0
              }
            }
          ]
        }
      }
    };
  },
  computed: {
    tempData: function () {
      return {
        labels: this.temperatures_timestamps,
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
        labels: this.co2values_timestamps,
        datasets: [
          {
            label: "CO₂ (ppm)",
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
    addTemperaturePoint: function (value, time) {
      this.temperatures.push(value);
      this.temperatures_timestamps.push(time);

      if (this.temperatures.length > SECS) {
        this.temperatures.shift();
        this.temperatures_timestamps.shift();
      }
    },
    addCO2Point: function (value, time) {
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
  flex-wrap: wrap;

  .chart {
    max-height: 200px;
    margin-right: 20px;
  }
}
</style>
