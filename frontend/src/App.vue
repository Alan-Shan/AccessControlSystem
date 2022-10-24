<template>
  <div id="app">
    <NavigationBar/>
    <router-view></router-view>
  </div>
</template>
<script>
import NavigationBar from "@/components/NavigationBar";
export default {
  name: "App",
  components: {
    NavigationBar,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
h1 {
  margin-bottom: 1rem!important;
}
</style>
