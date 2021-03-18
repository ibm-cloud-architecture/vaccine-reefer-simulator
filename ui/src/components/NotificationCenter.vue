<template>
  <div class="notification-panel">
    <cv-toast-notification
      v-for="notification in notifications"
      :key="notification.id"
      :kind="notification.kind"
      :title="notification.title"
      :sub-title="notification.subTitle"
      :caption="notification.caption"
      @close="removeNotification(notification.id)"
    />
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "NotificationCenter",
  computed: {
    ...mapGetters(["notifications"]),
  },
  methods: {
    removeNotification(id) {
      this.$store.dispatch("removeNotificationById", id);
    },
  },
};
</script>

<style lang="scss" scoped>
.notification-panel {
  position: fixed;
  right: 0;
  bottom: 0;
}
</style>