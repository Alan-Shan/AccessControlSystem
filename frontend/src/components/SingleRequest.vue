<template>
  <!-- single request form template -->
  <div class="container">
    <div class="row">
      <div class="col">
        <h1 class="text-center">Заявка</h1>
        <div v-if="loading" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="sr-only">Loading...</span>
          </div>
        </div>
        <div v-else>
          <div v-if="message.text" class="alert" :class="alertClass" role="alert">
            {{ message.text }}
          </div>
          <form>
            <div class="form-group">
              <label for="name">Имя</label>
              <input type="text" class="form-control" id="name" v-model="request.name" disabled>
            </div>
            <div class="form-group">
              <label for="surname">Фамилия</label>
              <input type="text" class="form-control" id="surname" v-model="request.surname" disabled>
            </div>
            <div class="form-group">
              <label for="patronymic">Отчество</label>
              <input type="text" class="form-control" id="patronymic" v-model="request.patronymic" disabled>
            </div>
            <div class="form-group">
              <label for="email">Email</label>
              <input type="email" class="form-control" id="email" v-model="request.email" disabled>
            </div>
            <div class="form-group">
              <label for="phone">Телефон</label>
              <input type="text" class="form-control" id="phone" v-model="request.phone" disabled>
            </div>
            <div class="form-group">
              <label for="visitPurpose">Цель визита</label>
              <input type="text" class="form-control" id="visitPurpose" v-model="request.visitPurpose" disabled>
            </div>
            <div class="form-group">
              <label for="documentType">Тип документа</label>
              <input type="text" class="form-control" id="documentType" v-model="request.document.type" disabled>
            </div>
            <div class="form-group">
              <label for="documentNumber">Номер документа</label>
              <input type="text" class="form-control" id="documentNumber" v-model="request.document.number" disabled>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "SingleRequest",
  data() {
    console.log(this.$route.params.id);
    return {
      request: {},
      loading: true,
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
  methods: {}
}
</script>

<style scoped>

</style>