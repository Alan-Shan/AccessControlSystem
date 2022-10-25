<template>
  <!-- single request form template -->
  <div class="container">
    <div class="row">
      <div class="col">
        <h1 class="text-center">Заявка</h1>
        <div v-if="loading" class="d-flex justify-content-center w-100 mt-5 mb-5">
          <div class="spinner-grow" role="status">
          </div>
        </div>
        <div v-else>
          <div v-if="message.text" class="alert" :class="alertClass" role="alert">
            {{ message.text }}
          </div>
          <form>
            <div class="form-group mb-3">
              <label for="name">Имя</label>
              <input type="text" class="form-control" id="name" v-model="request.name">
            </div>
            <div class="form-group mb-3">
              <label for="surname">Фамилия</label>
              <input type="text" class="form-control" id="surname" v-model="request.surname">
            </div>
            <div class="form-group mb-3">
              <label for="patronymic">Отчество</label>
              <input type="text" class="form-control" id="patronymic" v-model="request.patronymic">
            </div>
            <div class="form-group mb-3">
              <label for="email">Email</label>
              <input type="email" class="form-control" id="email" v-model="request.email">
            </div>
            <div class="form-group mb-3">
              <label for="phone">Телефон</label>
              <input type="text" class="form-control" id="phone" v-model="request.phone">
            </div>
            <div class="form-group mb-3">
              <label for="visitPurpose">Цель визита</label>
              <input type="text" class="form-control" id="visitPurpose" v-model="request.purpose">
            </div>
            <span>Тип докумета</span>
            <div class="row mb-3">
              <div class="form-group col-md-6">
                <input class="me-1" type="radio" id="passport" value="passport"
                       v-model="request.document_type" name="doc_type" checked/>
                <label for="passport">Паспорт</label>
              </div>
              <div class="form-group col-md-6">
                <input class="me-1" type="radio" id="drivers_license"
                       value="drivers_license" v-model="request.document_type" name="doc_type"/>
                <label for="drivers_license">Водительское удостоверение</label>
              </div>
            </div>
            <div class="form-group mb-3">
              <label for="documentNumber">Номер документа</label>
              <input type="text" class="form-control" id="documentNumber" v-model="request.document_number">
            </div>
            <div class="form-group mb-3">
              <label for="visitPurpose">Цель визита</label>
              <input type="text" class="form-control" id="visitPurpose" v-model="request.purpose">
            </div>
            <img class="img-fluid" :src="request.base64_image" />
            <div class="form-group mb-3">
              <label for="formFile" class="form-label">Фотография</label>
              <input v-on:change="imageChanged" class="form-control" type="file" id="formFile">
              <small class="form-text text-danger" v-if="'image' in errors">{{ errors.image }}</small>
            </div>
            <button type="button" class="btn btn-primary" @click="saveRequest">
              <font-awesome-icon icon="save"/>
              Сохранить
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import api from "@/services/api";

export default {
  name: "SingleRequest",
  data() {
    return {
      request: {},
      newRequest: !this.$route.params.id,
      loading: true,
      errors: [],
      message: {
        text: "",
        isError: false,
      }
    };
  },
  computed: {
    alertClass() {
      return this.message.isError ? "alert-danger" : "alert-success";
    },
  },
  async mounted() {
    if (this.newRequest) {
      this.loading = false;
      return;
    }
    try {
      await api.getRequest(this.$route.params.id).then((response) => {
        this.request = response.data;
        this.loading = false;
      });
    } catch (e) {
      this.message = {
        text: "Произошла ошибка при загрузке заявки",
        isError: true,
      };
      console.log(e);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    imageChanged(e) {
      this.errors.image = "";
      const reader = new FileReader();
      reader.readAsDataURL(e.target.files[0])
      if (!e.target.files[0].type.match(/image.*/)) {
        this.errors.image = "Файл не является изображением";
        return;
      }
      reader.onload = () => {
        // get base64 string
        this.request.base64_image = reader.result;
      };
    },
    saveRequest() {
      if (this.newRequest) {
        api.postApplication(this.request).then(() => {
          this.message = {
            text: "Заявка успешно создана",
            isError: false,
          };
        }).catch((e) => {
          this.message = {
            text: "Произошла ошибка при создании заявки",
            isError: true,
          };
          console.log(e);
        });
      } else {
        api.modifyRequest({
          base64_image: this.image,
          ...this.request
        }).then(() => {
          this.message = {
            text: "Заявка успешно изменена",
            isError: false,
          };
        }).catch((e) => {
          this.message = {
            text: "Произошла ошибка при изменении заявки",
            isError: true,
          };
          console.log(e);
        });
      }
    },
  }
}
</script>

<style scoped>

</style>