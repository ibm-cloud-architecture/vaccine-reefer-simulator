<template>
  <div class="reefer-info">

    <cv-tag class="tag" kind="green" label="Everything OK" />

    <cv-structured-list>
      <template slot="items">
        <cv-structured-list-item>
          <cv-structured-list-heading>Container ID</cv-structured-list-heading>
          <cv-structured-list-data>12345</cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading># Vaccines</cv-structured-list-heading>
          <cv-structured-list-data>50,000</cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading>Location</cv-structured-list-heading>
          <cv-structured-list-data>See on map</cv-structured-list-data>
        </cv-structured-list-item>

        <cv-structured-list-item>
          <cv-structured-list-heading>Status</cv-structured-list-heading>
          <cv-structured-list-data>Loaded</cv-structured-list-data>
        </cv-structured-list-item>
      </template>
    </cv-structured-list>
  </div>
</template>

<script>
export default {
  name: "ReeferInfo",
};
</script>

<style lang="scss" scoped>
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
}
</style>
