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
          <cv-structured-list-heading>Brand</cv-structured-list-heading>
          <cv-structured-list-data>
            <span v-if="container">{{ container.brand }}</span>
            <cv-skeleton-text v-if="!container" />
          </cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading>Type</cv-structured-list-heading>
          <cv-structured-list-data>
            <span v-if="container">{{ container.type }}</span>
            <cv-skeleton-text v-if="!container" />
          </cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading>Product</cv-structured-list-heading>
          <cv-structured-list-data>
            <cv-button-skeleton v-if="!container" />
            <cv-text-input v-if="container" v-model="product">
            </cv-text-input>
          </cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading># records</cv-structured-list-heading>
          <cv-structured-list-data>
            <cv-button-skeleton v-if="!container" />
            <cv-number-input v-if="container" :min="0" v-model="nb_of_records">
            </cv-number-input>
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
      nb_of_records: 0,
      product: "",
      receivedRecords: [],
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
  mounted() {
    if (this.container != null) {
      this.product = this.container.product;
    } else {
      this.product = "P01"
    }
   
    this.showSimulation();
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
        nb_of_records: this.nb_of_records,
        product_id: this.product,
        simulation: this.simulation,
      };

      const controlResponse = await fetch("/control", {
        method: "POST",
        body: JSON.stringify(load),
      });
      this.receivedRecords = await controlResponse.json();
      this.showSimulation();
    },
    showSimulation(num = 0) {
      this.$store.dispatch("addRecord", this.receivedRecords[num])
      if (num < this.receivedRecords.length - 1) {
        setTimeout(() => this.showSimulation(num + 1), 500);
      }
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

  .bx--number, .cv-text-input {
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
