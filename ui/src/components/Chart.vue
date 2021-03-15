<script>
import { Line, mixins } from "vue-chartjs";
const { reactiveProp } = mixins;

const opts = {
  responsive: true,
  maintainAspectRatio: false,
  tooltips: {
    callbacks: {
      label: function (tooltipItem) {
        return tooltipItem.yLabel;
      },
    },
  },
  scales: {
    xAxes: [
      {
        ticks: {
          display: false,
        },
      },
    ],
    yAxes: [
      {
        ticks: {
          min: 0,
  },
      },
    ],
  },
};

import { mergeDeep } from "@/tools.js";

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: ["chartData", "options"],
  mounted() {
    this.renderChart(this.chartData, mergeDeep(opts, this.options));
  },
};
</script>

<style></style>
