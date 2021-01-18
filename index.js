const byDistrict = (district) => (street) =>
  street.districts.includes(district);

window.addEventListener("load", () => {
  document.getElementById("loading-spinner").style.opacity = 0;

  const App = new Vue({
    el: "#app",
    data: {
      streets: STREETS,
      selectedStreet: null,
      selectedDistrict: "all",
    },
    computed: {
      districts() {
        return new Set(
          this.streets
            .map((s) => s.districts)
            .flat()
            .sort()
        );
      },
    },
    methods: {
      selectRandomStreet() {
        if (this.selectedDistrict === "all") {
          const i = Math.floor(Math.random() * this.streets.length);
          this.selectedStreet = this.streets[i];
        } else {
          const streetsInDistrict = this.streets.filter(
            byDistrict(this.selectedDistrict)
          );
          const i = Math.floor(Math.random() * streetsInDistrict.length);
          const streetIndex = this.streets.findIndex(
            (street) =>
              street.google_maps_link === streetsInDistrict[i].google_maps_link
          );
          this.selectedStreet = this.streets[streetIndex];
        }
        Vue.nextTick(() =>
          this.$refs.card.scrollIntoView({ behavior: "smooth" })
        );
      },
    },
  });
});
