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
        <button class="btn_check_box" @click="active = !active">
          <p class="but_check">Оценить стоимость</p>
        </button>
      </header>
    </div>

    <transition name="fade">
      <div class="popup" v-if="active">
        <div class="fields">
          <div class="fields_wrap">
            <p class="fields_title">Выберите параметры квартиры</p>

            <form @submit.prevent="send_data" class="fields_form">
              <div class="input_field">
                <p class="field_title">Регион</p>
                <select v-model="region" class="selecter" required>
                  <option disabled value="">Выберите один из вариантов</option>
                  <option value="Moscow">Москва</option>
                  <option value="Saint-Petersburg">Санкт-Петербург</option>
                </select>
              </div>

              <div class="input_field">
                <p class="field_title">Площадь объекта</p>
                <input
                  type="number"
                  v-model="total_area"
                  maxlength="5"
                  oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
                  id="total_area"
                  required
                />
              </div>

              <div class="input_field">
                <p class="field_title">Жилая площадь</p>
                <input
                  type="number"
                  v-model="living_area"
                  maxlength="5"
                  oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
                  id="living_area"
                  required
                />
              </div>

              <div class="input_field">
                <p class="field_title">Площадь кухни</p>
                <input
                  type="number"
                  v-model="kitchen_area"
                  maxlength="5"
                  oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
                  id="kitchen_area"
                  required
                />
              </div>

              <div class="input_field">
                <p class="field_title">Год постройки</p>
                <input
                  type="number"
                  v-model="year"
                  maxlength="4"
                  oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
                  id="year"
                  max="2050"
                  required
                />
              </div>

              <div class="input_field">
                <p class="field_title">Минут до метро(пешком)</p>
                <input
                  type="number"
                  v-model="underground"
                  maxlength="3"
                  oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
                  id="underground"
                  required
                />
              </div>

              <div class="input_field">
                <p class="field_title">Материал дома</p>
                <select v-model="material_type" class="selecter" required>
                  <option disabled value="">Выберите один из вариантов</option>
                  <option value="block">Блочный</option>
                  <option value="brick">Кирпичный</option>
                  <option value="monolith">Монолитный</option>
                  <option value="monolithBrick">Монолитный из кирпича</option>
                  <option value="old">Старый</option>
                  <option value="panel">Панельный</option>
                  <option value="stalin">Сталинская застройка</option>
                  <option value="wireframe">Каркасный</option>
                </select>
              </div>

              <div class="input_field">
                <p class="field_title">Адрес</p>
                <input
                  type="text"
                  v-model="address"
                  id="address"
                  required
                  placeholder="Улица, дом"
                />
              </div>

              <div class="input_field">
                <p class="field_title">Номер этажа</p>
                <input
                  type="number"
                  v-model="floor_number"
                  id="floor_number"
                  maxlength="3"
                  oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
                  required
                />
              </div>

              <div class="input_field">
                <p class="field_title">Всего этажей</p>
                <input
                  type="number"
                  v-model="total_floors"
                  maxlength="3"
                  oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
                  id="total_floors"
                  required
                />
              </div>

              <button
                class="btn_send"
                @click="this.loading = true"
              >
                <p class="but_send">Отправить</p>
              </button>

              <button class="btn_send" @click="active = !active">
                <p class="but_send">Назад</p>
              </button>
              <transition name="fade" v-if="loading">
                <p class="loader">Загрузка...</p>
              </transition>
              <transition name="fade" v-if="error">
                <p class="error">Ошибка! Попробуйте снова.</p>
              </transition>
            </form>

            <transition name="fade" v-if="seen_results">
              <div class="cost" v-if="seen_results">
                <p class="cost_title">
                  Предполагаемая рыночная цена жилья: {{ this.price }} Руб.
                </p>
                <p class="cost_title">Залоговая цена: {{ this.refund }} Руб.</p>
                <div class="cost_title">
                  Качество воздуха:
                  <div
                    class="quality"
                    :class="{
                      quality_1: this.air_quality == 1,
                      quality_2: this.air_quality == 2,
                      quality_3: this.air_quality == 3,
                      quality_4: this.air_quality == 4,
                      quality_5: this.air_quality == 5,
                    }"
                  >
                    {{ this.air_quality }}
                  </div>
                  Cодержание CO в воздухе {{ this.comp_co }}
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </transition>
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
      active: false,
      price: "",
      refund: "",
      air_quality: "",
      comp_co: "",
      seen_results: false,
      loading: false,
      error: false,
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
          underground: this.underground > 15 ? 1 : 0,
          material_type: this.material_type,
          address: this.address,
          floor_number: this.floor_number,
          total_floors: this.total_floors,
        })
      );
    },
  },
  mounted() {
    this.sockets.subscribe("price", (data) => {
      this.price = data.price;
      this.refund = data.refund;
      this.air_quality = data.air_quality;
      this.comp_co = data.components.co;
      this.loading = false;
      this.seen_results = true;
    });
    this.sockets.subscribe("error", (data) => {
      this.loading = false;
      this.error = true;
    });
  },
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
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
  background-position: bottom;
  padding-top: 40px;
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
  font-size: 25px;
  line-height: 44px;
  color: #444040;
}

