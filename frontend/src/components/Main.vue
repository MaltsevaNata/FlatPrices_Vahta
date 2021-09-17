<template>
  <div>
    <div class="content">
        <header>
          <div class="logo_pic">
            <img src="@/logo.png" alt="Vaxta" class="logo_pic_img" />
          </div>
          <div class="wrap_sub1">
            <p class="subtitle_1">
              Сервис для оценивания стоимости объекта недвижимости
            </p>
          </div>
          <div class="wrap_sub2">
            <p class="subtitle_2">
              С использованием технологии машинного обучения
            </p>
          </div>

          <button class="btn_check_box">
            <p class="but_check">Оценить стоимость</p>
          </button>
        </header>
      </div>









    <input type="radio" v-model="type" v-bind:value="flat" />Квартира
    <input type="radio" v-model="type" v-bind:value="home" />Частный дом
    <br />

    <form @submit.prevent="send_data">
      <div class="input_field">
        <p>Регион</p>
        <input type="text" v-model="region" id="region" required />
      </div>

      <div class="input_field">
        <p>Площадь объекта</p>
        <input type="text" v-model="total_area" id="total_area" required />
      </div>

      <div class="input_field">
        <p>Жилая площадь</p>
        <input type="text" v-model="living_area" id="living_area" required />
      </div>

      <div class="input_field">
        <p>Площадь кухни</p>
        <input type="text" v-model="kitchen_area" id="kitchen_area" required />
      </div>

      <div class="input_field">
        <p>Год постройки</p>
        <input type="text" v-model="year" id="year" required />
      </div>

      <div class="input_field">
        <p>Минут до метро(пешком)</p>
        <input type="text" v-model="underground" id="underground" required />
      </div>

      <div class="input_field">
        <p>Материал дома</p>
        <input type="text" v-model="material_type" id="region" required />
      </div>

      <div class="input_field">
        <p>Адрес</p>
        <input type="text" v-model="address" id="address" required />
      </div>

      <div class="input_field">
        <p>Номер этажа</p>
        <input type="text" v-model="floor_number" id="floor_number" required />
      </div>

      <div class="input_field">
        <p>Всего этажей</p>
        <input type="text" v-model="total_floors" id="total_floors" required />
      </div>

      <transition name="fade">
        <div class="input_field" v-if="this.type == home">
          <p>Площадь прилегающих участков</p>
          <input type="text" v-model="land" id="land" required />
        </div>
      </transition>

      <button>Отправить</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "Main",
  props: {},
  data() {
    return {
      region: "",
      total_area: "",
      living_area: "",
      kitchen_area: "",
      year: "",
      underground: "",
      material_type: "",
      address: "",
      floor_number: "",
      total_floors: "",
      land: "",
      picked: "",
      active: true,
      flat: 0,
      home: 1,
      type: "",
    };
  },
  methods: {
    send_data: function () {
      this.$socket.emit(
        "real_estate_data",
        JSON.stringify({
          region: this.region,
          total_area: this.total_area,
          living_area: this.living_area,
          kitchen_area: this.kitchen_area,
          year: this.year,
          underground: this.underground,
          material_type: this.material_type,
          address: this.address,
          floor_number: this.floor_number,
          total_floors: this.total_floors,
          land: this.land,
        })
      );
    },
  },
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active до версии 2.1.8 */ {
  opacity: 0;
}


/* montserrat-regular - latin */
@font-face {
  font-family: "Montserrat", sans-serif;
  font-style: normal;
  font-weight: 400;
  src: local(""),
    url("../fonts/montserrat-v18-latin-regular.woff2") format("woff2"),
    /* Chrome 26+, Opera 23+, Firefox 39+ */
      url("../fonts/montserrat-v18-latin-regular.woff") format("woff"); /* Chrome 6+, Firefox 3.6+, IE 9+, Safari 5.1+ */
}
/* montserrat-500 - latin */
@font-face {
  font-family: "Montserrat", sans-serif;
  font-style: normal;
  font-weight: 500;
  src: local(""), url("../fonts/montserrat-v18-latin-500.woff2") format("woff2"),
    /* Chrome 26+, Opera 23+, Firefox 39+ */
      url("../fonts/montserrat-v18-latin-500.woff") format("woff"); /* Chrome 6+, Firefox 3.6+, IE 9+, Safari 5.1+ */
}
/* montserrat-700 - latin */
@font-face {
  font-family: "Montserrat", sans-serif;
  font-style: normal;
  font-weight: 700;
  src: local(""), url("../fonts/montserrat-v18-latin-700.woff2") format("woff2"),
    /* Chrome 26+, Opera 23+, Firefox 39+ */
      url("../fonts/montserrat-v18-latin-700.woff") format("woff"); /* Chrome 6+, Firefox 3.6+, IE 9+, Safari 5.1+ */
}
/* montserrat-900 - latin */
@font-face {
  font-family: "Montserrat", sans-serif;
  font-style: normal;
  font-weight: 900;
  src: local(""), url("../fonts/montserrat-v18-latin-900.woff2") format("woff2"),
    /* Chrome 26+, Opera 23+, Firefox 39+ */
      url("../fonts/montserrat-v18-latin-900.woff") format("woff"); /* Chrome 6+, Firefox 3.6+, IE 9+, Safari 5.1+ */
}
.content {
  background: url(../bg.png) no-repeat center top;
  background-size: cover;
  max-width: 100%;
  height: 100vh;
}

header {
  min-height: 47px;
  width: 100%;
  color: #958e86;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  font-style: normal;
  font-weight: normal;
  font-size: 24px;
  line-height: 29px;
  font-family: "Montserrat";
  font-weight: bold;
  font-size: 60px;
  line-height: 176px;
  color: #8d2e2c;

  text-align: center;
}

.subtitle_1 {
  font-family: Montserrat;
  font-style: normal;
  font-weight: bold;
  font-size: 36px;
  line-height: 44px;
  text-align: center;
  color: #958e86;
  max-width: 762px;
}

.subtitle_2 {
  font-family: Montserrat;
  font-style: normal;
  font-weight: bold;
  font-size: 18px;
  line-height: 22px;
  text-align: center;
  color: #807b7a;
  opacity: 0.4;
}

.logo_pic {
  width: 100%;
  margin-bottom: 0;
  margin-top: 20px;
}

.logo_pic_img {
  margin-bottom: 0;
}

.wrap_sub1 {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.wrap_sub2 {
  width: 100%;
}

.but_check {
  font-family: Montserrat;
  font-style: normal;
  font-weight: 600;
  font-size: 36px;
  line-height: 44px;
  color: #444040;
}

.btn_check_box {
  background: #fdf8f8;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(15px);

  border-radius: 60px;
  padding: 18px 65px;
  margin-top: 58px;
  transition: 0.3s ease-in-out;
}

.btn_check_box:hover,
.btn_check_box:focus,
.btn_check_box:active {
  background: #dfd6d6;
}

.choose_wrap {
  background-color: rgba(251, 251, 251, 0.55);
  margin-left: 80px;
  margin-right: 80px;
  border-radius: 60px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.choose_box {
  padding-top: 80px;
}

.choose_check {
  padding-top: 47px;
}
</style>
