import Vue from "vue";
import App from "./App.vue";

// socket io
import * as io from "socket.io-client";
import VueSocketIO from "vue-socket.io";

Vue.use(
  new VueSocketIO({
    debug: true,
    connection: io('http://localhost:5000'), // options object is Optional
  })
);

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