.btn_check_box {
  background: #fdf8f8;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(15px);
  border-radius: 60px;
  padding: 5px 30px;
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

.fields {
  background-color: #f4ebe9;
  padding: 60px;
}

.fields_wrap {
  border-radius: 30px;
  background-color: #fbfbfb;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  padding-bottom: 60px;
}

.fields_title {
  width: 100%;
  font-size: 25px;
  text-align: center;
  margin-top: 30px;
  margin-bottom: 20px;
}

.fields_form {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  padding: 0 30px;
  justify-content: center;
}

.input_field {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 35px;
}

.field_title {
  width: 100%;
  text-align: center;
  margin-bottom: 10px;
}

input {
  width: 50%;
  height: 20px;
  padding: 10px 15px;
  color: #575555;
  border: 1px solid rgb(201, 201, 201); /* Параметры рамки */
  border-radius: 15px;
  outline: 0;
  outline-offset: 0;
}

.cost {
  margin-top: 30px;
}

.cost_title {
  font-size: 30px;

  text-align: center;
  margin-bottom: 15px;
}

.popup {
  position: absolute;
  margin-left: auto;
  margin-right: auto;
  left: 0;
  top: 0;
  text-align: center;
}

.but_send {
  font-family: Montserrat;
  font-style: normal;
  font-weight: 600;
  font-size: 25px;
  line-height: 44px;
  color: #444040;
}

.btn_send {
  background: #fdf8f8;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(15px);
  border-radius: 60px;
  padding: 5px 30px;
  margin-top: 58px;
  transition: 0.3s ease-in-out;
  margin-right: 60px;
}

.btn_send:hover,
.btn_send:focus,
.btn_send:active {
  background: #dfd6d6;
}

.selecter {
  width: 53%;
  height: 40px;
  padding: 10px 15px;
  color: #575555;
  border: 1px solid rgb(201, 201, 201); /* Параметры рамки */
  border-radius: 15px;
  outline: 0;
  outline-offset: 0;
}

.quality {
  width: 100%;
  padding-top: 20px;
  padding-bottom: 20px;
  border-radius: 15px;
  margin-top: 15px;
  margin-bottom: 15px;
  text-align: center;
  color: #e0e0e0;
  font-weight: bold;
}
.quality_1 {
  background-color: #09f343;
}

.quality_2 {
  background-color: #d3e910;
  color: #f0f0f0;
}

.quality_3 {
  background-color: #e9c913;
  color: #f0f0f0;
}

.quality_4 {
  background-color: #fc9917;
  color: #f0f0f0;
}

.quality_5 {
  background-color: #f1440f;
}

.loader {
  font-size: 30px;
  text-align: center;
  width: 100%;
  margin-top: 20px;
  color: #0f8f2f;
}

.error {
  font-size: 30px;
  text-align: center;
  width: 100%;
  margin-top: 20px;
  color: #df0f0f;
}
</style>
