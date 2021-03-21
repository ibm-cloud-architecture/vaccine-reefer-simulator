<template>
  <cv-header aria-label="Carbon header">
    <cv-header-menu-button aria-label="Header menu" aria-controls="side-nav" />

    <cv-header-name to="/" prefix="IBM">
      Vaccine Reefer Simulator
    </cv-header-name>

    <cv-header-nav aria-label="Carbon nav">
      <cv-header-menu aria-label="Links" title="Links">
        <cv-header-menu-item
          v-for="link in externalLinks"
          :key="link.link"
          target="_blank"
          :href="link.link"
        >
          {{ link.title }}
        </cv-header-menu-item>
      </cv-header-menu>
    </cv-header-nav>

    <template v-slot:left-panels>
      <cv-side-nav id="side-nav" fixed>
        <cv-side-nav-items>
          <cv-header-side-nav-items>
            <cv-header-menu-item
              v-for="link in externalLinks"
              :key="link.link"
              target="_blank"
              :href="link.link"
            >
              {{ link.title }}
            </cv-header-menu-item>
          </cv-header-side-nav-items>
        </cv-side-nav-items>
      </cv-side-nav>
    </template>
  </cv-header>
</template>

<script>
import { backendURL } from "@/tools.js";

export default {
  name: "Header",
  data() {
    return {
      externalLinks: [
        {
          title: "EDA",
          link: "https://ibm-cloud-architecture.github.io/refarch-eda/",
        },
        {
          title: "Vaccine Delivery at Scale",
          link:
            "https://ibm-cloud-architecture.github.io/vaccine-solution-main/",
        },
        { title: "Backend Swagger", link: `${backendURL}/apidocs` },
      ],
    };
  },
};
</script>

<style lang="scss">
.bx--header__name--prefix {
  margin-right: 3px; // Separate "IBM" from "Vaccine Reefer Simulator"
}
</style>
