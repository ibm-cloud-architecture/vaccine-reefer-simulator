<template>
  <div class="reefer-info">

    <cv-tag class="tag" kind="green" label="Everything OK" />

    <cv-structured-list>
      <template slot="items">
        <cv-structured-list-item>
          <cv-structured-list-heading>Container ID</cv-structured-list-heading>
          <cv-structured-list-data>{{ container.id }}</cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading>Product</cv-structured-list-heading>
          <cv-structured-list-data>{{
            container.product.id
          }}</cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading># records</cv-structured-list-heading>
          <cv-structured-list-data>
            <cv-number-input :label="null" v-model="container.product.amount">
            </cv-number-input>
          </cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading>Simulation</cv-structured-list-heading>
          <cv-structured-list-data>
            <div class="simulator-selector">
              <cv-dropdown :value="simulation" v-model="simulation">
                <cv-dropdown-item
                  v-for="simulation in simulations"
                  :key="simulation.type"
                  :value="simulation.type"
                  >{{ simulation.title }}</cv-dropdown-item
                >
              </cv-dropdown>
              <cv-icon-button
                kind="primary"
                :icon="icon"
                :disabled="!simulation"
                @click="runSimulation"
                label="Run simulation"
                tip-position="bottom"
                tip-alignment="center"
              />
            </div>
          </cv-structured-list-data>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script>
import Checkmark32 from "@carbon/icons-vue/es/checkmark/32";

export default {
  name: "ReeferInfo",
  props: ["container"],
  data() {
    return {
      icon: Checkmark32,
      simulation: "",
      simulations: [
        { type: "tempgrowth", title: "Temperature Growth" },
        { type: "co2sensor", title: "CO₂ Sensor" },
        { type: "temperature", title: "Temperature" },
        { type: "o2sensor", title: "O₂ Sensor" },
        { type: "poweroff", title: "Power Off" },
        { type: "normal", title: "Normal" },
      ],
    };
  },
  methods: {
    async runSimulation() {
      const load = {
        containerID: this.container.id,
        nb_of_records: this.container.product.amount,
        product_id: this.container.product.id,
        simulation: this.simulation,
      };

      const controlResponse = await fetch("http://localhost:5000/control", {
        method: "POST",
        body: JSON.stringify(load),
      });
      console.log(await controlResponse.text());
    },
  },
};
</script>

<style lang="scss">
.reefer-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 50px;

  .tag {
    width: max-content;
    margin: 50px 0;
  }

  .cv-structured-list-heading {
    vertical-align: inherit;
  }

  .bx--number {
    .bx--label {
      display: none;
    }
  }

  .simulator-selector {
    display: flex;
    width: 250px;

    .bx--dropdown {
      height: 48px;
      max-height: 48px;
    }
  }
}
</style>
