<template>
  <div id="app">
    <Main/>
  </div>
</template>

<script>
import Main from './components/Main.vue'
import io from "socket.io-client";

export default {
  name: "App",
  components: {
    Main
  },
  mounted() {
    this.sockets.subscribe("my_response", (data) => {
      console.log(data);
    });
  },
  methods: {
    sendserv() {
      this.$socket.emit("real_estate_data", "real_estate_data");
      console.log("Отправил");
    },
  },
  sockets: {
    connect: function () {
      console.log("socket connected");
    },
  },
  data() {
    return {
      socket: io(),
      selected: "",
    };
  },
};
</script>

<style>
#app {
  font-family: Montserrat, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
