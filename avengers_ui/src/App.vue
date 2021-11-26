<template lang="pug">
  #app.m-0.p-0
    ul.nav.m-2
      li.nav-item
        a.nav-link( href="#" )
          img(alt="Avengers Data" src="./assets/avengers.png" width="50" height="50")
      li.nav-item.mt-2
        a.nav-link( href="#" )
          | Nav Item 1
      li.nav-item.mt-2
        a.nav-link( href="#" )
          | Nav Item 2
      li.nav-item.mt-2
        a.nav-link( href="#" )
          | Nav Item 3

    .row.row-cols-1
      .col-md
        Avengers
</template>

<script>
import Avengers from "./components/Avengers";

export default {
  name: "App",
  components: {
    Avengers,
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
