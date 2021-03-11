<template>
  <div class="controls">
    <div
      v-for="button in buttons"
      :key="button.title"
      class="button-and-explanation"
    >
      <cv-button @click="control(button.action)">
        {{ button.title }}
      </cv-button>

      <cv-tooltip :tip="button.tip"></cv-tooltip>
    </div>
  </div>
</template>

<script>
export default {
  name: "ReeferControl",
  data() {
    return {
      buttons: [
        { title: "Open Door", tip: "This will make the temperature raise abruptly", action: "open-door" },
        { title: "Stop Power", tip: "This will make the temperature raise slowly", action: "stop-power" },
        { title: "Gen CO₂ event", tip: "This will trigger an alarm", action: "co2-event" },
      ],
    };
  },
  methods: {
    control: function(action) {
      console.log(action);
    },
  },
};
</script>

<style lang="scss" scoped>
.controls {
  margin-top: 50px;
  display: flex;
  flex-direction: column;

  .button-and-explanation {
    margin-bottom: 20px;
    display: flex;
    flex-direction: row;

    *:first-of-type {
      margin-right: 10px;
    }
  }
}
</style>
