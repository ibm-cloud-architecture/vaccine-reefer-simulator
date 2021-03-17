<script>
import { Line, mixins } from "vue-chartjs";
const { reactiveProp } = mixins;

const opts = {
  responsive: true,
  maintainAspectRatio: false,
  tooltips: {
    enabled: false,
  },
  scales: {
    xAxes: [
      {
        ticks: {
          display: false,
        },
      },
    ],
  },
};

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: ["chartData", "min", "max"],
  mounted() {
    this.renderChart(this.chartData, opts);
  },
  watch: {
    min(min) {
      this.$data._chart.options.scales.yAxes[0].ticks.min = min;
      this.$data._chart.update();
    },
    max(max) {
      this.$data._chart.options.scales.yAxes[0].ticks.max = max;
      this.$data._chart.update();
    },
  },
};
</script>

<style></style>
