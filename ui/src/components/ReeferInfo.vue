<template>
  <div class="reefer-info">
    <img alt="Reefer" src="../assets/reefer.png" />

    <cv-tag class="tag" kind="green" v-if="container" label="Everything OK" />
    <cv-tag-skeleton class="tag" v-if="!container" />

    <cv-structured-list>
      <template slot="items">
        <cv-structured-list-item>
          <cv-structured-list-heading>Container ID</cv-structured-list-heading>
          <cv-structured-list-data>
            <cv-dropdown-skeleton v-if="!container" />
            <cv-combo-box
              v-if="container"
              :auto-filter="true"
              :auto-highlight="true"
              :value="container.reeferID"
              :options="containersOptions"
              @change="changeContainer"
            >
            </cv-combo-box>
          </cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading>Product</cv-structured-list-heading>
          <cv-structured-list-data>
            <span v-if="container">{{ container.product.id }}</span>
            <cv-skeleton-text v-if="!container" />
          </cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading># records</cv-structured-list-heading>
          <cv-structured-list-data>
            <div class="row">
              <cv-button-skeleton v-if="!container" />
              <cv-number-input
                v-if="container"
                :min="0"
                :max="container.capacity"
                v-model="container.product.amount"
              >
              </cv-number-input>
              <span v-if="container"> / {{ container.capacity }}</span>
            </div>
          </cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading>Simulation</cv-structured-list-heading>
          <cv-structured-list-data>
            <div class="simulation-selector">
              <cv-dropdown
                :value="simulation"
                v-if="container"
                v-model="simulation"
              >
                <cv-dropdown-item
                  v-for="simulation in simulations"
                  :key="simulation.type"
                  :value="simulation.type"
                  >{{ simulation.title }}</cv-dropdown-item
                >
              </cv-dropdown>
              <cv-icon-button
                v-if="container"
                kind="primary"
                :icon="icon"
                :disabled="!simulation"
                @click="runSimulation"
                label="Run simulation"
                tip-position="bottom"
                tip-alignment="center"
              />
              <cv-button-skeleton v-if="!container" />
            </div>
          </cv-structured-list-data>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
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
  computed: {
    ...mapGetters(["containers"]),
    containersOptions: {
      get() {
        return this.containers.map((c) => ({
          name: c.reeferID,
          label: c.reeferID,
          value: c.reeferID,
        }));
      },
    },
  },
  methods: {
    changeContainer(container) {
      if (container) {
        this.$router.push({
          name: "ContainerDetail",
          params: { id: container },
        });
      }
    },
    async runSimulation() {
      const load = {
        containerID: this.container.reeferID,
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

  img {
    width: 300px;
    min-height: 225px;
  }

  .tag {
    width: max-content;
    margin: 50px 0;
  }

  .cv-structured-list-heading {
    vertical-align: inherit;
  }

  .row {
    display: flex;
    flex-direction: row;
    align-items: center;

    span {
      white-space: nowrap;
      padding-left: 10px;
    }
  }

  .bx--number {
    .bx--label {
      display: none;
    }
  }

  .bx--list-box__selection {
    display: none; // Hide container selector "clear" button
  }

  .simulation-selector {
    display: flex;
    width: 250px;

    .bx--dropdown {
      height: 48px;
      max-height: 48px;
    }
  }
}
</style>
