<template>
  <div id="app">
    <colorization-page></colorization-page>
  </div>
</template>

<script>
import ColorizationPage from './components/ColorizationPage'

export default {
  name: 'App',
  components: {
    ColorizationPage
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
