<template>
  <div class="h-100 d-flex align-items-center justify-content-center">
    <div class="container w-auto">
      <div class="alert" :class="{ 'alert-danger': message.isError, 'alert-success': !message.isError }" role="alert"
           v-if="message.show">
        {{ message.text }}
      </div>
      <h3 class="mb-5">Заявка на посещение</h3>
      <form>
        <div class="row">
          <div class="col-md-6">
            <h5 class="text-muted">Контактная информация</h5>
            <div class="form-group mb-3">
              <label for="surname">Фамилия</label>
              <input type="text" v-model="surname" class="form-control" id="surname" placeholder="Иванов">
              <small id="surnameErrors" v-if="'surname' in errors" class="form-text text-danger">
                {{ errors.surname }}
              </small>
            </div>
            <div class="form-group mb-3">
              <label for="name">Имя</label>
              <input type="text" v-model="name" class="form-control" id="name" placeholder="Иван">
              <small id="nameErrors" v-if="'name' in errors" class="form-text text-danger">
                {{ errors.name }}
              </small>
            </div>
            <div class="form-group mb-3">
              <label for="patronymic">Отчество</label>
              <input type="text" v-model="patronymic" class="form-control" id="patronymic" placeholder="Иванович">
              <small id="patronymicErrors" v-if="'patronymic' in errors" class="form-text text-danger">
                {{ errors.patronymic }}
              </small>
            </div>
            <div class="form-group mb-3">
              <label for="email">E-mail</label>
              <input type="email" v-model="email" class="form-control" id="email" placeholder="email@ilum.top">
              <small id="emailErrors" v-if="'email' in errors" class="form-text text-danger">
                {{ errors.email }}
              </small>
            </div>
            <div class="form-group mb-3">
              <label for="phone">Телефон</label>
              <input type="tel" v-model="phone" class="form-control" id="phone" placeholder="+71234567890">
              <small id="phoneErrors" v-if="'phone' in errors" class="form-text text-danger">
                {{ errors.phone }}
              </small>
            </div>
          </div>
          <div class="col-md-6">
            <h5 class="text-muted">Информация о документе</h5>
            <span class="">Тип документа</span>
            <div class="row mb-3">
              <div class="form-group col-md-6">
                <input class="me-1" type="radio" id="passport" value="passport"
                       v-model="document.type" name="doc_type" checked/>
                <label for="passport">Паспорт</label>
              </div>
              <div class="form-group col-md-6">
                <input class="me-1" type="radio" id="drivers_license"
                       value="drivers_license" v-model="document.type" name="doc_type"/>
                <label for="drivers_license">Водительское удостоверение</label>
              </div>
            </div>
            <div class="form-group mb-3">
              <label for="doc_number">Номер документа</label>
              <input type="text" v-model="document.number" class="form-control" id="doc_number"
                     placeholder="1234 567890">
              <small id="doc_numberErrors" v-if="'doc_number' in errors" class="form-text text-danger">
                {{ errors.doc_number }}
              </small>
            </div>
            <div class="form-group mb-3">
              <label for="visit_purpose">Цель посещения</label>
              <input type="text" v-model="visitPurpose" class="form-control" id="visit_purpose"
                     placeholder="Получение документов">
              <small id="visit_purposeErrors" v-if="'visit_purpose' in errors" class="form-text text-danger">
                {{ errors.visit_purpose }}
              </small>
            </div>
          </div>
        </div>
        <div class="form-group mb-3">
          <div class="w-100">
            <input type="checkbox" class="me-1" v-model="consent" id="data_processing_consent"/>
            <label for="data_processing_consent">Даю согласие на <a href="#">обработку персональных данных</a></label>
          </div>
          <small id="consentErrors" v-if="'consent' in errors" class="form-text text-danger">
            {{ errors.consent }}
          </small>
        </div>
        <button @click="sendForm"
                class="btn btn-primary" type="button" :disabled="sending">
          <span v-if="sending"
                class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
          {{ sending ? 'Отправка...' : 'Отправить' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "ApplyForVisit",
  data() {
    return {
      name: "",
      surname: "",
      patronymic: "",
      email: "",
      phone: "",
      visitPurpose: "",
      document: {
        type: "passport",
        series: "",
        number: "",
      },
      consent: false,
      message: {
        show: false,
        text: "",
        isError: false,
      },
      errors: {},
      sending: false,
    };
  },
  methods: {
    checkForm: function (e) {
      if (!this.name) {
        this.errors.name = "Введите имя";
      }
      if (!this.surname) {
        this.errors.surname = "Введите фамилию";
      }
      if (!this.patronymic) {
        this.errors.patronymic = "Введите отчество";
      }
      if (!this.email) {
        this.errors.email = "Введите email";
      } else if (!this.validEmail(this.email)) {
        this.errors.email = "Введите корректный email";
      }
      if (!this.phone) {
        this.errors.phone = "Введите телефон";
      }
      if (!this.document.type || !this.document.number) {
        this.errors.doc_number = "Некорректный документ.";
      }
      if (!this.consent) {
        this.errors.consent = "Необходимо дать согласие на обработку персональных данных";
      }
      if (!Object.keys(this.errors).length) {
        return true;
      }
      e.preventDefault();
      return false;
    },
    validEmail: function (email) {
      // eslint-disable-next-line no-useless-escape
      const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(String(email).toLowerCase());
    },
    sendForm: function (e) {
      this.errors = {};
      this.message.show = false;
      if (this.checkForm(e)) {
        this.sending = true;
        api.postApplication(
            {
              "name": this.name,
              "surname": this.surname,
              "patronymic": this.patronymic,
              "email": this.email,
              "phone": this.phone,
              "purpose": this.visitPurpose,
              "document_type": this.document.type,
              "document_number": this.document.number,
            }
        ).then(() => {
          this.message.text = "Заявка успешно отправлена";
          this.message.isError = false;
        }).catch(() => {
          this.message.text = "Произошла ошибка. Пожалуйста, попробуйте позже.";
          this.message.isError = true;
        }).finally(() => {
          this.message.show = true;
          this.sending = false;
        });
      }
    }
  }
}
</script>

<style scoped>

</style>